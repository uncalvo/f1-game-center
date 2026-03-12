import streamlit as st
import random
from f1_data import daily_played, mark_daily_played

STATEMENTS = [
    ("Michael Schumacher ganó 7 Campeonatos del Mundo de F1.", True,
     "Schumacher tiene 7 títulos: 1994, 1995 y 2000–2004."),
    ("Lewis Hamilton tiene más victorias en F1 que Michael Schumacher.", True,
     "Hamilton tiene 105 victorias, Schumacher tuvo 91."),
    ("Ayrton Senna nunca ganó el Campeonato del Mundo de F1.", False,
     "Senna ganó 3 títulos mundiales: 1988, 1990 y 1991."),
    ("El Gran Premio de Mónaco es el más lento del calendario de F1.", True,
     "Con una velocidad promedio de ~161 km/h, Mónaco es el más lento del calendario."),
    ("Max Verstappen ganó 4 títulos mundiales consecutivos (2021-2024).", True,
     "Verstappen ganó en 2021, 2022, 2023 y 2024 con Red Bull Racing."),
    ("Ferrari ha ganado más Campeonatos de Constructores que cualquier otro equipo.", False,
     "Mercedes tiene 8 títulos de constructores (2014-2021), Ferrari tiene 16."),
    ("El circuito de Monza es conocido como el Templo de la Velocidad.", True,
     "Monza, en Italia, es famoso por su alta velocidad promedio, de ahí su apodo."),
    ("Fernando Alonso ganó sus dos títulos mundiales con McLaren.", False,
     "Alonso ganó sus dos títulos con Renault, en 2005 y 2006."),
    ("El DRS (Drag Reduction System) se introdujo en F1 en 2011.", True,
     "El DRS se usó por primera vez en 2011 para facilitar los adelantamientos."),
    ("Sebastian Vettel ganó 4 títulos mundiales consecutivos.", True,
     "Vettel ganó con Red Bull en 2010, 2011, 2012 y 2013."),
    ("El motor de F1 más poderoso de la historia fue el BMW en 2005.", False,
     "El BMW P84/5 de 2005 generaba ~900 CV. Los motores turbo de los 80s llegaban a ~1500 CV en clasificación."),
    ("Kimi Räikkönen ganó el título mundial en 2007.", True,
     "Räikkönen ganó su único título en 2007, su primer año con Ferrari."),
    ("El Gran Premio de Bélgica se disputa en el circuito de Spa-Francorchamps.", True,
     "Spa-Francorchamps, con 7 km, es el circuito más largo del calendario moderno."),
    ("Nico Rosberg ganó el título mundial y se retiró pocos días después.", True,
     "Rosberg anunció su retiro apenas 5 días después de ganar el título en 2016."),
    ("El récord de velocidad punta en F1 es de más de 370 km/h.", True,
     "Valtteri Bottas registró 372.5 km/h en Monza 2016, el récord oficial en carrera."),
    ("Jenson Button ganó el título mundial de 2009.", True,
     "Button ganó con Brawn GP, el equipo que surgió de Honda, en 2009."),
    ("Lewis Hamilton ganó todos sus títulos con Mercedes.", False,
     "Hamilton ganó su primer título en 2008 con McLaren. Los otros 6 con Mercedes."),
    ("El Gran Premio más antiguo en el calendario actual es el de Gran Bretaña.", True,
     "El GP de Gran Bretaña se disputa desde 1950, el primer año del Campeonato del Mundo."),
    ("En F1 moderna, el motor máximo son 8 cilindros.", False,
     "Desde 2014, los motores de F1 son V6 turbo híbridos de 1.6L, no V8."),
    ("La vuelta más rápida en clasificación de la historia de F1 fue de Verstappen.", False,
     "Lewis Hamilton tiene la vuelta más rápida en clasificación registrada con 1:10.166 en Mónaco 2019."),
    ("Mick Schumacher, hijo de Michael, compitió en F1.", True,
     "Mick Schumacher corrió con Haas en 2021 y 2022."),
    ("El Halo fue introducido en F1 en 2018.", True,
     "El Halo, dispositivo de protección de la cabeza, es obligatorio desde 2018."),
    ("Ferrari es el único equipo que ha participado en todas las temporadas de F1.", True,
     "Ferrari ha estado en F1 desde la primera temporada en 1950, sin interrupciones."),
    ("El Gran Premio de Singapur fue el primer GP nocturno de la historia.", True,
     "El GP de Singapur 2008 fue el primero en disputarse de noche bajo iluminación artificial."),
    ("Alain Prost ganó 4 Campeonatos del Mundo de F1.", True,
     "Prost ganó en 1985, 1986, 1989 y 1993, siendo el campeón más exitoso de su era."),
    ("Nigel Mansell ganó el título de 1992 con el Williams FW14B activo.", True,
     "El FW14B con suspensión activa fue dominante. Mansell logró 9 victorias ese año."),
    ("El récord de poles en una temporada lo tiene Max Verstappen.", False,
     "Nigel Mansell tiene el récord con 14 poles en 1992. Verstappen tiene 9 en una temporada."),
    ("En F1 se usan neumáticos slick (sin ranuras) en condiciones secas desde 2009.", True,
     "Los slicks volvieron en 2009 tras años con neumáticos ranurados (1998-2008)."),
    ("Carlos Sainz ganó su primera carrera en el GP de Gran Bretaña 2022.", True,
     "Sainz ganó en Silverstone 2022, su primera victoria en F1 con Ferrari."),
    ("Lando Norris ganó su primera carrera en el GP de Miami 2024.", True,
     "Norris ganó en Miami 2024, su primera victoria tras años de carreras cercanas."),
    ("El equipo Brawn GP existió solo durante una temporada.", True,
     "Brawn GP ganó el campeonato en 2009 y fue vendido a Mercedes ese mismo año."),
    ("Ayrton Senna y Alain Prost fueron compañeros en McLaren.", True,
     "Compartieron equipo en 1988 y 1989 en una rivalidad histórica."),
    ("Damon Hill es hijo de otro campeón del mundo de F1.", True,
     "Graham Hill fue campeón en 1962 y 1968. Damon ganó en 1996."),
    ("El GP de Australia se disputó siempre en Melbourne.", False,
     "El GP de Australia se corrió en Adelaida de 1985 a 1995, luego en Melbourne."),
    ("El motor de un F1 moderno gira a más de 15.000 RPM.", True,
     "Los motores híbridos de F1 tienen un límite de 15.000 RPM."),
    ("Ayrton Senna ganó 3 Campeonatos del Mundo de F1.", True,
     "Senna ganó en 1988, 1990 y 1991, todos con McLaren-Honda."),
    ("Max Verstappen fue el campeón más joven de F1.", False,
     "Sebastian Vettel fue el más joven con 23 años en 2010. Verstappen tenía 24."),
    ("El motor V10 fue el estándar en F1 durante los años 90.", True,
     "Los motores V10 dominaron F1 desde 1989 hasta 2005."),
    ("Fernando Alonso ganó sus dos títulos con Renault.", True,
     "Alonso fue campeón en 2005 y 2006, ambas veces con Renault."),
    ("Kimi Räikkönen ganó el título siendo su única temporada con Ferrari.", False,
     "Räikkönen estuvo en Ferrari de 2007 a 2009, y volvió de 2014 a 2018."),
    ("El circuito de Spa-Francorchamps es el más largo del calendario actual.", True,
     "Spa tiene 7.004 km, siendo el más largo del calendario moderno de F1."),
    ("Sebastian Vettel ganó 4 títulos consecutivos con Red Bull.", True,
     "Vettel ganó en 2010, 2011, 2012 y 2013, todos con Red Bull Racing."),
    ("George Russell ganó su primera carrera de F1 en el GP de Brasil 2022.", True,
     "Russell ganó en Brasil 2022 con Mercedes, su primera victoria."),
    ("Sergio Pérez ganó su primera victoria con Racing Point.", True,
     "Pérez ganó el GP de Sakhir 2020 con Racing Point, su primera victoria."),
    ("El récord de victorias en una temporada es de Verstappen con 19 en 2023.", True,
     "Verstappen ganó 19 de 22 carreras en 2023, un récord absoluto."),
    ("Jenson Button ganó el título con Brawn GP, surgido de las cenizas de Honda.", True,
     "Honda abandonó F1 en 2008. Ross Brawn compró el equipo y ganó el título en 2009."),
    ("Gilles Villeneuve murió en un accidente durante la clasificación en Zolder.", True,
     "Gilles Villeneuve murió en el GP de Bélgica 1982 durante la clasificación."),
    ("Lewis Hamilton ganó su primer título en la última curva de la última carrera.", True,
     "En 2008, Hamilton pasó a Timo Glock en la última curva de la última carrera."),
    ("La escudería Williams ganó 7 títulos de constructores.", True,
     "Williams ganó en 1980, 1981, 1986, 1987, 1992, 1993 y 1994."),
    ("Oscar Piastri debutó en F1 con McLaren.", True,
     "Piastri debutó con McLaren en 2023 y ganó su primera carrera en Hungría 2024."),
]

