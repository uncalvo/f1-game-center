import streamlit as st
import random, datetime
from f1_data import daily_played, mark_daily_played

QUALY_DATA = [
    ("Michael Schumacher", "Spa-Francorchamps", 2004, "1:55.515", "Pole", "Récord de la era V10 en Spa"),
    ("Ayrton Senna", "Mónaco", 1990, "1:21.314", "Pole", "Senna dominó Mónaco en qualy"),
    ("Ayrton Senna", "Mónaco", 1988, "1:23.998", "Pole", "1.4 segundos por delante del segundo"),
    ("Lewis Hamilton", "Silverstone", 2020, "1:24.303", "Pole", "Récord histórico de Silverstone"),
    ("Lewis Hamilton", "Spa-Francorchamps", 2020, "1:41.252", "Pole", "Hamilton dominó Spa en 2020"),
    ("Max Verstappen", "Silverstone", 2021, "1:26.134", "Pole", "Pole en Silverstone el año del título"),
    ("Max Verstappen", "Abu Dhabi", 2021, "1:22.109", "Pole", "Pole en la carrera que le dio el primer título"),
    ("Lewis Hamilton", "Hungría", 2020, "1:13.447", "Pole", "Récord del Hungaroring con Hamilton"),
    ("Charles Leclerc", "Mónaco", 2022, "1:11.376", "Pole", "Leclerc lideró toda la qualy en casa"),
    ("Nico Rosberg", "Mónaco", 2016, "1:13.622", "Pole", "Último año de Rosberg en F1"),
    ("Lewis Hamilton", "Japón", 2015, "1:32.584", "Pole", "Hamilton en Suzuka camino al tercer título"),
    ("Sebastian Vettel", "Bahréin", 2010, "1:54.101", "Pole", "Vettel arrasó en Bahréin en el año del primer título"),
    ("Lewis Hamilton", "Italia", 2019, "1:19.307", "Pole", "Récord de Monza con el W10"),
    ("Valtteri Bottas", "Baku", 2019, "1:40.495", "Pole", "Bottas voló en las calles de Bakú"),
    ("Max Verstappen", "Países Bajos", 2021, "1:08.885", "Pole", "Zandvoort de regreso al calendario"),
    ("Sebastian Vettel", "Italia", 2008, "1:37.555", "Pole", "Primera pole de Vettel en F1"),
    ("Lewis Hamilton", "EE.UU.", 2012, "1:34.803", "Pole", "Hamilton en COTA en el primer GP de EE.UU. moderno"),
    ("Lewis Hamilton", "Mónaco", 2017, "1:12.178", "Pole", "Hamilton en Mónaco en la temporada del cuarto título"),
    ("Kimi Räikkönen", "Turquía", 2005, "1:26.797", "Pole", "Räikkönen volando en Estambul"),
    ("Fernando Alonso", "Italia", 2010, "1:21.962", "Pole", "Alonso pole en Monza con Ferrari"),
    ("Max Verstappen", "Emilia Romaña", 2021, "1:14.411", "Pole", "Pole en Imola en el año del primer título"),
    ("Lewis Hamilton", "Rusia", 2018, "1:31.387", "Pole", "Hamilton pole en Sochi en el año del quinto título"),
    ("Lewis Hamilton", "COTA", 2017, "1:33.108", "Pole", "Hamilton en Austin bajo presión"),
    ("Max Verstappen", "Hungría", 2022, "1:17.377", "Pole", "A décimas de Russell en la pole"),
    ("Valtteri Bottas", "Mugello", 2020, "1:13.609", "Pole", "GP de la Toscana, circuito nuevo"),
    ("Lewis Hamilton", "Abu Dhabi", 2020, "1:22.006", "Pole", "Última pole de 2020 para Hamilton"),
    ("Ayrton Senna", "San Marino", 1994, "1:21.548", "Pole", "Última pole de Senna antes de su trágico accidente"),
    ("Michael Schumacher", "Japón", 2000, "1:35.825", "Pole", "Pole en Suzuka camino al primer título con Ferrari"),
    ("Fernando Alonso", "Bahréin", 2005, "1:29.487", "Pole", "Primera pole del año campeón con Renault"),
    ("Fernando Alonso", "Hungría", 2006, "1:19.599", "Pole", "Alonso en su mejor forma con Renault"),
    ("Lewis Hamilton", "Hungría", 2012, "1:20.953", "Pole", "Hamilton con McLaren en la era de pelea con Vettel"),
    ("Lewis Hamilton", "Bélgica", 2017, "1:42.553", "Pole", "Dominó Spa en su camino al cuarto título"),
    ("Lewis Hamilton", "Japón", 2019, "1:27.064", "Pole", "Pole en Suzuka en el año de su sexto título"),
    ("Lewis Hamilton", "Mónaco", 2019, "1:10.166", "Pole", "Pole record en el circuito urbano más famoso"),
    ("Lewis Hamilton", "Brasil", 2021, "1:07.934", "Pole", "Pole en la Sprint, luego penalizado al fondo"),
    ("Sebastian Vettel", "Mónaco", 2011, "1:13.556", "Pole", "Vettel dominó Mónaco en su temporada perfecta"),
    ("Sebastian Vettel", "Italia", 2011, "1:22.275", "Pole", "Pole en Monza en el año de 15 victorias"),
    ("Sebastian Vettel", "Japón", 2013, "1:30.915", "Pole", "Pole en Suzuka en la temporada de 13 victorias seguidas"),
    ("Sebastian Vettel", "Abu Dhabi", 2010, "1:39.394", "Pole", "Pole en la carrera donde ganó su primer título"),
    ("Nico Rosberg", "Mónaco", 2015, "1:15.098", "Pole", "Rosberg dominó Mónaco con Mercedes"),
    ("Nico Rosberg", "Australia", 2016, "1:23.837", "Pole", "Pole en Melbourne en el año de su único título"),
    ("Max Verstappen", "Mónaco", 2021, "1:10.346", "Pole", "Verstappen arrebató la pole a Leclerc en Q3"),
    ("Max Verstappen", "Brasil", 2022, "1:11.556", "Pole", "Pole en la Sprint del GP de Brasil"),
    ("Max Verstappen", "Japón", 2022, "1:29.304", "Pole", "Pole en Suzuka en el año del dominio total"),
    ("Max Verstappen", "Bahréin", 2023, "1:29.708", "Pole", "Pole en la carrera inaugural de su temporada récord"),
    ("Max Verstappen", "Silverstone", 2023, "1:26.720", "Pole", "Pole en Silverstone en la temporada de 19 victorias"),
    ("Charles Leclerc", "Bahréin", 2022, "1:29.402", "Pole", "Leclerc inició 2022 dominando con el Ferrari F1-75"),
    ("Charles Leclerc", "Australia", 2022, "1:17.868", "Pole", "Leclerc lideró el campeonato con Ferrari"),
    ("Charles Leclerc", "Italia", 2019, "1:19.307", "Pole", "Primera pole y victoria de Leclerc con Ferrari"),
    ("George Russell", "Brasil", 2022, "1:11.556", "Pole", "Primera pole de Russell con Mercedes"),
    ("Lando Norris", "Miami", 2024, "1:27.241", "Pole", "Primera pole de Norris en F1"),
    ("Lando Norris", "Países Bajos", 2024, "1:09.673", "Pole", "Pole en Zandvoort en su gran temporada"),
    ("Carlos Sainz", "Singapur", 2023, "1:30.984", "Pole", "Primera pole de Sainz, ganó la carrera"),
    ("Nigel Mansell", "Brasil", 1992, "1:15.703", "Pole", "Mansell arrasó en 1992 con el Williams FW14B activo"),
    ("Mika Häkkinen", "Japón", 1998, "1:36.293", "Pole", "Häkkinen pole en Suzuka en el año de su primer título"),
    ("Jenson Button", "Australia", 2009, "1:26.202", "Pole", "Button dominó con el revolucionario Brawn BGP001"),
    ("Felipe Massa", "Bahréin", 2008, "1:32.994", "Pole", "Massa brilló en la temporada que casi le da el título"),
    ("Valtteri Bottas", "Abu Dhabi", 2017, "1:34.231", "Pole", "Bottas finalizó 2017 con una pole"),
    ("Sergio Pérez", "Arabia Saudí", 2021, "1:27.712", "Pole", "Primera pole en F1 de Checo Pérez"),
    ("Oscar Piastri", "Azerbaiyán", 2024, "1:41.365", "Pole", "Primera pole de Oscar Piastri en F1"),
]

