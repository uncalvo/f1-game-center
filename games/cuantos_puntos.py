import streamlit as st
import random, datetime
from f1_data import daily_played, mark_daily_played

POINTS_DATA = [
    ("Michael Schumacher", 2004, 148, "Su mejor temporada: 13 victorias de 18 carreras."),
    ("Michael Schumacher", 2002, 144, "11 victorias, 5 segundos. Dominó de principio a fin."),
    ("Michael Schumacher", 2001, 123, "9 victorias con Ferrari, título con 4 carreras de antelación."),
    ("Michael Schumacher", 2000, 108, "Primer título con Ferrari, ganando al filo contra Häkkinen."),
    ("Michael Schumacher", 1994, 92, "Título polémico en la última vuelta de la última carrera."),
    ("Michael Schumacher", 1995, 102, "Dominó con Benetton-Renault, 9 victorias."),
    ("Michael Schumacher", 1996, 59, "3 victorias su primer año con Ferrari."),
    ("Michael Schumacher", 1998, 86, "Perdió el título ante Häkkinen en la última carrera."),
    ("Michael Schumacher", 1999, 44, "Se perdió la mitad de la temporada por fractura de pierna."),
    ("Michael Schumacher", 2003, 93, "6 victorias, título por apenas 2 puntos ante Räikkönen."),
    ("Michael Schumacher", 2006, 121, "7 victorias pero Alonso se llevó el título con Renault."),
    ("Ayrton Senna", 1988, 90, "15 de 16 carreras ganadas con McLaren-Honda."),
    ("Ayrton Senna", 1990, 78, "6 victorias, título ante Prost en Suzuka."),
    ("Ayrton Senna", 1991, 96, "7 victorias, último campeonato de Senna."),
    ("Ayrton Senna", 1989, 60, "Descalificado en Japón, perdió el título ante Prost."),
    ("Alain Prost", 1989, 76, "Prost venció a Senna en la batalla interna de McLaren."),
    ("Alain Prost", 1993, 99, "7 victorias con Williams, se retiró campeón."),
    ("Alain Prost", 1986, 72, "4 victorias, campeón con McLaren en la última carrera."),
    ("Alain Prost", 1988, 87, "7 victorias pero Senna le ganó el título ese año."),
    ("Nigel Mansell", 1992, 108, "9 victorias, dominó con el Williams FW14B activo."),
    ("Nigel Mansell", 1991, 72, "5 victorias, subcampeón ante Senna con Williams."),
    ("Damon Hill", 1996, 97, "8 victorias, campeón con Williams ante Schumacher."),
    ("Damon Hill", 1994, 91, "6 victorias, perdió el título en la última vuelta en Adelaida."),
    ("Mika Häkkinen", 1998, 100, "8 victorias, primer título con McLaren."),
    ("Mika Häkkinen", 1999, 76, "5 victorias, retuvo el título ante Irvine."),
    ("Mika Häkkinen", 2000, 89, "Peleó el título hasta el final con Schumacher."),
    ("Fernando Alonso", 2005, 133, "7 victorias, primer campeonato de Alonso con Renault."),
    ("Fernando Alonso", 2006, 134, "7 victorias, segundo título con Renault."),
    ("Kimi Räikkönen", 2007, 110, "Ganó el título en la última carrera con 1 punto de ventaja."),
    ("Lewis Hamilton", 2008, 98, "Primer título, ganado en la última curva de la última carrera."),
    ("Lewis Hamilton", 2007, 109, "Perdió el título en la última carrera por 1 punto."),
    ("Lewis Hamilton", 2010, 240, "4 victorias, perdió el título en la última carrera."),
    ("Lewis Hamilton", 2014, 384, "11 victorias con el Mercedes W05 dominante."),
    ("Lewis Hamilton", 2015, 381, "10 victorias, tercer título mundial."),
    ("Lewis Hamilton", 2017, 363, "9 victorias, cuarto título ante Vettel."),
    ("Lewis Hamilton", 2018, 408, "11 victorias, quinto título con récord de puntos."),
    ("Lewis Hamilton", 2019, 413, "11 victorias, sexto título."),
    ("Lewis Hamilton", 2020, 347, "11 victorias en 17 carreras, séptimo título."),
    ("Lewis Hamilton", 2016, 380, "10 victorias, subcampeón ante Rosberg."),
    ("Jenson Button", 2009, 95, "6 victorias con el revolucionario Brawn BGP 001."),
    ("Jenson Button", 2011, 270, "3 victorias, subcampeón con McLaren."),
    ("Nico Rosberg", 2016, 385, "9 victorias, campeón y retirado 5 días después."),
    ("Nico Rosberg", 2014, 317, "5 victorias, subcampeón ante Hamilton."),
    ("Nico Rosberg", 2015, 322, "6 victorias, subcampeón ante Hamilton."),
    ("Sebastian Vettel", 2010, 256, "5 victorias, campeón en la última carrera del año."),
    ("Sebastian Vettel", 2011, 392, "15 victorias, dominó de punta a punta con el RB7."),
    ("Sebastian Vettel", 2012, 281, "5 victorias, campeón en la última carrera ante Alonso."),
    ("Sebastian Vettel", 2013, 397, "13 victorias consecutivas al final de temporada."),
    ("Sebastian Vettel", 2014, 167, "Temporada frustrante con el nuevo Red Bull."),
    ("Sebastian Vettel", 2015, 278, "3 victorias en su primer año con Ferrari."),
    ("Sebastian Vettel", 2018, 320, "5 victorias, subcampeón ante Hamilton."),
    ("Max Verstappen", 2021, 395, "10 victorias, título decidido en la última vuelta."),
    ("Max Verstappen", 2022, 454, "15 victorias, nuevo récord de puntos en una temporada."),
    ("Max Verstappen", 2023, 575, "19 victorias de 22, récord absoluto de victorias."),
    ("Max Verstappen", 2024, 437, "9 victorias, cuarto título consecutivo."),
    ("Charles Leclerc", 2022, 308, "3 victorias, subcampeón con Ferrari."),
    ("Charles Leclerc", 2019, 264, "2 victorias, 4º en el campeonato con Ferrari."),
    ("Sergio Perez", 2022, 305, "2 victorias, tercero en el campeonato."),
    ("George Russell", 2022, 275, "1 victoria en Brasil, cuarto en el campeonato."),
    ("Carlos Sainz", 2023, 200, "2 victorias, subcampeón a 175 puntos de Verstappen."),
    ("Carlos Sainz", 2024, 290, "2 victorias, 5º en el campeonato."),
    ("Lando Norris", 2024, 374, "4 victorias, subcampeón ante Verstappen."),
    ("Fernando Alonso", 2023, 206, "3 podios en las primeras 4 carreras con Aston Martin."),
    ("Mark Webber", 2010, 242, "4 victorias, perdió el título ante Vettel en la última carrera."),
    ("Mark Webber", 2011, 258, "1 victoria, tercero en el campeonato."),
    ("Valtteri Bottas", 2019, 326, "4 victorias, segundo en el campeonato."),
    ("Valtteri Bottas", 2020, 223, "2 victorias, tercero con Mercedes."),
    ("Oscar Piastri", 2024, 292, "2 victorias, tercer puesto en su segundo año."),
    ("Lewis Hamilton", 2023, 234, "3 victorias, tercer puesto en el campeonato."),
]