ROUNDS = 10
PTS_PER_HIT = 100
STREAK_BONUS = 20

def init():
    if "tf_round" not in st.session_state:
        st.session_state.tf_round = 0
        st.session_state.tf_score = 0
        st.session_state.tf_correct = 0
        st.session_state.tf_streak = 0
        st.session_state.tf_used = set()
        st.session_state.tf_q = None
        st.session_state.tf_answered = False
        st.session_state.tf_done = False
        st.session_state.tf_daily = False
        _next_question()

def _pick():
    pool = [i for i in range(len(STATEMENTS)) if i not in st.session_state.tf_used]
    if not pool:
        st.session_state.tf_used = set()
        pool = list(range(len(STATEMENTS)))
    import datetime
    idx = (int(datetime.date.today().strftime("%Y%m%d")) + st.session_state.tf_round) % len(pool) \
          if st.session_state.tf_daily else random.choice(pool)
    st.session_state.tf_used.add(pool[idx] if st.session_state.tf_daily else idx)
    return STATEMENTS[pool[idx] if st.session_state.tf_daily else idx]

def _next_question():
    if st.session_state.tf_round >= ROUNDS:
        st.session_state.tf_done = True
        return
    st.session_state.tf_q = _pick()
    st.session_state.tf_answered = False
    st.session_state.tf_round += 1

