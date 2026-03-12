import streamlit as st
import random
from f1_data import RAW_F1, CONSTRUCTOR_CATS, ALL_CONSTRUCTORS, daily_played, mark_daily_played

GRID_SIZE = 3
MAX_TRIES = 3

def _build_grid():
    for _ in range(500):
        cols = random.sample(CONSTRUCTOR_CATS, GRID_SIZE)
        rows = random.sample([c for c in CONSTRUCTOR_CATS if c not in cols], GRID_SIZE)
        answers = {}
        valid = True
        for r, rcat in enumerate(rows):
            for c, ccat in enumerate(cols):
                sol = [t for t in ALL_CONSTRUCTORS if ccat["check"](t) and rcat["check"](t)]
                if not sol:
                    valid = False
                    break
                answers[(r, c)] = set(sol)
            if not valid:
                break
        if valid:
            return cols, rows, answers
    return None, None, None

def init():
    if "ctr_grid" not in st.session_state:
        st.session_state.ctr_daily   = False
        st.session_state.ctr_score   = 0
        st.session_state.ctr_solved  = {}
        st.session_state.ctr_tries   = {}
        st.session_state.ctr_done    = False
        cols, rows, answers = _build_grid()
        st.session_state.ctr_grid    = {"cols": cols, "rows": rows, "answers": answers}

def render():
    init()
    st.markdown("## 🏗️ Constructor Challenge")
    st.caption("Encontrá la escudería que cumple condición de fila Y columna · 3 intentos por celda")

    col1, col2 = st.columns([3, 1])
    with col2:
        daily = st.toggle("📅 Diario", key="ctr_daily_tog", value=st.session_state.ctr_daily)
        if daily != st.session_state.ctr_daily:
            st.session_state.ctr_daily = daily
            if daily and daily_played("constructor"):
                st.warning("🔒 Ya jugaste el Constructor del día.")
                if st.button("🎮 Jugar libre"):
                    st.session_state.ctr_daily = False
                    st.rerun()
                return

    if st.button("🔄 Nueva grilla"):
        for k in list(st.session_state.keys()):
            if k.startswith("ctr_"):
                del st.session_state[k]
        st.rerun()

    grid = st.session_state.ctr_grid
    if not grid["cols"]:
        st.error("Error generando grilla.")
        return

    cols_cats = grid["cols"]
    rows_cats = grid["rows"]
    answers   = grid["answers"]

    total = GRID_SIZE * GRID_SIZE
    correct = sum(1 for v in st.session_state.ctr_solved.values() if v is True)
    st.metric("⭐ Puntuación", st.session_state.ctr_score)

    # Header
    col_widths = [2] + [3] * GRID_SIZE
    header_cols = st.columns(col_widths)
    header_cols[0].write("")
    for i, cat in enumerate(cols_cats):
        header_cols[i+1].markdown(
            f"<div style='background:#1a1a1a;border-radius:6px;padding:8px;text-align:center;"
            f"font-size:11px;font-weight:bold;color:#e10600'>{cat['label']}</div>",
            unsafe_allow_html=True
        )

    # Filas
    for r, rcat in enumerate(rows_cats):
        row_cols = st.columns(col_widths)
        with row_cols[0]:
            st.markdown(
                f"<div style='background:#1a1a1a;border-radius:6px;padding:8px;text-align:center;"
                f"font-size:11px;font-weight:bold;color:#ffd700'>{rcat['label']}</div>",
                unsafe_allow_html=True
            )
        for c in range(GRID_SIZE):
            with row_cols[c+1]:
                cell_key = (r, c)
                state = st.session_state.ctr_solved.get(cell_key)
                tries_left = MAX_TRIES - st.session_state.ctr_tries.get(cell_key, 0)

                if state is True:
                    st.markdown("<div style='background:#1b5e20;border-radius:6px;padding:10px;"
                                "text-align:center;color:white'>✅</div>", unsafe_allow_html=True)
                elif state is False:
                    # Mostrar respuesta correcta
                    sol = sorted(answers.get(cell_key, set()))
                    example = sol[0].title() if sol else "?"
                    st.markdown(f"<div style='background:#b71c1c;border-radius:6px;padding:8px;"
                                f"text-align:center;font-size:11px;color:white'>❌ {example}</div>",
                                unsafe_allow_html=True)
                else:
                    guess = st.selectbox("Escudería", [""] + ALL_CONSTRUCTORS,
                                         key=f"ctr_sel_{r}_{c}",
                                         format_func=lambda x: x.title() if x else "— elige —",
                                         label_visibility="collapsed")
                    if st.button(f"✔ ({tries_left})", key=f"ctr_ok_{r}_{c}"):
                        if guess:
                            tries = st.session_state.ctr_tries.get(cell_key, 0) + 1
                            st.session_state.ctr_tries[cell_key] = tries
                            if guess in answers.get(cell_key, set()):
                                pts = 30 * (MAX_TRIES - tries + 1)
                                st.session_state.ctr_score += pts
                                st.session_state.ctr_solved[cell_key] = True
                            elif tries >= MAX_TRIES:
                                st.session_state.ctr_solved[cell_key] = False
                            st.rerun()

    if len(st.session_state.ctr_solved) == total:
        if correct == total:
            st.success("🏆 ¡GRILLA COMPLETA!")
            if st.session_state.ctr_daily:
                mark_daily_played("constructor")
        else:
            st.info(f"✅ {correct}/{total} correctas · ⭐ {st.session_state.ctr_score} pts")
