import streamlit as st
import random, datetime
from f1_data import RAW_F1, daily_played, mark_daily_played

PISTAS_DEF = [
    ("Nacionalidad",         lambda n, d: d[1].title(),                        500),
    ("Debut en F1",          lambda n, d: str(d[5]),                           400),
    ("Año de nacimiento",    lambda n, d: str(d[7]),                           350),
    ("Últimas temporadas",   lambda n, d: f"{d[8]} temporadas en F1",          300),
    ("Victorias",            lambda n, d: f"{d[2]} victorias en F1",           200),
    ("Podios",               lambda n, d: f"{d[3]} podios en F1",              100),
    ("¿Fue campeón?",        lambda n, d: "Sí, fue campeón mundial" if d[4] else "No fue campeón mundial", 50),
]

def _candidates():
    return [(n, d) for n, d in RAW_F1.items() if d[2] > 0 or d[3] > 0 or d[4]]

def _pick_pilot():
    cands = _candidates()
    if st.session_state.my_daily:
        seed = int(datetime.date.today().strftime("%Y%m%d"))
        rng = random.Random(seed)
        pool = sorted(cands, key=lambda x: x[0])
        name, data = rng.choice(pool)
    else:
        pool = [c for c in cands if c[0] not in st.session_state.my_vistos]
        if not pool:
            st.session_state.my_vistos = set()
            pool = cands
        name, data = random.choice(pool)
    st.session_state.my_vistos.add(name)
    return name, data

def init():
    if "my_name" not in st.session_state:
        st.session_state.my_daily = False
        st.session_state.my_score = 0
        st.session_state.my_vistos = set()
        st.session_state.my_pistas = 1
        st.session_state.my_answered = False
        st.session_state.my_last_result = None
        name, data = _pick_pilot()
        st.session_state.my_name = name
        st.session_state.my_data = data

def _answer(guess):
    if st.session_state.my_answered:
        return
    name = st.session_state.my_name
    correct = guess.strip().lower() == name.lower()
    pts_idx = min(st.session_state.my_pistas - 1, len(PISTAS_DEF)-1)
    pts = PISTAS_DEF[pts_idx][2] if correct else 0
    st.session_state.my_answered = True
    st.session_state.my_score += pts
    st.session_state.my_last_result = (correct, pts, name)
    if st.session_state.my_daily:
        mark_daily_played("mystery")

def render():
    init()
    st.markdown("## 🕵️ Piloto Misterioso")
    st.caption("Adiviná el piloto con las menos pistas posibles · Menos pistas = más puntos")

    col1, col2 = st.columns([3, 1])
    with col2:
        daily = st.toggle("📅 Diario", key="my_daily_tog", value=st.session_state.my_daily)
        if daily != st.session_state.my_daily:
            st.session_state.my_daily = daily
            if daily and daily_played("mystery"):
                st.warning("🔒 Ya jugaste el piloto del día.")
                if st.button("🎮 Jugar libre"):
                    st.session_state.my_daily = False
                    st.rerun()
                return

    st.metric("⭐ Puntos totales", st.session_state.my_score)

    name = st.session_state.my_name
    data = st.session_state.my_data
    pts_now = PISTAS_DEF[min(st.session_state.my_pistas-1, len(PISTAS_DEF)-1)][2]

    # Mostrar pistas
    st.markdown("### Pistas reveladas:")
    for i in range(st.session_state.my_pistas):
        if i < len(PISTAS_DEF):
            label, fn, pts = PISTAS_DEF[i]
            valor = fn(name, data)
            st.markdown(f"**{i+1}. {label}:** {valor}")

    if not st.session_state.my_answered:
        st.caption(f"💡 Si acertás ahora: **{pts_now} pts**")
        guess = st.text_input("¿Quién es?", key=f"my_input_{st.session_state.my_pistas}",
                              placeholder="Apellido del piloto...")

        col_ok, col_pista = st.columns(2)
        with col_ok:
            if st.button("✔ Responder", type="primary", use_container_width=True):
                if guess.strip():
                    _answer(guess)
                    st.rerun()
        with col_pista:
            if st.session_state.my_pistas < len(PISTAS_DEF):
                if st.button("🔍 Ver pista", use_container_width=True):
                    st.session_state.my_pistas += 1
                    st.rerun()
            else:
                if st.button("❌ Me rindo", use_container_width=True):
                    st.session_state.my_answered = True
                    st.session_state.my_last_result = (False, 0, name)
                    if st.session_state.my_daily:
                        mark_daily_played("mystery")
                    st.rerun()
    else:
        correct, pts, real_name = st.session_state.my_last_result
        if correct:
            st.success(f"🎯 ¡Correcto! Era **{real_name.title()}** · +{pts} pts")
        else:
            st.error(f"❌ Era **{real_name.title()}**")

        # Datos completos del piloto
        acad = f" · Academia: {data[6]}" if data[6] else ""
        st.info(f"🏎️ Equipos: {', '.join(t.title() for t in data[0][:3])} · "
                f"🏆 {'Campeón' if data[4] else 'Sin título'} · "
                f"🥇 {data[2]} victorias · 🥈 {data[3]} podios{acad}")

        if st.button("➡️ Siguiente piloto", type="primary"):
            for k in ["my_name", "my_data", "my_pistas", "my_answered", "my_last_result"]:
                if k in st.session_state:
                    del st.session_state[k]
            n, d = _pick_pilot()
            st.session_state.my_name = n
            st.session_state.my_data = d
            st.session_state.my_pistas = 1
            st.session_state.my_answered = False
            st.session_state.my_last_result = None
            st.rerun()