ROUNDS = 10
PTS_TABLE = {50: 500, 200: 400, 500: 300, 1000: 200, 2000: 100}

def _parse_time(t):
    """Convierte '1:23.456' a milisegundos."""
    mins, rest = t.split(":")
    secs, ms = rest.split(".")
    return int(mins)*60000 + int(secs)*1000 + int(ms)

def _calc_pts(guess_ms, correct_ms):
    diff = abs(guess_ms - correct_ms)
    if diff <= 50: return 500
    if diff <= 200: return 400
    if diff <= 500: return 300
    if diff <= 1000: return 200
    if diff <= 2000: return 100
    return 0

def _pick():
    pool = [i for i in range(len(QUALY_DATA)) if i not in st.session_state.qt_used]
    if not pool:
        st.session_state.qt_used = set()
        pool = list(range(len(QUALY_DATA)))
    if st.session_state.qt_daily:
        idx = (int(datetime.date.today().strftime("%Y%m%d")) + st.session_state.qt_round) % len(pool)
    else:
        idx = random.randrange(len(pool))
    chosen = pool[idx]
    st.session_state.qt_used.add(chosen)
    return QUALY_DATA[chosen]

def init():
    if "qt_round" not in st.session_state:
        st.session_state.qt_round = 0
        st.session_state.qt_score = 0
        st.session_state.qt_correct = 0
        st.session_state.qt_used = set()
        st.session_state.qt_q = None
        st.session_state.qt_done = False
        st.session_state.qt_round_done = False
        st.session_state.qt_daily = False
        st.session_state.qt_last_result = None
        st.session_state.qt_min = 1
        st.session_state.qt_sec = 20
        st.session_state.qt_ms = 0
        _next_question()

