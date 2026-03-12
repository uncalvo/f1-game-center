import streamlit as st
import random, datetime
from f1_data import GP_RESULTS, daily_played, mark_daily_played

MEDALS = ["🥇", "🥈", "🥉"] + ["  "] * 7

def _daily_seed():
    return int(datetime.date.today().strftime("%Y%m%d"))

def init():
    if "po_year" not in st.session_state:
        st.session_state.po_daily = False
        st.session_state.po_score = 0
        st.session_state.po_history = []
        years = sorted(GP_RESULTS.keys(), reverse=True)
        st.session_state.po_year = years[0]
        st.session_state.po_gp = None
        st.session_state.po_answer = None
        st.session_state.po_checked = False
        st.session_state.po_result = None

def _get_gps(year):
    return [gp for gp, res in GP_RESULTS.get(year, {}).items() if len(res) >= 10]

def _start_race():
    year = st.session_state.po_year
    gp = st.session_state.po_gp
    if not gp:
        return
    answer = GP_RESULTS[year][gp][:10]
    st.session_state.po_answer = answer
    st.session_state.po_checked = False
    st.session_state.po_result = None
    for i in range(10):
        st.session_state[f"po_input_{i}"] = ""

def _check():
    answer = st.session_state.po_answer
    guesses = [st.session_state.get(f"po_input_{i}", "").strip().lower() for i in range(10)]
    correct_pos = sum(1 for g, a in zip(guesses, answer) if g == a.lower())
    correct_any = sum(1 for g in guesses if g in [a.lower() for a in answer])
    pts = correct_pos * 100 + (correct_any - correct_pos) * 20
    st.session_state.po_score += pts
    st.session_state.po_checked = True
    st.session_state.po_result = (correct_pos, correct_any, pts, guesses, answer)
    if st.session_state.po_daily:
        mark_daily_played("podium")

def render():
    init()
    st.markdown("## 🏆 Podium Challenge")
    st.caption("Adiviná el Top 10 de un Gran Premio histórico de F1")

    col1, col2 = st.columns([3, 1])
    with col2:
        daily = st.toggle("📅 Diario", key="po_daily_tog", value=st.session_state.po_daily)
        if daily != st.session_state.po_daily:
            st.session_state.po_daily = daily
            if daily and daily_played("podium"):
                st.warning("🔒 Ya jugaste el Podium del día.")
                if st.button("🎮 Jugar libre"):
                    st.session_state.po_daily = False
                    st.rerun()
                return

    st.metric("⭐ Puntuación total", st.session_state.po_score)

    if st.session_state.po_answer is None or st.session_state.po_checked:
        # Selector de carrera
        years = sorted(GP_RESULTS.keys(), reverse=True)

        if st.session_state.po_daily:
            rng = random.Random(_daily_seed())
            all_races = [(yr, gp) for yr, gps in GP_RESULTS.items()
                         for gp in gps if len(GP_RESULTS[yr][gp]) >= 10]
            yr, gp = rng.choice(all_races)
            st.session_state.po_year = yr
            st.session_state.po_gp = gp
            st.info(f"📅 Carrera del día: **{gp} {yr}**")
        else:
            col_y, col_g = st.columns(2)
            with col_y:
                year = st.selectbox("Año", years,
                                    index=years.index(st.session_state.po_year),
                                    key="po_year_sel")
                st.session_state.po_year = year
            with col_g:
                gps = _get_gps(st.session_state.po_year)
                if gps:
                    gp = st.selectbox("Gran Premio", gps, key="po_gp_sel")
                    st.session_state.po_gp = gp

        if st.session_state.po_checked and st.session_state.po_result:
            correct_pos, correct_any, pts, guesses, answer = st.session_state.po_result
            st.markdown("### Resultado:")
            for i, (g, a) in enumerate(zip(guesses, answer)):
                if g == a.lower():
                    icon = "🟩"
                elif g in [x.lower() for x in answer]:
                    icon = "🟨"
                else:
                    icon = "🟥"
                st.markdown(f"{MEDALS[i]} P{i+1}: {icon} **{a.title()}** ← tu respuesta: *{g or '(vacío)'}*")
            st.info(f"🟩 {correct_pos}/10 exactos · 🟨 {correct_any-correct_pos} posición errónea · ⭐ +{pts} pts")

        if st.button("▶ Iniciar carrera", type="primary", use_container_width=True):
            _start_race()
            st.rerun()
        return

    # Formulario de respuestas
    answer = st.session_state.po_answer
    yr = st.session_state.po_year
    gp = st.session_state.po_gp

    # Obtener todos los drivers para autocomplete
    all_drivers = sorted(set(d for races in GP_RESULTS.values() for res in races.values() for d in res))

    st.markdown(f"### {gp} {yr} — ¿Quién clasificó P1 a P10?")
    st.caption("🟩 Posición exacta · 🟨 En top 10 pero posición errónea")

    cols = st.columns(2)
    for i in range(10):
        col = cols[i % 2]
        with col:
            val = st.text_input(f"P{i+1}", key=f"po_input_{i}",
                                placeholder=f"P{i+1}...")

    if st.button("✔ Verificar", type="primary", use_container_width=True):
        _check()
        st.rerun()
