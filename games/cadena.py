import streamlit as st
import random
from collections import deque
from f1_data import RAW_F1, _CHAIN_GRAPH, _CHAIN_TEAM_GRAPH, daily_played, mark_daily_played

MAX_STEPS = 15

def _bfs_path(start, end):
    if start == end:
        return [start]
    visited = {start}
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        for neighbor in _CHAIN_GRAPH.get(node, set()):
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path
                visited.add(neighbor)
                queue.append(new_path)
    return None

def _pick_pair():
    pool = sorted(_CHAIN_GRAPH.keys())
    for _ in range(100):
        start, end = random.sample(pool, 2)
        path = _bfs_path(start, end)
        if path and 2 <= len(path) - 1 <= 6:
            return start, end, len(path) - 1
    return random.sample(pool, 2) + [3]

def _shared_teams(a, b):
    ta = set(RAW_F1.get(a, ([],))[0])
    tb = set(RAW_F1.get(b, ([],))[0])
    return ta & tb

def init():
    if "ch_start" not in st.session_state:
        st.session_state.ch_daily = False
        st.session_state.ch_score = 0
        start, end, opt = _pick_pair()
        st.session_state.ch_start = start
        st.session_state.ch_end   = end
        st.session_state.ch_optimal = opt
        st.session_state.ch_chain = [start]
        st.session_state.ch_steps_left = MAX_STEPS
        st.session_state.ch_solved = False
        st.session_state.ch_failed = False

def _add_link(pilot):
    if st.session_state.ch_solved or st.session_state.ch_failed:
        return
    chain = st.session_state.ch_chain
    prev = chain[-1]

    # Verificar que son compañeros de equipo reales
    shared = _shared_teams(prev, pilot)
    if not shared:
        st.session_state.ch_link_error = f"❌ {prev.title()} y {pilot.title()} nunca fueron compañeros de equipo"
        return

    if pilot in chain:
        st.session_state.ch_link_error = f"⚠️ {pilot.title()} ya está en la cadena"
        return

    st.session_state.ch_link_error = None
    chain.append(pilot)
    st.session_state.ch_steps_left -= 1

    if pilot == st.session_state.ch_end:
        hops = len(chain) - 1
        optimal = st.session_state.ch_optimal
        base = 200
        bonus = max(0, optimal - hops + 1) * 100
        pts = base + bonus
        st.session_state.ch_score += pts
        st.session_state.ch_solved = True
        st.session_state.ch_pts_earned = pts
        if st.session_state.ch_daily:
            mark_daily_played("chain")
    elif st.session_state.ch_steps_left <= 0:
        st.session_state.ch_failed = True
        if st.session_state.ch_daily:
            mark_daily_played("chain")

def render():
    init()
    st.markdown("## 🔗 Cadena de Pilotos")
    st.caption("Conectá dos pilotos a través de compañeros de equipo reales")

    col1, col2 = st.columns([3, 1])
    with col2:
        daily = st.toggle("📅 Diario", key="ch_daily_tog", value=st.session_state.ch_daily)
        if daily != st.session_state.ch_daily:
            st.session_state.ch_daily = daily
            if daily and daily_played("chain"):
                st.warning("🔒 Ya jugaste la cadena de hoy.")
                if st.button("🎮 Jugar libre"):
                    st.session_state.ch_daily = False
                    st.rerun()
                return

    start = st.session_state.ch_start
    end   = st.session_state.ch_end
    chain = st.session_state.ch_chain
    optimal = st.session_state.ch_optimal

    st.markdown(f"""
    <div style='background:#1a1a1a;border-radius:8px;padding:12px;text-align:center;margin:12px 0'>
        <span style='font-size:18px;color:#e10600;font-weight:bold'>{start.title()}</span>
        <span style='color:#888;margin:0 12px'>→→→</span>
        <span style='font-size:18px;color:#ffd700;font-weight:bold'>{end.title()}</span>
        <br><span style='font-size:12px;color:#555'>Camino óptimo: {optimal} pasos</span>
    </div>
    """, unsafe_allow_html=True)

    # Cadena actual
    st.markdown("**Cadena actual:**")
    chain_display = " → ".join(p.title() for p in chain)
    st.markdown(f"<div style='font-size:16px;padding:8px;background:#111;border-radius:6px'>{chain_display}</div>",
                unsafe_allow_html=True)

    col_steps, col_score = st.columns(2)
    col_steps.metric("Pasos restantes", st.session_state.ch_steps_left)
    col_score.metric("⭐ Puntos", st.session_state.ch_score)

    if st.session_state.ch_solved:
        pts = st.session_state.ch_pts_earned
        hops = len(chain) - 1
        st.success(f"🎉 ¡Cadena completa! {hops} pasos · +{pts} pts")
        if st.button("🆕 Nueva cadena", type="primary"):
            for k in list(st.session_state.keys()):
                if k.startswith("ch_") and k != "ch_score" and k != "ch_daily":
                    del st.session_state[k]
            start2, end2, opt2 = _pick_pair()
            st.session_state.ch_start   = start2
            st.session_state.ch_end     = end2
            st.session_state.ch_optimal = opt2
            st.session_state.ch_chain   = [start2]
            st.session_state.ch_steps_left = MAX_STEPS
            st.session_state.ch_solved  = False
            st.session_state.ch_failed  = False
            st.rerun()
        return

    if st.session_state.ch_failed:
        st.error(f"❌ Sin pasos restantes. El camino óptimo era {optimal} pasos.")
        path = _bfs_path(start, end)
        if path:
            st.info("Ruta más corta: " + " → ".join(p.title() for p in path))
        if st.button("🆕 Nueva cadena"):
            for k in list(st.session_state.keys()):
                if k.startswith("ch_") and k != "ch_score" and k != "ch_daily":
                    del st.session_state[k]
            start2, end2, opt2 = _pick_pair()
            st.session_state.ch_start   = start2
            st.session_state.ch_end     = end2
            st.session_state.ch_optimal = opt2
            st.session_state.ch_chain   = [start2]
            st.session_state.ch_steps_left = MAX_STEPS
            st.session_state.ch_solved  = False
            st.session_state.ch_failed  = False
            st.rerun()
        return

    # Error de link
    if st.session_state.get("ch_link_error"):
        st.error(st.session_state.ch_link_error)

    # Compañeros disponibles del último piloto
    current = chain[-1]
    neighbors = sorted(
        [n for n in _CHAIN_GRAPH.get(current, set()) if n not in chain],
        key=lambda x: x.title()
    )

    st.caption(f"Compañeros de **{current.title()}**: {len(neighbors)} disponibles")
    pilot_choice = st.selectbox(
        "Elegí el siguiente eslabón",
        options=[""] + [p.title() for p in neighbors],
        key=f"ch_sel_{len(chain)}",
        label_visibility="collapsed"
    )

    if st.button("➕ Agregar eslabón", type="primary", use_container_width=True):
        if pilot_choice:
            _add_link(pilot_choice.lower())
            st.rerun()
        else:
            st.warning("Elegí un piloto primero")