MAX_INTENTOS = 5
PTS_TABLE = [500, 350, 200, 100, 50]
ROUNDS = 10

def init():
    if "pg_round" not in st.session_state:
        st.session_state.pg_round = 0
        st.session_state.pg_score = 0
        st.session_state.pg_correct = 0
        st.session_state.pg_used = set()
        st.session_state.pg_q = None
        st.session_state.pg_intentos = []
        st.session_state.pg_done = False
        st.session_state.pg_round_done = False
        st.session_state.pg_daily = False
        st.session_state.pg_last_result = None
        _next_question()

def _pick():
    pool = [i for i in range(len(POINTS_DATA)) if i not in st.session_state.pg_used]
    if not pool:
        st.session_state.pg_used = set()
        pool = list(range(len(POINTS_DATA)))
    if st.session_state.pg_daily:
        idx = (int(datetime.date.today().strftime("%Y%m%d")) + st.session_state.pg_round) % len(pool)
    else:
        idx = random.randrange(len(pool))
    chosen = pool[idx]
    st.session_state.pg_used.add(chosen)
    return POINTS_DATA[chosen]

def _next_question():
    if st.session_state.pg_round >= ROUNDS:
        st.session_state.pg_done = True
        if st.session_state.pg_daily:
            mark_daily_played("pointsguess")
        return
    st.session_state.pg_q = _pick()
    st.session_state.pg_intentos = []
    st.session_state.pg_round_done = False
    st.session_state.pg_last_result = None
    st.session_state.pg_round += 1

def _submit_guess(guess):
    if st.session_state.pg_round_done or not st.session_state.pg_q:
        return
    pilot, year, correct, info = st.session_state.pg_q
    intento_num = len(st.session_state.pg_intentos) + 1

    if guess == correct:
        pts = PTS_TABLE[intento_num - 1]
        st.session_state.pg_score += pts
        st.session_state.pg_correct += 1
        st.session_state.pg_intentos.append(("exact", guess, pts))
        st.session_state.pg_last_result = ("win", pts, info)
        st.session_state.pg_round_done = True
    elif guess < correct:
        st.session_state.pg_intentos.append(("low", guess, 0))
        if intento_num >= MAX_INTENTOS:
            st.session_state.pg_last_result = ("lose", correct, info)
            st.session_state.pg_round_done = True
    else:
        st.session_state.pg_intentos.append(("high", guess, 0))
        if intento_num >= MAX_INTENTOS:
            st.session_state.pg_last_result = ("lose", correct, info)
            st.session_state.pg_round_done = True

