import streamlit as st
import random, datetime
from f1_data import RAW_F1, daily_played, mark_daily_played

STATS = ["victorias", "podios", "campeonatos"]
STAT_LABELS = {
    "victorias":    ("Victorias",    "victorias en F1"),
    "podios":       ("Podios",       "podios en F1"),
    "campeonatos":  ("Campeonatos",  "campeonatos del mundo"),
}

def _get_val(name, stat):
    d = RAW_F1[name]
    if stat == "victorias":   return d[2]
    if stat == "podios":      return d[3]
    if stat == "campeonatos": return 1 if d[4] else 0
    return 0

def _pool():
    return [n for n, d in RAW_F1.items() if d[2] > 0 or d[3] > 0 or d[4]]

def _pick_pair(stat):
    pool = _pool()
    for _ in range(200):
        a, b = random.sample(pool, 2)
        va, vb = _get_val(a, stat), _get_val(b, stat)
        if va != vb:
            return a, b, va, vb
    return random.sample(pool, 2) + [0, 0]

def init():
    if "du_streak" not in st.session_state:
        st.session_state.du_streak = 0
        st.session_state.du_best = 0
        st.session_state.du_total = 0
        st.session_state.du_daily = False
        st.session_state.du_answered = False
        st.session_state.du_last_result = None
        _next_round()

def _next_round():
    stat = random.choice(STATS)
    a, b, va, vb = _pick_pair(stat)
    st.session_state.du_stat = stat
    st.session_state.du_a = a
    st.session_state.du_b = b
    st.session_state.du_va = va
    st.session_state.du_vb = vb
    st.session_state.du_answered = False
    st.session_state.du_last_result = None

def _answer(choice):
    if st.session_state.du_answered:
        return
    a = st.session_state.du_a
    b = st.session_state.du_b
    va = st.session_state.du_va
    vb = st.session_state.du_vb
    stat = st.session_state.du_stat

    correct = (choice == "A" and va > vb) or (choice == "B" and vb > va)
    if correct:
        st.session_state.du_streak += 1
        if st.session_state.du_streak > st.session_state.du_best:
            st.session_state.du_best = st.session_state.du_streak
        pts = 10 + (st.session_state.du_streak - 1) * 5
        st.session_state.du_total += pts
        st.session_state.du_last_result = ("win", pts, a, b, va, vb, stat)
    else:
        if st.session_state.du_daily:
            mark_daily_played("duel")
        st.session_state.du_streak = 0
        winner = a if va > vb else b
        wval = va if va > vb else vb
        st.session_state.du_last_result = ("lose", 0, a, b, va, vb, stat, winner, wval)
    st.session_state.du_answered = True

def _card_html(name, stat, val=None):
    label = STAT_LABELS[stat][0]
    val_str = f"{val}" if val is not None else "?"
    return f"""
    <div style='background:#1a1a1a;border:2px solid #333;border-radius:10px;
    padding:16px;text-align:center;min-height:100px'>
        <div style='font-size:18px;font-weight:bold;color:white'>{name.title()}</div>
        <div style='font-size:13px;color:#888;margin-top:4px'>{label}</div>
        <div style='font-size:28px;font-weight:bold;color:#e10600;margin-top:6px'>{val_str}</div>
    </div>
    """

def render():
    init()
    st.markdown("## ⚔️ Duelo de Pilotos")
    st.caption("¿Quién tiene más? · Racha infinita")

    col1, col2 = st.columns([3, 1])
    with col2:
        daily = st.toggle("📅 Diario", key="du_daily_tog", value=st.session_state.du_daily)
        if daily != st.session_state.du_daily:
            st.session_state.du_daily = daily
            if daily and daily_played("duel"):
                st.warning("🔒 Ya jugaste el duelo de hoy.")
                if st.button("🎮 Jugar libre"):
                    st.session_state.du_daily = False
                    st.rerun()
                return

    # Header stats
    c1, c2, c3 = st.columns(3)
    c1.metric("🔥 Racha", st.session_state.du_streak)
    c2.metric("🏅 Mejor", st.session_state.du_best)
    c3.metric("⭐ Pts", st.session_state.du_total)

    stat = st.session_state.du_stat
    a = st.session_state.du_a
    b = st.session_state.du_b
    label = STAT_LABELS[stat][1]

    st.markdown(f"<h3 style='text-align:center;color:#ffd700'>¿Quién tiene más <b>{label.upper()}</b>?</h3>",
                unsafe_allow_html=True)

    if not st.session_state.du_answered:
        col_a, col_vs, col_b = st.columns([5, 1, 5])
        with col_a:
            st.markdown(_card_html(a, stat), unsafe_allow_html=True)
            if st.button(f"◀ {a.title()}", use_container_width=True, type="primary"):
                _answer("A"); st.rerun()
        with col_vs:
            st.markdown("<div style='text-align:center;padding-top:40px;font-size:18px;color:#444'>VS</div>",
                        unsafe_allow_html=True)
        with col_b:
            st.markdown(_card_html(b, stat), unsafe_allow_html=True)
            if st.button(f"{b.title()} ▶", use_container_width=True):
                _answer("B"); st.rerun()
    else:
        result = st.session_state.du_last_result
        va = st.session_state.du_va
        vb = st.session_state.du_vb

        col_a, col_vs, col_b = st.columns([5, 1, 5])
        with col_a:
            st.markdown(_card_html(a, stat, va), unsafe_allow_html=True)
        with col_vs:
            st.markdown("<div style='text-align:center;padding-top:40px;font-size:18px;color:#444'>VS</div>",
                        unsafe_allow_html=True)
        with col_b:
            st.markdown(_card_html(b, stat, vb), unsafe_allow_html=True)

        if result[0] == "win":
            st.success(f"✅ ¡Correcto! +{result[1]} pts · Racha: {st.session_state.du_streak}")
            if st.button("➡️ Siguiente", type="primary", use_container_width=True):
                _next_round(); st.rerun()
        else:
            st.error(f"❌ Racha perdida · Ganaba **{result[7].title()}** con {result[8]}")
            if st.button("🔄 Intentar de nuevo", use_container_width=True):
                _next_round(); st.rerun()
