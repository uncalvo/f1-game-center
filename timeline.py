import streamlit as st
import random, datetime
from f1_data import F1_EVENTS, daily_played, mark_daily_played

DIFFS = {
    "🟢 Fácil":   (4, 1.0),
    "🟡 Medio":   (5, 1.5),
    "🔴 Difícil": (6, 2.0),
    "⚫ Experto": (7, 3.0),
}
ROUNDS = 10
CAT_ICONS = {
    "debut":     "🏁",
    "victoria":  "🏆",
    "reglamento":"📋",
    "record":    "📊",
    "tragedia":  "🖤",
    "equipo":    "🏗️",
}

def init():
    if "tl_round" not in st.session_state:
        st.session_state.tl_round = 0
        st.session_state.tl_score = 0
        st.session_state.tl_diff = "🟡 Medio"
        st.session_state.tl_used = set()
        st.session_state.tl_events = None
        st.session_state.tl_order = None       # orden del usuario
        st.session_state.tl_confirmed = False
        st.session_state.tl_done = False
        st.session_state.tl_daily = False

def _pick_events(n):
    pool = [i for i in range(len(F1_EVENTS)) if i not in st.session_state.tl_used]
    if len(pool) < n:
        st.session_state.tl_used = set()
        pool = list(range(len(F1_EVENTS)))
    chosen = random.sample(pool, n)
    for c in chosen:
        st.session_state.tl_used.add(c)
    events = [F1_EVENTS[i] for i in chosen]
    return events

def _new_round():
    n, _ = DIFFS[st.session_state.tl_diff]
    events = _pick_events(n)
    # Mezclar para mostrar
    shuffled = events[:]
    random.shuffle(shuffled)
    st.session_state.tl_events = shuffled
    st.session_state.tl_correct_order = sorted(events, key=lambda x: x[0])
    st.session_state.tl_order = list(range(len(shuffled)))
    st.session_state.tl_confirmed = False
    st.session_state.tl_round += 1

def render():
    init()
    st.markdown("## 📅 Línea de Tiempo")
    st.caption("Ordená los eventos de F1 cronológicamente · 10 rondas")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        diff = st.selectbox("Dificultad", list(DIFFS.keys()),
                            index=list(DIFFS.keys()).index(st.session_state.tl_diff),
                            key="tl_diff_sel", label_visibility="collapsed")
        if diff != st.session_state.tl_diff:
            st.session_state.tl_diff = diff
    with col3:
        daily = st.toggle("📅 Diario", key="tl_daily_tog", value=st.session_state.tl_daily)
        st.session_state.tl_daily = daily

    if st.session_state.tl_done:
        n, mult = DIFFS[st.session_state.tl_diff]
        max_pts = ROUNDS * (n * 20 + 50) * mult
        pct = int(st.session_state.tl_score / max_pts * 100) if max_pts > 0 else 0
        if pct >= 80: e, t = "🏆", "¡Historiador de F1!"
        elif pct >= 50: e, t = "🥇", "¡Muy bien!"
        elif pct >= 30: e, t = "🥈", "Bien, sigue practicando"
        else: e, t = "🤔", "¡La historia de F1 es larga!"
        st.markdown(f"<div style='text-align:center;font-size:48px'>{e}</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center;color:#e10600'>{t}</h3>", unsafe_allow_html=True)
        st.metric("Puntuación", f"{st.session_state.tl_score:.0f} / {max_pts:.0f}")
        if st.button("🔄 Jugar de nuevo"):
            for k in list(st.session_state.keys()):
                if k.startswith("tl_"):
                    del st.session_state[k]
            st.rerun()
        return

    # Iniciar primera ronda si no hay eventos
    if st.session_state.tl_events is None:
        _new_round()

    st.progress(max(0, st.session_state.tl_round - 1) / ROUNDS,
                text=f"Ronda {st.session_state.tl_round}/{ROUNDS}  ·  ⭐ {st.session_state.tl_score:.0f} pts")

    n, mult = DIFFS[st.session_state.tl_diff]
    events = st.session_state.tl_events

    if not st.session_state.tl_confirmed:
        st.markdown("**Ordená estos eventos del más antiguo al más reciente:**")
        st.caption("Usá los números para indicar el orden (1 = más antiguo)")

        # Mostrar eventos con selectbox para ordenar
        user_order = []
        used_positions = set()
        all_valid = True

        for i, ev in enumerate(events):
            cat = ev[2] if len(ev) > 2 else "evento"
            icon = CAT_ICONS.get(cat, "📌")
            st.markdown(f"**{icon} {ev[1]}**")
            pos = st.selectbox(
                f"Posición para evento {i+1}",
                options=list(range(1, len(events)+1)),
                key=f"tl_pos_{i}_{st.session_state.tl_round}",
                label_visibility="collapsed"
            )
            user_order.append((pos, i))

        if st.button("✔ Confirmar orden", type="primary", use_container_width=True):
            positions = [p for p, _ in user_order]
            if len(set(positions)) < len(positions):
                st.error("⚠️ No podés usar la misma posición dos veces")
            else:
                st.session_state.tl_confirmed = True
                st.session_state.tl_user_order = sorted(user_order, key=lambda x: x[0])
                st.rerun()
    else:
        # Mostrar resultado
        correct_order = st.session_state.tl_correct_order
        user_order = st.session_state.tl_user_order  # [(pos, original_idx), ...]
        user_events = [events[idx] for _, idx in user_order]

        hits = sum(1 for u, c in zip(user_events, correct_order) if u == c)
        perfect = hits == len(correct_order)
        n_ev = len(correct_order)
        pts = (hits * 20 + (50 if perfect else 0)) * mult
        st.session_state.tl_score += pts

        if perfect:
            st.success(f"🏆 ¡Perfecto! +{pts:.0f} pts")
        else:
            st.warning(f"👍 {hits}/{n_ev} correctos · +{pts:.0f} pts")

        st.markdown("**Orden correcto:**")
        for ev in correct_order:
            cat = ev[2] if len(ev) > 2 else ""
            icon = CAT_ICONS.get(cat, "📌")
            st.markdown(f"📅 **{ev[0]}** — {icon} {ev[1]}")

        if st.session_state.tl_round >= ROUNDS:
            if st.session_state.tl_daily:
                mark_daily_played("timeline")
                st.session_state.tl_done = True
            if st.button("🏁 Ver resultado final"):
                st.session_state.tl_done = True
                st.rerun()
        else:
            if st.button("➡️ Siguiente ronda", type="primary"):
                _new_round()
                st.rerun()
