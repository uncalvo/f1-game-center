import streamlit as st
import random, datetime
from f1_data import RAW_F1, RAW_F2, RAW_F3, daily_played, mark_daily_played

SERIES_OPTS = ["🏎️ Fórmula 1", "🚀 Fórmula 2", "🔵 Fórmula 3"]
DIFF_OPTS   = ["Fácil", "Medio", "Difícil", "Experto"]
DIFF_MULT   = {"Fácil": 1, "Medio": 2, "Difícil": 3, "Experto": 5}

def _get_raw(series):
    if series == "🏎️ Fórmula 1": return RAW_F1
    if series == "🚀 Fórmula 2": return RAW_F2
    return RAW_F3

def _all_names(raw):
    return list(raw.keys())

def _make_categories(raw):
    teams, nations = {}, {}
    for name, data in raw.items():
        for team in data[0]:
            teams.setdefault(team, set()).add(name)
        nations.setdefault(data[1], set()).add(name)

    cats = []
    for team, pilots in teams.items():
        if len(pilots) >= 3:
            cats.append({"label": f"Pilotó para {team.title()}",
                         "check": lambda n, t=team, r=raw: t in r.get(n, ([],))[0]})
    for nat, pilots in nations.items():
        if len(pilots) >= 3:
            cats.append({"label": f"Nacionalidad: {nat.title()}",
                         "check": lambda n, na=nat, r=raw: r.get(n, ([], na))[1] == na})
    cats.append({"label": "≥1 victoria",  "check": lambda n, r=raw: r.get(n, (None,None,0))[2] >= 1})
    cats.append({"label": "≥5 victorias", "check": lambda n, r=raw: r.get(n, (None,None,0))[2] >= 5})
    cats.append({"label": "Fue campeón",  "check": lambda n, r=raw: bool(r.get(n, (None,None,None,None,False))[4])})
    return cats

def _build_grid(raw, size=3):
    cats  = _make_categories(raw)
    names = _all_names(raw)
    for _ in range(500):
        cols = random.sample(cats, size)
        rows = random.sample([c for c in cats if c not in cols], size)
        answers = {}
        valid = True
        for r, rcat in enumerate(rows):
            for c, ccat in enumerate(cols):
                sol = [n for n in names if ccat["check"](n) and rcat["check"](n)]
                if not sol:
                    valid = False
                    break
                answers[(r, c)] = sol
            if not valid:
                break
        if valid:
            return cols, rows, answers
    return None, None, None

def _driver_options(series):
    raw = _get_raw(series)
    return sorted(set(n.title() for n in raw.keys()))

def init():
    if "gr_initialized" not in st.session_state:
        st.session_state.gr_initialized = True
        st.session_state.gr_series = "🏎️ Fórmula 1"
        st.session_state.gr_diff   = "Medio"
        st.session_state.gr_daily  = False
        st.session_state.gr_grid   = None
        st.session_state.gr_score  = 0
        st.session_state.gr_solved = {}

def _new_game():
    series = st.session_state.gr_series
    diff   = st.session_state.gr_diff
    raw    = _get_raw(series)
    size   = 4 if diff in ["Difícil", "Experto"] else 3
    cols, rows, answers = _build_grid(raw, size)
    if cols is None:
        return False
    st.session_state.gr_grid   = {"cols": cols, "rows": rows, "answers": answers, "size": size}
    st.session_state.gr_solved = {}
    st.session_state.gr_score  = 0
    return True

