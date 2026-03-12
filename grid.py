import streamlit as st
import random, datetime
from f1_data import RAW_F1, RAW_F2, RAW_F3, daily_played, mark_daily_played

# ── Definición de categorías ─────────────────────────────────
SERIES_OPTS = ["🏎️ Fórmula 1", "🚀 Fórmula 2", "🔵 Fórmula 3"]
DIFF_OPTS   = ["Fácil", "Medio", "Difícil", "Experto"]
DIFF_MULT   = {"Fácil": 1, "Medio": 2, "Difícil": 3, "Experto": 5}
DIFF_HINTS  = {"Fácil": 4, "Medio": 2, "Difícil": 1, "Experto": 0}

def _get_raw(series):
    if series == "🏎️ Fórmula 1":  return RAW_F1
    if series == "🚀 Fórmula 2":  return RAW_F2
    return RAW_F3

def _make_categories(raw):
    """Genera categorías de filas y columnas desde los datos."""
    teams = {}
    nations = {}
    for name, data in raw.items():
        for team in data[0]:
            teams.setdefault(team, set()).add(name)
        nations.setdefault(data[1], set()).add(name)

    cats = []
    # Top equipos (min 3 pilotos)
    for team, pilots in teams.items():
        if len(pilots) >= 3:
            cats.append({
                "label": f"Pilotó para {team.title()}",
                "check": lambda n, t=team: t in RAW_F1.get(n, RAW_F2.get(n, RAW_F3.get(n, ([],))))[0]
            })
    # Nacionalidades comunes
    for nat, pilots in nations.items():
        if len(pilots) >= 3:
            cats.append({
                "label": f"Nacionalidad: {nat.title()}",
                "check": lambda n, na=nat: RAW_F1.get(n, RAW_F2.get(n, RAW_F3.get(n, ([], na))))[1] == na
            })
    # Victorias
    cats.append({"label": "≥1 victoria", "check": lambda n: (RAW_F1.get(n) or RAW_F2.get(n) or RAW_F3.get(n, (None,None,0)))[2] >= 1})
    cats.append({"label": "≥5 victorias", "check": lambda n: (RAW_F1.get(n) or RAW_F2.get(n) or RAW_F3.get(n, (None,None,0)))[2] >= 5})
    cats.append({"label": "Fue campeón", "check": lambda n: bool((RAW_F1.get(n) or RAW_F2.get(n) or RAW_F3.get(n, (None,None,None,None,False)))[4])})
    return cats

def _build_grid(raw, size=3):
    """Genera una grilla válida."""
    cats = _make_categories(raw)
    all_names = list(raw.keys())
    for _ in range(500):
        cols = random.sample(cats, size)
        rows = random.sample([c for c in cats if c not in cols], size)
        answers = {}
        valid = True
        for r, rcat in enumerate(rows):
            for c, ccat in enumerate(cols):
                sol = [n for n in all_names if ccat["check"](n) and rcat["check"](n)]
                if not sol:
                    valid = False
                    break
                answers[(r, c)] = sol
            if not valid:
                break
        if valid:
            return cols, rows, answers
    return None, None, None

def init():
    if "gr_grid" not in st.session_state:
        st.session_state.gr_series = "🏎️ Fórmula 1"
        st.session_state.gr_diff   = "Medio"
        st.session_state.gr_size   = 3
        st.session_state.gr_daily  = False
        st.session_state.gr_grid   = None
        st.session_state.gr_score  = 0
        st.session_state.gr_solved = {}
        st.session_state.gr_guesses = {}
        st.session_state.gr_done   = False

def _new_game():
    raw = _get_raw(st.session_state.gr_series)
    size = 3 if st.session_state.gr_diff in ["Fácil", "Medio"] else 4
    cols, rows, answers = _build_grid(raw, size)
    if cols is None:
        st.error("No se pudo generar la grilla. Intenta de nuevo.")
        return
    st.session_state.gr_grid    = {"cols": cols, "rows": rows, "answers": answers, "size": size}
    st.session_state.gr_solved  = {}
    st.session_state.gr_guesses = {}
    st.session_state.gr_done    = False
    st.session_state.gr_score   = 0
    st.session_state.gr_checked = {}

