import streamlit as st
import random, datetime
from f1_data import GP_RESULTS, daily_played, mark_daily_played

MEDALS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

ALL_GP_DRIVERS = sorted(set(
    d.strip().title()
    for yr in GP_RESULTS.values()
    for res in yr.values()
    for d in res
))

def _daily_seed():
    return int(datetime.date.today().strftime("%Y%m%d"))

def _pick_daily():
    rng = random.Random(_daily_seed())
    all_races = sorted([
        (yr, gp)
        for yr, gps in GP_RESULTS.items()
        for gp, res in gps.items()
        if len(res) >= 10
    ])
    return rng.choice(all_races)

def init():
    if "po_initialized" not in st.session_state:
        st.session_state.po_initialized = True
        st.session_state.po_daily   = False
        st.session_state.po_score   = 0
        years = sorted(GP_RESULTS.keys(), reverse=True)
        st.session_state.po_year    = years[0]
        gps = [gp for gp, res in GP_RESULTS[years[0]].items() if len(res) >= 10]
        st.session_state.po_gp      = gps[0] if gps else None
        st.session_state.po_answer  = None
        st.session_state.po_checked = False
        st.session_state.po_result  = None

def _get_gps(year):
    return [gp for gp, res in GP_RESULTS.get(year, {}).items() if len(res) >= 10]

def _start_race():
    if st.session_state.po_daily:
        yr, gp = _pick_daily()
        st.session_state.po_year = yr
        st.session_state.po_gp   = gp
    year = st.session_state.po_year
    gp   = st.session_state.po_gp
    if not gp:
        return
    st.session_state.po_answer  = GP_RESULTS[year][gp][:10]
    st.session_state.po_checked = False
    st.session_state.po_result  = None
    for i in range(10):
        st.session_state[f"po_sel_{i}"] = ""

def _check():
    answer  = st.session_state.po_answer
    guesses = [st.session_state.get(f"po_sel_{i}", "").strip().lower() for i in range(10)]
    correct_pos = sum(1 for g, a in zip(guesses, answer) if g == a.lower())
    correct_any = sum(1 for g in guesses if g and g in [a.lower() for a in answer])
    pts = correct_pos * 100 + (correct_any - correct_pos) * 20
    st.session_state.po_score  += pts
    st.session_state.po_checked = True
    st.session_state.po_result  = (correct_pos, correct_any, pts, guesses, answer)
    if st.session_state.po_daily:
        mark_daily_played("podium")

def render():
    init()
    st.markdown("## 🏆 Podium Challenge")
    st.caption("Adiviná el Top 10 de un Gran Premio histórico de F1")

    col1, col2 = st.columns([3, 1])
    with col2:
        new_daily = st.toggle("📅 Diario", key="po_daily_tog",
                              value=st.session_state.po_daily)
        if new_daily != st.session_state.po_daily:
            st.session_state.po_daily   = new_daily
            st.session_state.po_answer  = None
            st.session_state.po_checked = False
            st.session_state.po_result  = None
            st.rerun()

    st.metric("⭐ Puntuación total", st.session_state.po_score)

    # Bloqueo diario
    if st.session_state.po_daily and daily_played("podium") and st.session_state.po_answer is None:
        st.warning("🔒 Ya jugaste el Podium del día. ¡Volvé mañana!")
        if st.button("🎮 Jugar sin restricción"):
            st.session_state.po_daily = False
            st.rerun()
        return

    # Pantalla de selección / resultado
    if st.session_state.po_answer is None or st.session_state.po_checked:
        if st.session_state.po_daily:
            yr, gp = _pick_daily()
            st.info(f"📅 Carrera del día: **{gp} {yr}**")
        else:
            years = sorted(GP_RESULTS.keys(), reverse=True)
            col_y, col_g = st.columns(2)
            with col_y:
                year = st.selectbox("Año", years,
                                    index=years.index(st.session_state.po_year),
                                    key="po_year_sel")
                if year != st.session_state.po_year:
                    st.session_state.po_year = year
                    gps = _get_gps(year)
                    st.session_state.po_gp = gps[0] if gps else None
            with col_g:
                gps = _get_gps(st.session_state.po_year)
                if gps:
                    gp_idx = gps.index(st.session_state.po_gp) if st.session_state.po_gp in gps else 0
                    gp = st.selectbox("Gran Premio", gps, index=gp_idx, key="po_gp_sel")
                    st.session_state.po_gp = gp

        if st.session_state.po_checked and st.session_state.po_result:
            correct_pos, correct_any, pts, guesses, answer = st.session_state.po_result
            st.markdown("### Resultado:")
            for i, (g, a) in enumerate(zip(guesses, answer)):
                if g == a.lower():
                    icon = "🟩"
                elif g and g in [x.lower() for x in answer]:
                    icon = "🟨"
                else:
                    icon = "🟥"
                st.markdown(f"{MEDALS[i]} P{i+1}: {icon} **{a.title()}** ← *{g.title() if g else '(vacío)'}*")
            st.info(f"🟩 {correct_pos}/10 exactos · 🟨 {correct_any - correct_pos} pos. errónea · ⭐ +{pts} pts")

        if st.button("▶ Iniciar carrera", type="primary", use_container_width=True):
            _start_race()
            st.rerun()
        return

    # Formulario de respuestas
    yr  = st.session_state.po_year
    gp  = st.session_state.po_gp
    st.markdown(f"### {gp} {yr} — ¿Quién clasificó P1 a P10?")
    st.caption("🟩 Posición exacta · 🟨 En top 10 pero posición errónea · Escribí para filtrar la lista")

    driver_opts = [""] + ALL_GP_DRIVERS
    cols = st.columns(2)
    for i in range(10):
        with cols[i % 2]:
            current = st.session_state.get(f"po_sel_{i}", "")
            idx = driver_opts.index(current.title()) if current.title() in driver_opts else 0
            chosen = st.selectbox(
                f"{MEDALS[i]} P{i+1}",
                driver_opts,
                index=idx,
                key=f"po_sel_widget_{i}",
            )
            st.session_state[f"po_sel_{i}"] = chosen.lower() if chosen else ""

    if st.button("✔ Verificar", type="primary", use_container_width=True):
        _check()
        st.rerun()
