import streamlit as st
import random, datetime
from f1_data import F1_CIRCUITS, daily_played, mark_daily_played

PTS_PER_PISTA = [600, 450, 300, 200, 100, 50]

FLAG_MAP = {
    "Mónaco": "🇲🇨", "Italia": "🇮🇹", "Gran Bretaña": "🇬🇧", "Bélgica": "🇧🇪",
    "Japón": "🇯🇵", "Brasil": "🇧🇷", "España": "🇪🇸", "Emiratos Árabes": "🇦🇪",
    "Hungría": "🇭🇺", "Países Bajos": "🇳🇱", "Alemania": "🇩🇪", "Arabia Saudí": "🇸🇦",
    "Bahréin": "🇧🇭", "Australia": "🇦🇺", "China": "🇨🇳", "Estados Unidos": "🇺🇸",
    "México": "🇲🇽", "Singapur": "🇸🇬", "Azerbaiyán": "🇦🇿", "Canadá": "🇨🇦",
    "Catar": "🇶🇦", "Francia": "🇫🇷", "Portugal": "🇵🇹", "Turquía": "🇹🇷",
}

def _pick_circuit(seed=None):
    all_keys = list(F1_CIRCUITS.keys())
    rng = random.Random(seed) if seed is not None else random
    key = rng.choice(all_keys)
    # 4 opciones: la correcta + 3 random distintas
    others = [k for k in all_keys if k != key]
    wrong = rng.sample(others, 3)
    options = wrong + [key]
    rng.shuffle(options)
    return key, options

def init():
    if "cg_key" not in st.session_state:
        st.session_state.cg_daily = False
        st.session_state.cg_score = 0
        st.session_state.cg_streak = 0
        st.session_state.cg_total = 0
        st.session_state.cg_correct_count = 0
        st.session_state.cg_pistas = 1
        st.session_state.cg_answered = False
        st.session_state.cg_last_correct = None
        st.session_state.cg_vistos = set()
        _new_question()

def _new_question():
    if st.session_state.get("cg_daily") and daily_played("circuit"):
        st.session_state.cg_locked = True
        return
    st.session_state.cg_locked = False
    if st.session_state.get("cg_daily"):
        seed = int(datetime.date.today().strftime("%Y%m%d")) + st.session_state.cg_total
        key, options = _pick_circuit(seed=seed)
    else:
        pool = [k for k in F1_CIRCUITS if k not in st.session_state.cg_vistos]
        if not pool:
            st.session_state.cg_vistos = set()
            pool = list(F1_CIRCUITS.keys())
        key = random.choice(pool)
        others = [k for k in F1_CIRCUITS if k != key]
        wrong = random.sample(others, 3)
        options = wrong + [key]
        random.shuffle(options)
    st.session_state.cg_vistos.add(key)
    st.session_state.cg_key = key
    st.session_state.cg_options = options
    st.session_state.cg_pistas = 1
    st.session_state.cg_answered = False
    st.session_state.cg_last_correct = None

def _answer(chosen):
    if st.session_state.cg_answered:
        return
    correct = st.session_state.cg_key
    correct_data = F1_CIRCUITS[correct]
    st.session_state.cg_answered = True
    st.session_state.cg_total += 1

    if chosen == correct:
        pts_idx = min(st.session_state.cg_pistas - 1, len(PTS_PER_PISTA) - 1)
        pts = PTS_PER_PISTA[pts_idx]
        st.session_state.cg_streak += 1
        if st.session_state.cg_streak > 1:
            bonus = min(st.session_state.cg_streak - 1, 5) * 30
            pts += bonus
        st.session_state.cg_score += pts
        st.session_state.cg_correct_count += 1
        st.session_state.cg_last_correct = (True, pts, correct, correct_data)
    else:
        st.session_state.cg_streak = 0
        st.session_state.cg_last_correct = (False, 0, correct, correct_data)
        if st.session_state.cg_daily:
            mark_daily_played("circuit")

def render():
    init()
    st.markdown("## 🗺️ ¿En qué Circuito?")
    st.caption("Pistas progresivas sobre un circuito de F1 · Menos pistas = más puntos")

    col1, col2 = st.columns([3, 1])
    with col2:
        daily = st.toggle("📅 Diario", key="cg_daily_tog", value=st.session_state.cg_daily)
        if daily != st.session_state.cg_daily:
            st.session_state.cg_daily = daily
            if daily and daily_played("circuit"):
                st.session_state.cg_locked = True
            _new_question()
            st.rerun()

    if st.session_state.get("cg_locked"):
        st.warning("🔒 Ya jugaste el circuito del día. ¡Volvé mañana!")
        if st.button("🎮 Jugar sin restricción"):
            st.session_state.cg_daily = False
            st.session_state.cg_locked = False
            _new_question()
            st.rerun()
        return

    # Stats
    col_s, col_r, col_p = st.columns(3)
    col_s.metric("⭐ Puntos", st.session_state.cg_score)
    col_r.metric("🔥 Racha", st.session_state.cg_streak)
    col_p.metric("✅ Correctas", st.session_state.cg_correct_count)

    data = F1_CIRCUITS[st.session_state.cg_key]
    caracteristicas = data.get("caracteristicas", [])
    pts_si = PTS_PER_PISTA[min(st.session_state.cg_pistas - 1, len(PTS_PER_PISTA)-1)]

    # Pistas mostradas
    st.markdown("### Pistas:")
    for i in range(st.session_state.cg_pistas):
        if i < len(caracteristicas):
            st.markdown(f"**{i+1}.** {caracteristicas[i]}")

    if not st.session_state.cg_answered:
        st.caption(f"💡 Si acertás ahora: **{pts_si} pts**")

        col_btn1, col_btn2 = st.columns(2)
        options = st.session_state.cg_options
        for idx, opt in enumerate(options):
            opt_data = F1_CIRCUITS[opt]
            flag = FLAG_MAP.get(opt_data.get("pais", ""), "🏁")
            label = f"{flag} {opt}"
            col = col_btn1 if idx % 2 == 0 else col_btn2
            with col:
                if st.button(label, key=f"cg_opt_{idx}", use_container_width=True):
                    _answer(opt)
                    st.rerun()

        if st.session_state.cg_pistas < len(caracteristicas):
            if st.button("🔍 Ver siguiente pista", use_container_width=True):
                st.session_state.cg_pistas += 1
                st.rerun()
    else:
        correct_flag, pts, correct_key, correct_data = st.session_state.cg_last_correct
        flag = FLAG_MAP.get(correct_data.get("pais", ""), "🏁")
        if correct_flag:
            st.success(f"✅ ¡Correcto! **{correct_key}** {flag} +{pts} pts")
        else:
            st.error(f"❌ Era **{correct_key}** {flag}")

        if correct_data.get("ciudad") and correct_data.get("pais"):
            st.info(f"📍 {correct_data['ciudad']}, {correct_data['pais']}")

        if st.button("➡️ Siguiente circuito", type="primary", use_container_width=True):
            _new_question()
            st.rerun()