def _check_cell(r, c, guess):
    answers = st.session_state.gr_grid["answers"]
    correct_list = answers.get((r, c), [])
    return guess.strip().lower() in [x.lower() for x in correct_list]

def render():
    init()
    st.markdown("## 🔲 Grid Challenge")
    st.caption("Encontrá el piloto que cumple ambas condiciones: fila y columna")

    # Controls
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
        series = st.selectbox("Serie", SERIES_OPTS, key="gr_series_sel",
                              index=SERIES_OPTS.index(st.session_state.gr_series),
                              label_visibility="collapsed")
        if series != st.session_state.gr_series:
            st.session_state.gr_series = series
    with col2:
        diff = st.selectbox("Dificultad", DIFF_OPTS, key="gr_diff_sel",
                            index=DIFF_OPTS.index(st.session_state.gr_diff),
                            label_visibility="collapsed")
        if diff != st.session_state.gr_diff:
            st.session_state.gr_diff = diff
    with col3:
        daily = st.toggle("📅", key="gr_daily_tog", value=st.session_state.gr_daily)
        st.session_state.gr_daily = daily
    with col4:
        if st.button("▶ Nueva", type="primary"):
            if daily and daily_played(f"grid_{series}_{diff}"):
                st.warning("🔒 Ya jugaste el grid diario.")
            else:
                _new_game()
                st.rerun()

    if st.session_state.gr_grid is None:
        st.info("Elegí serie y dificultad, luego pulsá **▶ Nueva** para empezar.")
        return

    grid = st.session_state.gr_grid
    size = grid["size"]
    cols_cats = grid["cols"]
    rows_cats = grid["rows"]

    # Header de columnas
    header = [""] + [c["label"] for c in cols_cats]
    col_widths = [2] + [3] * size
    cols_ui = st.columns(col_widths)
    for i, h in enumerate(header):
        with cols_ui[i]:
            if h:
                st.markdown(f"<div style='background:#1a1a1a;border-radius:6px;padding:8px;"
                            f"text-align:center;font-size:12px;font-weight:bold;color:#e10600'>{h}</div>",
                            unsafe_allow_html=True)
            else:
                st.write("")

    # Filas
    total_cells = size * size
    correct_cells = sum(1 for v in st.session_state.gr_solved.values() if v)
    score = correct_cells * 100 * DIFF_MULT[st.session_state.gr_diff]

    for r, rcat in enumerate(rows_cats):
        row_cols = st.columns(col_widths)
        with row_cols[0]:
            st.markdown(f"<div style='background:#1a1a1a;border-radius:6px;padding:8px;"
                        f"text-align:center;font-size:12px;font-weight:bold;color:#ffd700'>{rcat['label']}</div>",
                        unsafe_allow_html=True)
        for c in range(size):
            with row_cols[c + 1]:
                cell_key = (r, c)
                if cell_key in st.session_state.gr_solved:
                    is_ok = st.session_state.gr_solved[cell_key]
                    val   = st.session_state.gr_guesses.get(cell_key, "")
                    bg    = "#1b5e20" if is_ok else "#b71c1c"
                    st.markdown(f"<div style='background:{bg};border-radius:6px;padding:10px;"
                                f"text-align:center;font-size:13px;color:white;font-weight:bold'>"
                                f"{'✓' if is_ok else '✗'} {val.title()}</div>", unsafe_allow_html=True)
                else:
                    guess = st.text_input("", key=f"gr_cell_{r}_{c}",
                                          placeholder="Piloto...",
                                          label_visibility="collapsed")
                    if st.button("✔", key=f"gr_check_{r}_{c}"):
                        if guess.strip():
                            ok = _check_cell(r, c, guess)
                            st.session_state.gr_solved[cell_key] = ok
                            st.session_state.gr_guesses[cell_key] = guess
                            st.rerun()

    st.metric("⭐ Puntos", score)

    # Check si terminó
    if len(st.session_state.gr_solved) == total_cells:
        if correct_cells == total_cells:
            st.success("🏆 ¡GRILLA COMPLETA!")
            if st.session_state.gr_daily:
                mark_daily_played(f"grid_{st.session_state.gr_series}_{st.session_state.gr_diff}")
        else:
            st.warning(f"✅ {correct_cells}/{total_cells} correctas · ⭐ {score} pts")