def render():
    init()
    st.markdown("## 🔲 Grid Challenge")
    st.caption("Encontrá el piloto que cumple ambas condiciones: fila y columna")

    # Controles
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
        series = st.selectbox("Serie", SERIES_OPTS, key="gr_series_sel",
                              index=SERIES_OPTS.index(st.session_state.gr_series),
                              label_visibility="collapsed")
        st.session_state.gr_series = series
    with col2:
        diff = st.selectbox("Dificultad", DIFF_OPTS, key="gr_diff_sel",
                            index=DIFF_OPTS.index(st.session_state.gr_diff),
                            label_visibility="collapsed")
        st.session_state.gr_diff = diff
    with col3:
        daily = st.toggle("📅", key="gr_daily_tog", value=st.session_state.gr_daily)
        st.session_state.gr_daily = daily
    with col4:
        if st.button("▶ Nueva", type="primary"):
            if daily and daily_played(f"grid_{series}_{diff}"):
                st.warning("🔒 Ya jugaste el grid diario.")
            else:
                if _new_game():
                    st.rerun()

    if st.session_state.gr_grid is None:
        st.info("Elegí serie y dificultad, luego pulsá **▶ Nueva** para empezar.")
        return

    grid      = st.session_state.gr_grid
    size      = grid["size"]
    cols_cats = grid["cols"]
    rows_cats = grid["rows"]
    driver_opts = [""] + _driver_options(st.session_state.gr_series)

    col_widths = [2] + [3] * size

    # Header columnas
    header_cols = st.columns(col_widths)
    header_cols[0].write("")
    for i, cat in enumerate(cols_cats):
        header_cols[i+1].markdown(
            f"<div style='background:#1a1a1a;border-radius:6px;padding:8px;"
            f"text-align:center;font-size:11px;font-weight:bold;color:#e10600'>{cat['label']}</div>",
            unsafe_allow_html=True)

    # Filas
    correct_cells = sum(1 for v in st.session_state.gr_solved.values() if v is True)
    for r, rcat in enumerate(rows_cats):
        row_cols = st.columns(col_widths)
        with row_cols[0]:
            st.markdown(
                f"<div style='background:#1a1a1a;border-radius:6px;padding:8px;"
                f"text-align:center;font-size:11px;font-weight:bold;color:#ffd700'>{rcat['label']}</div>",
                unsafe_allow_html=True)
        for c in range(size):
            with row_cols[c+1]:
                cell_key = (r, c)
                state = st.session_state.gr_solved.get(cell_key)
                if state is True:
                    val = st.session_state.gr_solved.get(f"val_{r}_{c}", "✓")
                    st.markdown(f"<div style='background:#1b5e20;border-radius:6px;padding:10px;"
                                f"text-align:center;font-size:12px;color:white;font-weight:bold'>"
                                f"✅ {val}</div>", unsafe_allow_html=True)
                elif state is False:
                    val = st.session_state.gr_solved.get(f"val_{r}_{c}", "?")
                    st.markdown(f"<div style='background:#b71c1c;border-radius:6px;padding:10px;"
                                f"text-align:center;font-size:12px;color:white'>❌ {val}</div>",
                                unsafe_allow_html=True)
                else:
                    chosen = st.selectbox(
                        "Piloto",
                        driver_opts,
                        key=f"gr_sel_{r}_{c}",
                        label_visibility="collapsed",
                    )
                    if st.button("✔", key=f"gr_ok_{r}_{c}", use_container_width=True):
                        if chosen:
                            answers = grid["answers"]
                            ok = chosen.lower() in [x.lower() for x in answers.get(cell_key, [])]
                            st.session_state.gr_solved[cell_key] = ok
                            st.session_state.gr_solved[f"val_{r}_{c}"] = chosen
                            if ok:
                                mult = DIFF_MULT[st.session_state.gr_diff]
                                st.session_state.gr_score += 100 * mult
                            st.rerun()

    # Score y fin
    total = size * size
    st.metric("⭐ Puntos", st.session_state.gr_score)
    solved = {k: v for k, v in st.session_state.gr_solved.items()
              if isinstance(k, tuple)}
    if len(solved) == total:
        if correct_cells == total:
            st.success("🏆 ¡GRILLA COMPLETA!")
            if st.session_state.gr_daily:
                mark_daily_played(f"grid_{st.session_state.gr_series}_{st.session_state.gr_diff}")
        else:
            st.warning(f"✅ {correct_cells}/{total} correctas")
