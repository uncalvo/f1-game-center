import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

st.set_page_config(
    page_title="F1 Game Center",
    page_icon="🏎️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS global ───────────────────────────────────────────────────
st.markdown("""
<style>
    .main { max-width: 720px; margin: 0 auto; }
    div[data-testid="stMetricValue"] { font-size: 1.6rem; }
    div[data-testid="stButton"] button { border-radius: 8px; font-weight: bold; }
    .stTextInput input { border-radius: 8px; }
    .stSelectbox select { border-radius: 8px; }
    /* Header rojo F1 */
    h1, h2, h3 { color: #f0f0f0 !important; }
</style>
""", unsafe_allow_html=True)

GAMES = {
    "🏠 Inicio":              None,
    "🔲 Grid Challenge":      "grid",
    "🏆 Podium Challenge":    "podium",
    "⚔️ Duelo de Pilotos":   "duelo",
    "🏗️ Constructor":        "constructor",
    "📅 Línea de Tiempo":     "timeline",
    "🕵️ Piloto Misterioso":  "piloto_misterioso",
    "🔗 Cadena de Pilotos":   "cadena",
    "📊 Stats Extremas":      "stats_extremas",
    "⏱️ Adivina la Vuelta":  "adivina_vuelta",
    "🧩 F1 Wordle":           "wordle",
    "🔢 ¿Cuántos Puntos?":   "cuantos_puntos",
    "🗺️ ¿En qué Circuito?":  "circuito",
}

# ── Sidebar / selector ───────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏎️ F1 Game Center")
    st.divider()
    selection = st.radio(
        "Elegí un juego:",
        list(GAMES.keys()),
        key="nav_selection",
        label_visibility="collapsed",
    )

# ── Routing ──────────────────────────────────────────────────────
module_name = GAMES.get(selection)

if module_name is None:
    # Pantalla de inicio
    st.markdown("""
    <div style='text-align:center;padding:30px 0'>
        <div style='font-size:64px'>🏎️</div>
        <h1 style='color:#e10600 !important;font-size:2.5rem;margin:8px 0'>F1 Game Center</h1>
        <p style='color:#888;font-size:16px'>12 juegos de Fórmula 1 · Modo diario · Sin registro</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    games_list = [
        ("🔲", "Grid Challenge",      "Encontrá el piloto que cumple fila y columna"),
        ("🏆", "Podium Challenge",     "Adiviná el Top 10 de un GP histórico"),
        ("⚔️", "Duelo de Pilotos",    "¿Quién tiene más victorias, podios o títulos?"),
        ("🏗️", "Constructor",         "Encontrá la escudería que cumple ambas condiciones"),
        ("📅", "Línea de Tiempo",      "Ordená eventos de F1 cronológicamente"),
        ("🕵️", "Piloto Misterioso",   "Adiviná el piloto con pistas progresivas"),
        ("🔗", "Cadena de Pilotos",    "Conectá dos pilotos por compañeros de equipo"),
        ("📊", "Stats Extremas",       "Verdadero o Falso sobre récords de F1"),
        ("⏱️", "Adivina la Vuelta",   "Adiviná el tiempo de clasificación"),
        ("🧩", "F1 Wordle",            "Adiviná el apellido del piloto en 6 intentos"),
        ("🔢", "¿Cuántos Puntos?",    "Adiviná los puntos del piloto en esa temporada"),
        ("🗺️", "¿En qué Circuito?",   "Pistas progresivas para identificar el circuito"),
    ]

    cols = st.columns(2)
    for i, (icon, name, desc) in enumerate(games_list):
        with cols[i % 2]:
            st.markdown(f"""
            <div style='background:#1a1a1a;border:1px solid #333;border-radius:10px;
            padding:14px;margin:6px 0;cursor:pointer'>
                <div style='font-size:22px'>{icon}</div>
                <div style='font-weight:bold;color:#f0f0f0;margin:4px 0'>{name}</div>
                <div style='font-size:12px;color:#888'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.caption("← Usá el menú lateral para elegir un juego")

else:
    try:
        import importlib
        game_module = importlib.import_module(f"games.{module_name}")
        game_module.render()
    except Exception as e:
        st.error(f"Error cargando el juego: {e}")
        st.exception(e)