def _answer(resp):
    if st.session_state.tf_answered:
        return
    stmt, correct, explanation = st.session_state.tf_q
    hit = (resp == correct)
    st.session_state.tf_answered = True
    if hit:
        st.session_state.tf_streak += 1
        pts = PTS_PER_HIT + STREAK_BONUS * (st.session_state.tf_streak - 1)
        st.session_state.tf_score += pts
        st.session_state.tf_correct += 1
    else:
        st.session_state.tf_streak = 0
    if st.session_state.tf_daily and st.session_state.tf_round >= ROUNDS:
        mark_daily_played("truefalse")

def render():
    init()
    st.markdown("## 📊 Stats Extremas")
    st.caption("Verdadero o Falso sobre estadísticas de F1 · 10 rondas")

    # Daily toggle
    col1, col2 = st.columns([3,1])
    with col2:
        daily = st.toggle("📅 Diario", key="tf_daily_tog",
                          value=st.session_state.tf_daily)
        if daily != st.session_state.tf_daily:
            st.session_state.tf_daily = daily
            if daily and daily_played("truefalse"):
                st.session_state.tf_done = True

    if st.session_state.tf_done:
        pct = int(st.session_state.tf_correct / ROUNDS * 100)
        if st.session_state.tf_daily and daily_played("truefalse") and st.session_state.tf_round == 0:
            st.warning("🔒 Ya jugaste el modo diario hoy. ¡Volvé mañana!")
            if st.button("🎮 Jugar sin restricción"):
                st.session_state.tf_daily = False
                st.session_state.tf_done = False
                st.session_state.tf_round = 0
                st.session_state.tf_score = 0
                st.session_state.tf_correct = 0
                st.session_state.tf_streak = 0
                _next_question()
                st.rerun()
        else:
            if pct == 100: e, t = "🏆", "¡Perfecto!"
            elif pct >= 70: e, t = "🥇", "¡Muy bien!"
            elif pct >= 40: e, t = "🥈", "Bien, sigue practicando"
            else: e, t = "🤔", "¡Las stats de F1 son complicadas!"
            st.markdown(f"<div style='text-align:center;font-size:48px'>{e}</div>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;color:#e10600'>{t}</h3>", unsafe_allow_html=True)
            st.metric("Correctas", f"{st.session_state.tf_correct}/{ROUNDS}")
            st.metric("Puntuación", st.session_state.tf_score)
            if st.button("🔄 Jugar de nuevo"):
                for k in ["tf_round","tf_score","tf_correct","tf_streak","tf_used","tf_q","tf_answered","tf_done"]:
                    del st.session_state[k]
                st.rerun()
        return

    # Progress
    prog = st.session_state.tf_round - 1
    st.progress(prog / ROUNDS, text=f"Ronda {st.session_state.tf_round}/{ROUNDS}  ·  ⭐ {st.session_state.tf_score} pts  ·  🔥 Racha: {st.session_state.tf_streak}")

    stmt, correct, explanation = st.session_state.tf_q
    st.markdown(f"### {stmt}")

    if not st.session_state.tf_answered:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ VERDADERO", use_container_width=True, type="primary"):
                _answer(True); st.rerun()
        with c2:
            if st.button("❌ FALSO", use_container_width=True):
                _answer(False); st.rerun()
    else:
        _, correct_val, explanation = st.session_state.tf_q
        hit = (st.session_state.tf_streak > 0) if st.session_state.tf_correct > 0 else False
        # re-check: did they get it right?
        # We need to store last result
        st.info(f"💡 {explanation}")
        label = "🏁 Ver resultado" if st.session_state.tf_round >= ROUNDS else "➡️ Siguiente"
        if st.button(label, type="primary"):
            _next_question()
            st.rerun()