def _next_question():
    if st.session_state.qt_round >= ROUNDS:
        st.session_state.qt_done = True
        if st.session_state.qt_daily:
            mark_daily_played("qualytime")
        return
    st.session_state.qt_q = _pick()
    st.session_state.qt_round_done = False
    st.session_state.qt_last_result = None
    st.session_state.qt_round += 1
    # Reset spinners
    st.session_state.qt_min = 1
    st.session_state.qt_sec = 20
    st.session_state.qt_ms = 0

def render():
    init()
    st.markdown("## ⏱️ Adivina la Vuelta")
    st.caption("Adiviná el tiempo de clasificación · 10 rondas")

    col1, col2 = st.columns([3, 1])
    with col2:
        daily = st.toggle("📅 Diario", key="qt_daily_tog", value=st.session_state.qt_daily)
        if daily != st.session_state.qt_daily:
            st.session_state.qt_daily = daily
            if daily and daily_played("qualytime"):
                st.warning("🔒 Ya jugaste el modo diario hoy.")
                if st.button("🎮 Jugar libre"):
                    st.session_state.qt_daily = False
                    st.rerun()
                return

    if st.session_state.qt_done:
        pct = int(st.session_state.qt_correct / ROUNDS * 100)
        if pct >= 80: e, t = "🏆", "¡Cronómetro humano!"
        elif pct >= 50: e, t = "🥇", "¡Muy buen ojo!"
        elif pct >= 30: e, t = "🥈", "Bien, sigue practicando"
        else: e, t = "🤔", "Los tiempos de F1 son difíciles..."
        st.markdown(f"<div style='text-align:center;font-size:48px'>{e}</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center;color:#e10600'>{t}</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("Precisos (±2s)", f"{st.session_state.qt_correct}/{ROUNDS}")
        c2.metric("Puntuación", st.session_state.qt_score)
        if st.button("🔄 Jugar de nuevo"):
            for k in list(st.session_state.keys()):
                if k.startswith("qt_"):
                    del st.session_state[k]
            st.rerun()
        return

    st.progress((st.session_state.qt_round - 1) / ROUNDS,
                text=f"Ronda {st.session_state.qt_round}/{ROUNDS}  ·  ⭐ {st.session_state.qt_score} pts")

    pilot, circuit, year, correct_t, pos, info = st.session_state.qt_q

    st.markdown(f"""
    <div style='background:#1a1a1a;border-left:4px solid #e10600;border-radius:8px;padding:16px;margin:12px 0'>
        <div style='font-size:20px;font-weight:bold'>🏎️ {pilot}</div>
        <div style='font-size:16px;color:#aaa'>🗺️ {circuit} &nbsp;·&nbsp; 📅 {year} &nbsp;·&nbsp; {pos}</div>
        <div style='font-size:12px;color:#666;margin-top:6px'>
        ±50ms→500pts · ±200ms→400 · ±500ms→300 · ±1s→200 · ±2s→100
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.qt_round_done:
        result = st.session_state.qt_last_result
        pts, correct_time, diff_ms = result
        if pts >= 300:
            st.success(f"🎯 +{pts} pts — diferencia: {diff_ms}ms — Tiempo real: **{correct_time}**")
        elif pts > 0:
            st.warning(f"👍 +{pts} pts — diferencia: {diff_ms}ms — Tiempo real: **{correct_time}**")
        else:
            st.error(f"❌ +0 pts — diferencia: {diff_ms}ms — Tiempo real: **{correct_time}**")
        st.info(f"💡 {info}")
        label = "🏁 Ver resultado" if st.session_state.qt_round >= ROUNDS else "➡️ Siguiente"
        if st.button(label, type="primary"):
            _next_question()
            st.rerun()
    else:
        col_m, col_s, col_ms = st.columns(3)
        with col_m:
            st.caption("MIN")
            mins = st.number_input("min", 0, 3, st.session_state.qt_min,
                                   key="qt_min_inp", label_visibility="collapsed")
            st.session_state.qt_min = mins
        with col_s:
            st.caption("SEG")
            secs = st.number_input("seg", 0, 59, st.session_state.qt_sec,
                                   key="qt_sec_inp", label_visibility="collapsed")
            st.session_state.qt_sec = secs
        with col_ms:
            st.caption("MS")
            ms = st.number_input("ms", 0, 999, st.session_state.qt_ms,
                                 key="qt_ms_inp", label_visibility="collapsed")
            st.session_state.qt_ms = ms

        preview = f"{mins}:{secs:02d}.{ms:03d}"
        st.markdown(f"<div style='text-align:center;font-size:22px;color:#e10600;font-weight:bold'>⏱ {preview}</div>",
                    unsafe_allow_html=True)

        if st.button("✔ Confirmar", type="primary", use_container_width=True):
            guess_ms = mins*60000 + secs*1000 + ms
            correct_ms = _parse_time(correct_t)
            diff = abs(guess_ms - correct_ms)
            pts = _calc_pts(guess_ms, correct_ms)
            st.session_state.qt_score += pts
            if pts > 0:
                st.session_state.qt_correct += 1
            st.session_state.qt_last_result = (pts, correct_t, diff)
            st.session_state.qt_round_done = True
            st.rerun()