def render():
    init()
    st.markdown("## 🔢 ¿Cuántos Puntos?")
    st.caption("Adiviná los puntos del piloto en esa temporada · 10 rondas · 5 intentos")

    col1, col2 = st.columns([3, 1])
    with col2:
        daily = st.toggle("📅 Diario", key="pg_daily_tog", value=st.session_state.pg_daily)
        if daily != st.session_state.pg_daily:
            st.session_state.pg_daily = daily
            if daily and daily_played("pointsguess"):
                st.warning("🔒 Ya jugaste el modo diario hoy.")
                if st.button("🎮 Jugar libre"):
                    st.session_state.pg_daily = False
                    st.rerun()
                return

    if st.session_state.pg_done:
        pct = int(st.session_state.pg_correct / ROUNDS * 100)
        if pct >= 80: e, t = "🏆", "¡Cronista perfecto!"
        elif pct >= 50: e, t = "🥇", "¡Muy buen ojo!"
        elif pct >= 30: e, t = "🥈", "Bien, sigue practicando"
        else: e, t = "🤔", "Los puntos de F1 son complicados..."
        st.markdown(f"<div style='text-align:center;font-size:48px'>{e}</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center;color:#e10600'>{t}</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Exactos", f"{st.session_state.pg_correct}/{ROUNDS}")
        c2.metric("Puntuación", st.session_state.pg_score)
        if st.button("🔄 Jugar de nuevo"):
            for k in list(st.session_state.keys()):
                if k.startswith("pg_"):
                    del st.session_state[k]
            st.rerun()
        return

    # Progress bar
    st.progress((st.session_state.pg_round - 1) / ROUNDS,
                text=f"Ronda {st.session_state.pg_round}/{ROUNDS}  ·  🎯 Exactos: {st.session_state.pg_correct}  ·  ⭐ {st.session_state.pg_score} pts")

    pilot, year, correct, info = st.session_state.pg_q

    st.markdown(f"""
    <div style='background:#1a1a1a;border-left:4px solid #e10600;border-radius:8px;padding:16px;margin:12px 0'>
        <div style='font-size:20px;font-weight:bold'>🏎️ {pilot} &nbsp;·&nbsp; 📅 {year}</div>
        <div style='font-size:12px;color:#888;margin-top:6px'>
        💡 Puntos por intento: 1°→500 · 2°→350 · 3°→200 · 4°→100 · 5°→50
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Historial de intentos
    if st.session_state.pg_intentos:
        chips = []
        for state, val, _ in st.session_state.pg_intentos:
            if state == "exact":
                chips.append(f"<span style='background:#1b5e20;color:white;padding:3px 10px;border-radius:6px;margin:2px'>🎯 {val} ✓</span>")
            elif state == "low":
                chips.append(f"<span style='background:#1565c0;color:white;padding:3px 10px;border-radius:6px;margin:2px'>🔼 {val} → más</span>")
            else:
                chips.append(f"<span style='background:#b71c1c;color:white;padding:3px 10px;border-radius:6px;margin:2px'>🔽 {val} → menos</span>")
        st.markdown(" ".join(chips), unsafe_allow_html=True)

    if st.session_state.pg_round_done:
        result = st.session_state.pg_last_result
        if result[0] == "win":
            st.success(f"🎯 ¡Exacto! +{result[1]} pts — {result[2]}")
        else:
            st.error(f"❌ Eran **{result[1]}** puntos — {result[2]}")
        label = "🏁 Ver resultado" if st.session_state.pg_round >= ROUNDS else "➡️ Siguiente"
        if st.button(label, type="primary"):
            _next_question()
            st.rerun()
    else:
        intentos_left = MAX_INTENTOS - len(st.session_state.pg_intentos)
        # Feedback mensaje
        if st.session_state.pg_intentos:
            last = st.session_state.pg_intentos[-1]
            if last[0] == "low":
                st.info(f"🔼 MÁS de {last[1]}")
            elif last[0] == "high":
                st.warning(f"🔽 MENOS de {last[1]}")

        # Input con +/- buttons
        col_m10, col_m1, col_val, col_p1, col_p10, col_ok = st.columns([1,1,2,1,1,2])
        if "pg_guess" not in st.session_state:
            st.session_state.pg_guess = max(1, correct // 2)

        with col_m10:
            if st.button("-10", key="pg_m10"):
                st.session_state.pg_guess = max(0, st.session_state.pg_guess - 10); st.rerun()
        with col_m1:
            if st.button("-1", key="pg_m1"):
                st.session_state.pg_guess = max(0, st.session_state.pg_guess - 1); st.rerun()
        with col_val:
            guess = st.number_input("Puntos", min_value=0, max_value=700,
                                    value=st.session_state.pg_guess,
                                    key="pg_input", label_visibility="collapsed")
            st.session_state.pg_guess = guess
        with col_p1:
            if st.button("+1", key="pg_p1"):
                st.session_state.pg_guess = min(700, st.session_state.pg_guess + 1); st.rerun()
        with col_p10:
            if st.button("+10", key="pg_p10"):
                st.session_state.pg_guess = min(700, st.session_state.pg_guess + 10); st.rerun()
        with col_ok:
            if st.button(f"✔ Confirmar ({intentos_left} left)", type="primary", use_container_width=True):
                _submit_guess(st.session_state.pg_guess)
                st.rerun()
