import streamlit as st
import random, datetime
from f1_data import RAW_F1, daily_played, mark_daily_played

# Generar lista de palabras válidas desde RAW_F1
def _build_word_list():
    words = []
    for name in RAW_F1:
        apellido = name.strip().split()[-1].upper()
        if 4 <= len(apellido) <= 8 and apellido.isalpha():
            words.append(apellido)
    return sorted(set(words))

WORD_LIST = _build_word_list()
MAX_INTENTOS = 6

COLOR_GREEN  = "#538d4e"
COLOR_YELLOW = "#b59f3b"
COLOR_GRAY   = "#3a3a3c"
COLOR_EMPTY  = "#1a1a1a"
COLOR_ACTIVE = "#2a2a2a"

def _check_guess(guess, answer):
    result = ["gray"] * len(guess)
    answer_chars = list(answer)
    # Primero verdes
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            result[i] = "green"
            answer_chars[i] = None
    # Luego amarillos
    for i, g in enumerate(guess):
        if result[i] == "green":
            continue
        if g in answer_chars:
            result[i] = "yellow"
            answer_chars[answer_chars.index(g)] = None
    return result

def _pick_word():
    if st.session_state.wd_daily:
        seed = int(datetime.date.today().strftime("%Y%m%d"))
        rng = random.Random(seed)
        return rng.choice(WORD_LIST)
    return random.choice(WORD_LIST)

def init():
    if "wd_answer" not in st.session_state:
        st.session_state.wd_daily = False
        st.session_state.wd_answer = _pick_word()
        st.session_state.wd_guesses = []     # list of (word, colors)
        st.session_state.wd_current = ""
        st.session_state.wd_done = False
        st.session_state.wd_won = False
        st.session_state.wd_msg = ""

def _render_grid():
    answer = st.session_state.wd_answer
    n = len(answer)
    guesses = st.session_state.wd_guesses
    current = st.session_state.wd_current

    rows_html = []
    # Intentos enviados
    for word, colors in guesses:
        cells = []
        for ch, col in zip(word, colors):
            bg = COLOR_GREEN if col=="green" else COLOR_YELLOW if col=="yellow" else COLOR_GRAY
            cells.append(f"<div style='width:52px;height:52px;background:{bg};border-radius:4px;"
                         f"display:flex;align-items:center;justify-content:center;"
                         f"font-size:24px;font-weight:bold;color:white'>{ch}</div>")
        rows_html.append("<div style='display:flex;gap:6px;justify-content:center;margin:3px 0'>" + "".join(cells) + "</div>")

    # Fila activa
    if len(guesses) < MAX_INTENTOS and not st.session_state.wd_done:
        cells = []
        for i in range(n):
            ch = current[i] if i < len(current) else ""
            border = "2px solid #888" if i < len(current) else "2px solid #444"
            cells.append(f"<div style='width:52px;height:52px;background:{COLOR_ACTIVE};border:{border};border-radius:4px;"
                         f"display:flex;align-items:center;justify-content:center;"
                         f"font-size:24px;font-weight:bold;color:white'>{ch}</div>")
        rows_html.append("<div style='display:flex;gap:6px;justify-content:center;margin:3px 0'>" + "".join(cells) + "</div>")

    # Filas vacías
    empty_rows = MAX_INTENTOS - len(guesses) - (0 if st.session_state.wd_done else 1)
    for _ in range(max(0, empty_rows)):
        cells = [f"<div style='width:52px;height:52px;background:{COLOR_EMPTY};border:2px solid #333;"
                 f"border-radius:4px'></div>" for _ in range(n)]
        rows_html.append("<div style='display:flex;gap:6px;justify-content:center;margin:3px 0'>" + "".join(cells) + "</div>")

    return "<div style='margin:16px auto;width:fit-content'>" + "".join(rows_html) + "</div>"

def _render_keyboard():
    guesses = st.session_state.wd_guesses
    answer  = st.session_state.wd_answer
    # Estado de cada letra
    letter_state = {}
    for word, colors in guesses:
        for ch, col in zip(word, colors):
            # verde > amarillo > gris
            prev = letter_state.get(ch, "unused")
            if col == "green": letter_state[ch] = "green"
            elif col == "yellow" and prev != "green": letter_state[ch] = "yellow"
            elif col == "gray" and prev == "unused": letter_state[ch] = "gray"

    rows = ["QWERTYUIOP", "ASDFGHJKLÑ", "ZXCVBNM"]
    html = "<div style='text-align:center;margin:12px 0'>"
    for row in rows:
        html += "<div style='display:flex;justify-content:center;gap:4px;margin:3px 0'>"
        for ch in row:
            state = letter_state.get(ch, "unused")
            bg = COLOR_GREEN if state=="green" else COLOR_YELLOW if state=="yellow" else COLOR_GRAY if state=="gray" else "#444"
            html += (f"<div style='width:36px;height:38px;background:{bg};border-radius:4px;"
                     f"display:flex;align-items:center;justify-content:center;"
                     f"font-size:13px;font-weight:bold;color:white'>{ch}</div>")
        html += "</div>"
    html += "</div>"
    return html

def _submit():
    guess = st.session_state.wd_current.upper()
    answer = st.session_state.wd_answer
    if len(guess) != len(answer):
        st.session_state.wd_msg = f"⚠️ La palabra debe tener {len(answer)} letras"
        return
    colors = _check_guess(guess, answer)
    st.session_state.wd_guesses.append((guess, colors))
    st.session_state.wd_current = ""
    if guess == answer:
        st.session_state.wd_done = True
        st.session_state.wd_won = True
        st.session_state.wd_msg = "🎉 ¡Correcto!"
        if st.session_state.wd_daily:
            mark_daily_played("wordle_f1")
    elif len(st.session_state.wd_guesses) >= MAX_INTENTOS:
        st.session_state.wd_done = True
        st.session_state.wd_msg = f"😔 Era: **{answer}**"
        if st.session_state.wd_daily:
            mark_daily_played("wordle_f1")

def render():
    init()
    st.markdown("## 🧩 F1 Wordle")
    st.caption(f"Adiviná el apellido del piloto de F1 · {MAX_INTENTOS} intentos")

    col1, col2 = st.columns([3, 1])
    with col2:
        daily = st.toggle("📅 Diario", key="wd_daily_tog", value=st.session_state.wd_daily)
        if daily != st.session_state.wd_daily:
            st.session_state.wd_daily = daily
            if daily and daily_played("wordle_f1"):
                st.warning("🔒 Ya jugaste el Wordle de hoy.")
                if st.button("🎮 Jugar libre"):
                    st.session_state.wd_daily = False
                    st.rerun()
                return

    # Grilla
    st.markdown(_render_grid(), unsafe_allow_html=True)

    # Teclado visual
    st.markdown(_render_keyboard(), unsafe_allow_html=True)

    if st.session_state.wd_msg:
        if "Correcto" in st.session_state.wd_msg:
            st.success(st.session_state.wd_msg)
        elif "Era:" in st.session_state.wd_msg:
            st.error(st.session_state.wd_msg)
        else:
            st.warning(st.session_state.wd_msg)

    if not st.session_state.wd_done:
        answer = st.session_state.wd_answer
        st.markdown(f"*Palabra de {len(answer)} letras*")
        col_input, col_del, col_ok = st.columns([3, 1, 1])
        with col_input:
            typed = st.text_input("Escribí una letra o la palabra completa",
                                  value=st.session_state.wd_current,
                                  max_chars=len(answer),
                                  key="wd_text",
                                  label_visibility="collapsed").upper()
            # Solo A-Z
            typed = "".join(c for c in typed if c.isalpha())[:len(answer)]
            if typed != st.session_state.wd_current:
                st.session_state.wd_current = typed
                st.session_state.wd_msg = ""
        with col_del:
            if st.button("⌫ Borrar"):
                st.session_state.wd_current = st.session_state.wd_current[:-1]
                st.rerun()
        with col_ok:
            if st.button("✔ Enviar", type="primary"):
                _submit()
                st.rerun()
    else:
        if st.button("🔄 Nueva palabra"):
            for k in list(st.session_state.keys()):
                if k.startswith("wd_"):
                    del st.session_state[k]
            st.rerun()
