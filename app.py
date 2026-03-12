   """
F1 Game Center v2 — Streamlit app (9 modos)
Ejecutar: streamlit run app.py
"""
import streamlit as st
import random
import hashlib
import datetime
import json
import pathlib
import unicodedata
import time

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import f1_data as D

# ══════════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="F1 Game Center",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1,h2,h3 { font-family: 'Rajdhani', sans-serif !important; }
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 1rem; max-width: 1100px; }
.stButton > button {
    border-radius: 6px; font-family: 'Rajdhani', sans-serif;
    font-weight: 600; font-size: 15px; letter-spacing: 0.5px; transition: all 0.15s;
}
.stButton > button:hover { transform: translateY(-1px); }
.f1-divider { height: 3px; background: linear-gradient(90deg, #e10600, #ff6b35, #e10600);
    border-radius: 2px; margin: 8px 0 16px; }
.pista-box { background:#1a1a1a; border-left:4px solid #1565c0; border-radius:0 8px 8px 0;
    padding:10px 16px; margin:4px 0; font-size:0.95rem; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PERSISTENCIA
# ══════════════════════════════════════════════════════════════════
DATA_FILE = pathlib.Path("~/.f1grid_data.json").expanduser()

def load_data() -> dict:
    try:
        return json.loads(DATA_FILE.read_text())
    except Exception:
        return {}

def save_data(data: dict):
    try:
        DATA_FILE.write_text(json.dumps(data))
    except Exception:
        pass

def already_played(key: str) -> bool:
    return load_data().get("daily_played", {}).get(key, False)

def mark_played(key: str):
    d = load_data()
    d.setdefault("daily_played", {})[key] = True
    save_data(d)

def add_points(pts: int):
    d = load_data()
    d["total_pts"] = d.get("total_pts", 0) + pts
    save_data(d)

def get_total_pts() -> int:
    return load_data().get("total_pts", 0)

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════
def normalize(s: str) -> str:
    s = s.lower().strip()
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("utf-8")
    return s

def daily_seed(prefix: str) -> int:
    today = datetime.date.today().isoformat()
    return int(hashlib.md5(f"{prefix}-{today}".encode()).hexdigest(), 16) % (2**31)

def fmt(name: str) -> str:
    return name.title()

FLAGS = {
    "española":"🇪🇸","británica":"🇬🇧","alemana":"🇩🇪","finlandesa":"🇫🇮",
    "australiana":"🇦🇺","brasileña":"🇧🇷","mexicana":"🇲🇽","francesa":"🇫🇷",
    "monegasca":"🇲🇨","neerlandesa":"🇳🇱","tailandesa":"🇹🇭","argentina":"🇦🇷",
    "canadiense":"🇨🇦","rusa":"🇷🇺","italiana":"🇮🇹","japonesa":"🇯🇵",
    "austriaca":"🇦🇹","colombiana":"🇨🇴","venezolana":"🇻🇪","danesa":"🇩🇰",
    "neozelandesa":"🇳🇿","sueca":"🇸🇪","sudafricana":"🇿🇦","estadounidense":"🇺🇸",
    "suiza":"🇨🇭","india":"🇮🇳","portuguesa":"🇵🇹","húngara":"🇭🇺","belga":"🇧🇪",
    "irlandesa":"🇮🇪","china":"🇨🇳","noruega":"🇳🇴","estonia":"🇪🇪",
    "polaca":"🇵🇱","singapurense":"🇸🇬","turca":"🇹🇷","indonesia":"🇮🇩",
    "checa":"🇨🇿","ecuatoriana":"🇪🇨","paraguaya":"🇵🇾","búlgara":"🇧🇬",
}

CIRCUIT_FLAGS = {
    "Mónaco":"🇲🇨","Italia":"🇮🇹","Gran Bretaña":"🇬🇧","Bélgica":"🇧🇪",
    "Japón":"🇯🇵","Brasil":"🇧🇷","España":"🇪🇸","Emiratos Árabes":"🇦🇪",
    "Hungría":"🇭🇺","Países Bajos":"🇳🇱","Alemania":"🇩🇪","Arabia Saudí":"🇸🇦",
    "Bahréin":"🇧🇭","Australia":"🇦🇺","China":"🇨🇳","Estados Unidos":"🇺🇸",
    "México":"🇲🇽","Singapur":"🇸🇬","Azerbaiyán":"🇦🇿","Canadá":"🇨🇦",
    "Catar":"🇶🇦","Francia":"🇫🇷","Portugal":"🇵🇹","Turquía":"🇹🇷",
}

def flag(nat: str) -> str:
    return FLAGS.get(nat, "🏁")

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════
def ss(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

ss("mode", "home")
for k in ["grid_state","podium_state","duel_state","constructor_state",
          "timeline_state","mystery_state","chain_state","whowon_state","circuit_state"]:
    ss(k, None)

# ══════════════════════════════════════════════════════════════════
#  HEADER GLOBAL
# ══════════════════════════════════════════════════════════════════
def render_header():
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        st.markdown(
            "<h1 style='font-family:Rajdhani;color:#e10600;margin:0;font-size:2.2rem'>"
            "🏎️ F1 GAME CENTER</h1><div class='f1-divider'></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.metric("⭐ Puntos", f"{get_total_pts():,}")
    with c3:
        if st.session_state.mode != "home":
            if st.button("🏠 Inicio", use_container_width=True):
                st.session_state.mode = "home"
                st.rerun()

# ══════════════════════════════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════════════════════════════
MODES = [
    ("🔲", "Grid Challenge",         "grid",        "Completá el grid F1/F2/F3 con pilotos"),
    ("🏆", "Podium Challenge",       "podium",      "Adiviná el top 10 de un GP histórico"),
    ("⚔️",  "Duelo de Pilotos",      "duel",        "¿Quién tiene más? Victorias · Podios · Títulos"),
    ("🏗️", "Constructor Challenge",  "constructor", "Adiviná la escudería que cumple la condición"),
    ("📅", "Línea de Tiempo",        "timeline",    "Ordená 5 eventos F1 cronológicamente"),
    ("🕵️", "Piloto Misterioso",      "mystery",     "Adiviná el piloto con las mínimas pistas"),
    ("🔗", "Cadena de Pilotos",      "chain",       "Conectá dos pilotos por compañeros de equipo"),
    ("🏁", "¿Quién Ganó?",           "whowon",      "Adiviná el ganador de un GP histórico"),
    ("🗺️", "¿En qué Circuito?",     "circuit",     "Adiviná el circuito por sus características"),
]

def render_home():
    st.markdown("<p style='color:#888;font-size:1rem;margin-bottom:24px'>Elegí un modo para jugar</p>",
                unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (icon, name, mode_key, desc) in enumerate(MODES):
        with cols[i % 3]:
            st.markdown(
                f"<div style='background:#111;border:1px solid #222;border-radius:12px;"
                f"padding:20px;text-align:center;margin-bottom:4px'>"
                f"<div style='font-size:2.2rem'>{icon}</div>"
                f"<div style='font-family:Rajdhani;font-size:1.3rem;font-weight:700;"
                f"color:#f0f0f0;margin:6px 0 4px'>{name}</div>"
                f"<div style='font-size:0.8rem;color:#777'>{desc}</div></div>",
                unsafe_allow_html=True,
            )
            if st.button("Jugar", key=f"btn_mode_{mode_key}", use_container_width=True):
                st.session_state.mode = mode_key
                st.rerun()

# ══════════════════════════════════════════════════════════════════
#  MODO 1 — GRID CHALLENGE
# ══════════════════════════════════════════════════════════════════
def init_grid(series_name, difficulty, daily=False):
    series = D.SERIES_MAP[series_name]
    cfg    = D.DIFFICULTY_CONFIG[difficulty]
    if daily:
        rng_state = random.getstate()
        random.seed(daily_seed(f"grid-{series_name}-{difficulty}"))
        row_cats, col_cats = series.generate_grid(cfg)
        random.setstate(rng_state)
    else:
        row_cats, col_cats = series.generate_grid(cfg)
    return {
        "series_name": series_name, "difficulty": difficulty, "daily": daily,
        "size": cfg["grid_size"], "row_cats": row_cats, "col_cats": col_cats,
        "answers": {}, "results": {}, "checked": False,
        "correct": 0, "score": 0,
        "start_time": datetime.datetime.now().isoformat(), "finished": False,
    }

def render_grid():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🔲 GRID CHALLENGE</h2>",
                unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
    with col1:
        series_name = st.selectbox("Serie", list(D.SERIES_MAP.keys()), key="grid_series")
    with col2:
        difficulty  = st.selectbox("Dificultad", list(D.DIFFICULTY_CONFIG.keys()), key="grid_diff", index=1)
    with col3:
        if st.button("🆕 Nuevo", use_container_width=True, type="primary"):
            st.session_state.grid_state = init_grid(series_name, difficulty)
            st.session_state.grid_show_solutions = False
            st.rerun()
    with col4:
        daily_key = f"grid-daily-{series_name}-{difficulty}-{datetime.date.today().isoformat()}"
        if st.button("📅 Diario", use_container_width=True):
            if already_played(daily_key):
                st.warning("Ya jugaste el grid del día.")
            else:
                st.session_state.grid_state = init_grid(series_name, difficulty, daily=True)
                st.rerun()
    with col5:
        if st.button("💡 Soluciones", use_container_width=True):
            st.session_state.grid_show_solutions = not st.session_state.get("grid_show_solutions", False)
            st.rerun()

    gs = st.session_state.grid_state
    if gs is None:
        st.info("Presioná **Nuevo** para empezar.")
        return

    series = D.SERIES_MAP[gs["series_name"]]
    size   = gs["size"]
    cfg    = D.DIFFICULTY_CONFIG[gs["difficulty"]]
    COLORS_MAP = {
        "🏎️ Fórmula 1": ("#e10600","#1565c0"),
        "🚀 Fórmula 2": ("#1565c0","#e10600"),
        "🔵 Fórmula 3": ("#2e7d32","#1b5e20"),
        "🔀 Modo Mixto": ("#6a1b9a","#4a148c"),
    }
    col_color, row_color = COLORS_MAP.get(gs["series_name"], ("#e10600","#1565c0"))
    all_drivers = sorted(d.title() for d in series.all_drivers)

    header_cols = st.columns([1] + [1]*size)
    header_cols[0].markdown("&nbsp;", unsafe_allow_html=True)
    for c_idx, cc in enumerate(gs["col_cats"]):
        header_cols[c_idx+1].markdown(
            f"<div style='background:{col_color}22;border:1px solid {col_color}55;"
            f"border-radius:6px;padding:6px;font-size:11px;font-weight:600;"
            f"text-align:center;color:{col_color};min-height:48px;"
            f"display:flex;align-items:center;justify-content:center'>{cc['label']}</div>",
            unsafe_allow_html=True)

    for r_idx, rc in enumerate(gs["row_cats"]):
        row_cols = st.columns([1] + [1]*size)
        row_cols[0].markdown(
            f"<div style='background:{row_color}22;border:1px solid {row_color}55;"
            f"border-radius:6px;padding:6px;font-size:11px;font-weight:600;"
            f"text-align:center;color:{row_color};min-height:48px;"
            f"display:flex;align-items:center;justify-content:center'>{rc['label']}</div>",
            unsafe_allow_html=True)
        for c_idx, cc in enumerate(gs["col_cats"]):
            result = gs["results"].get((r_idx, c_idx), "")
            border = {"correct":"2px solid #2e7d32","wrong":"2px solid #c62828",
                      "repeat":"2px solid #e65100","notfound":"2px solid #555"}.get(result,"2px solid #333")
            bg     = {"correct":"#0a1f0a","wrong":"#1f0a0a"}.get(result,"#0d0d0d")
            with row_cols[c_idx+1]:
                st.markdown(f"<div style='border:{border};border-radius:6px;background:{bg};padding:2px'>",
                            unsafe_allow_html=True)
                current_val = gs["answers"].get((r_idx, c_idx), "")
                val = st.selectbox("", [""] + all_drivers,
                    index=(all_drivers.index(current_val)+1 if current_val in all_drivers else 0),
                    key=f"grid_inp_{r_idx}_{c_idx}", label_visibility="collapsed")
                gs["answers"][(r_idx, c_idx)] = val
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    b1, b2 = st.columns([1, 3])
    with b1:
        if st.button("✔ Verificar", type="primary", use_container_width=True):
            allow_repeat = cfg.get("allow_repeat", False)
            used = set(); results = {}; correct = 0
            for r in range(size):
                for c in range(size):
                    raw    = gs["answers"].get((r, c), "")
                    driver = normalize(raw)
                    if not driver: results[(r,c)] = ""; continue
                    if driver not in series.drivers_meta: results[(r,c)] = "notfound"; continue
                    rc2 = gs["row_cats"][r]; cc2 = gs["col_cats"][c]
                    possible = series.drivers_satisfying(rc2, cc2)
                    if driver in used and (not allow_repeat or len(possible) > 1):
                        results[(r,c)] = "repeat"; continue
                    if rc2["check"](driver) and cc2["check"](driver):
                        results[(r,c)] = "correct"; used.add(driver); correct += 1
                    else:
                        results[(r,c)] = "wrong"
            gs["results"] = results; gs["checked"] = True; gs["correct"] = correct
            elapsed = (datetime.datetime.now() - datetime.datetime.fromisoformat(gs["start_time"])).seconds
            mult  = {"🟢 Fácil":1,"🟡 Medio":2,"🔴 Difícil":3,"💀 Experto":5}.get(gs["difficulty"],1)
            tlim  = cfg.get("time_limit")
            bonus = max(0, tlim - elapsed) * 5 * mult if tlim else 0
            gs["score"] = correct * 100 * mult + bonus
            if correct == size * size:
                add_points(gs["score"])
                if gs["daily"]: mark_played(daily_key)
            st.session_state.grid_state = gs; st.rerun()
    with b2:
        if gs.get("checked"):
            correct = gs["correct"]; total = size*size; score = gs["score"]
            color = "#00c853" if correct==total else "#ffd700" if correct>0 else "#888"
            st.markdown(f"<div style='font-family:Rajdhani;font-size:1.3rem;font-weight:700;"
                        f"color:{color};padding:6px 0'>✅ {correct}/{total} · ⭐ {score} pts</div>",
                        unsafe_allow_html=True)
            if correct == total: st.balloons()

    if st.session_state.get("grid_show_solutions"):
        st.markdown("---"); st.markdown("**💡 Soluciones posibles:**")
        for r in range(size):
            for c in range(size):
                sol = sorted(series.drivers_satisfying(gs["row_cats"][r], gs["col_cats"][c]))
                st.markdown(f"**[{gs['row_cats'][r]['label']}] × [{gs['col_cats'][c]['label']}]:** "
                            + ", ".join(fmt(d) for d in sol[:8])
                            + (f" (+{len(sol)-8})" if len(sol)>8 else ""))

# ══════════════════════════════════════════════════════════════════
#  MODO 2 — PODIUM CHALLENGE
# ══════════════════════════════════════════════════════════════════
def init_podium(year=None, gp=None, daily=False):
    if daily:
        rng  = random.Random(daily_seed("podium"))
        year = rng.choice(sorted(D.GP_RESULTS.keys()))
        gp   = rng.choice(sorted(D.GP_RESULTS[year].keys()))
    elif year is None or gp is None:
        year = random.choice(sorted(D.GP_RESULTS.keys()))
        gp   = random.choice(sorted(D.GP_RESULTS[year].keys()))
    return {"year": year, "gp": gp,
            "answer": [normalize(d) for d in D.GP_RESULTS[year][gp]],
            "inputs": [""]*10, "results": [], "checked": False, "score": 0, "daily": daily}

def render_podium():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🏆 PODIUM CHALLENGE</h2>",
                unsafe_allow_html=True)
    all_f1   = sorted(d.title() for d in D.RAW_F1.keys())
    decades  = ["Todos"] + [f"{d}s" for d in range(1950,2030,10) if any(
        (d//10)*10 <= y < (d//10)*10+10 for y in D.GP_RESULTS)]
    c1,c2,c3,c4 = st.columns([2,1,1,1])
    with c1: dec_filter = st.selectbox("Época", decades, key="podium_dec")
    with c2:
        if st.button("🎲 Aleatorio", use_container_width=True, type="primary"):
            filtered = [y for y in D.GP_RESULTS if dec_filter=="Todos" or
                        str((y//10)*10)+"s"==dec_filter]
            if filtered:
                yr = random.choice(filtered)
                gp = random.choice(list(D.GP_RESULTS[yr].keys()))
                st.session_state.podium_state = init_podium(yr, gp); st.rerun()
    with c3:
        if st.button("📅 Diario", use_container_width=True):
            key = f"podium-daily-{datetime.date.today().isoformat()}"
            if already_played(key): st.warning("Ya jugaste el Podio del día.")
            else: st.session_state.podium_state = init_podium(daily=True); st.rerun()
    with c4:
        if st.session_state.podium_state and st.session_state.podium_state.get("checked"):
            if st.button("🔄 Otro GP", use_container_width=True):
                st.session_state.podium_state = None; st.rerun()

    ps = st.session_state.podium_state
    if ps is None:
        st.info("Presioná **Aleatorio** o **Diario** para empezar."); return

    st.markdown(f"<div style='background:#1a1a1a;border:1px solid #333;border-radius:10px;"
                f"padding:16px;margin:12px 0'><h3 style='font-family:Rajdhani;color:#ffd700;margin:0'>"
                f"🏁 {ps['gp']} {ps['year']}</h3>"
                f"<p style='color:#888;margin:4px 0 0;font-size:0.85rem'>Ingresá los 10 pilotos en orden — P1 a P10</p></div>",
                unsafe_allow_html=True)

    cols = st.columns(2)
    for i in range(10):
        result = ps["results"][i] if ps.get("checked") and i < len(ps["results"]) else None
        icon   = {"correct_pos":"🟢","correct_any":"🟡","wrong":"🔴","empty":"⚪"}.get(result or "empty","⚪")
        with cols[i % 2]:
            val = st.selectbox(f"{icon} P{i+1}", [""]+all_f1,
                index=(all_f1.index(ps["inputs"][i])+1 if ps["inputs"][i] in all_f1 else 0),
                key=f"podium_inp_{i}")
            ps["inputs"][i] = val

    b1, b2 = st.columns([1,3])
    with b1:
        if st.button("✔ Verificar", type="primary", use_container_width=True, disabled=ps.get("checked",False)):
            results=[]; pts=0
            for i in range(10):
                driver = normalize(ps["inputs"][i])
                if not driver: results.append("empty"); continue
                if driver == (ps["answer"][i] if i < len(ps["answer"]) else ""):
                    results.append("correct_pos"); pts += 100
                elif driver in ps["answer"]:
                    results.append("correct_any"); pts += 20
                else:
                    results.append("wrong")
            ps["results"]=results; ps["checked"]=True; ps["score"]=pts
            add_points(pts)
            if ps["daily"]: mark_played(f"podium-daily-{datetime.date.today().isoformat()}")
            st.session_state.podium_state = ps; st.rerun()
    with b2:
        if ps.get("checked"):
            cp = ps["results"].count("correct_pos"); ca = ps["results"].count("correct_any")
            st.markdown(f"<div style='font-family:Rajdhani;font-size:1.2rem;padding:6px 0'>"
                        f"🟢 {cp} exactos · 🟡 {ca} en el top10 · ⭐ <b>{ps['score']} pts</b></div>",
                        unsafe_allow_html=True)

    if ps.get("checked"):
        with st.expander("🏁 Ver resultado completo"):
            answer = D.GP_RESULTS[ps["year"]][ps["gp"]]
            for i, d in enumerate(answer):
                res  = ps["results"][i] if i < len(ps["results"]) else "empty"
                icon = {"correct_pos":"🟢","correct_any":"🟡","wrong":"🔴","empty":"⚪"}.get(res,"⚪")
                inp  = ps["inputs"][i]
                mark = f" ← ✅ {fmt(d)}" if res=="correct_pos" else f" ← ⚠️ era {fmt(d)}"
                st.markdown(f"**P{i+1}** {icon} {inp or '_(vacío)_'}{mark}")

# ══════════════════════════════════════════════════════════════════
#  MODO 3 — DUELO DE PILOTOS
# ══════════════════════════════════════════════════════════════════
DUEL_STATS = {"wins":("🏆 VICTORIAS","victorias"),"podiums":("🥇 PODIOS","podios"),"champion":("👑 CAMPEONATOS","campeonatos")}

def get_stat(driver, stat):
    m = D.SERIES_F1.drivers_meta[driver]
    if stat == "champion":
        c = m["champion"]; return c if isinstance(c, int) else (1 if c else 0)
    return m[stat]

def pick_duel_pair(stat):
    pool = [d for d, m in D.SERIES_F1.drivers_meta.items() if m["podiums"] >= 1]
    for _ in range(300):
        a, b = random.sample(pool, 2)
        va, vb = get_stat(a,stat), get_stat(b,stat)
        if va != vb: return a, b, va, vb
    a, b = random.sample(pool, 2); return a, b, get_stat(a,stat), get_stat(b,stat)

def init_duel(daily=False):
    ss("duel_streak",0); ss("duel_best",0); ss("duel_total",0)
    stat = random.choice(list(DUEL_STATS.keys()))
    if daily:
        rng  = random.Random(daily_seed("duel"))
        pool = sorted(d for d,m in D.SERIES_F1.drivers_meta.items() if m["podiums"]>=1)
        stat = list(DUEL_STATS.keys())[rng.randint(0,2)]
        for _ in range(300):
            a, b = rng.sample(pool, 2)
            va, vb = get_stat(a,stat), get_stat(b,stat)
            if va != vb: break
    else:
        a, b, va, vb = pick_duel_pair(stat)
        va, vb = get_stat(a,stat), get_stat(b,stat)
    va, vb = get_stat(a,stat), get_stat(b,stat)
    return {"a":a,"b":b,"va":va,"vb":vb,"stat":stat,"revealed":False,
            "correct":None,"daily":daily}

def render_duel():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>⚔️ DUELO DE PILOTOS</h2>",
                unsafe_allow_html=True)
    ss("duel_streak",0); ss("duel_best",0); ss("duel_total",0)

    c1,c2 = st.columns([1,1])
    with c1:
        if st.button("🆕 Nueva Partida", use_container_width=True):
            st.session_state.duel_streak = 0
            st.session_state.duel_state  = init_duel(); st.rerun()
    with c2:
        if st.button("📅 Duelo del Día", use_container_width=True):
            key = f"duel-daily-{datetime.date.today().isoformat()}"
            if already_played(key): st.warning("Ya jugaste el Duelo del día.")
            else:
                st.session_state.duel_streak = 0
                st.session_state.duel_state  = init_duel(daily=True); st.rerun()

    ds = st.session_state.duel_state
    if ds is None:
        st.info("Presioná **Nueva Partida** para empezar."); return

    sc1,sc2,sc3 = st.columns(3)
    sc1.metric("🔥 Racha", st.session_state.duel_streak)
    sc2.metric("🏅 Mejor", st.session_state.duel_best)
    sc3.metric("⭐ Puntos", st.session_state.duel_total)

    stat_label, stat_word = DUEL_STATS[ds["stat"]]
    st.markdown(f"<div style='text-align:center;font-family:Rajdhani;font-size:1.3rem;"
                f"color:#bbb;padding:12px 0'>¿Quién tiene más "
                f"<span style='color:#ffd700;font-size:1.5rem'>{stat_word.upper()}</span> en F1?</div>",
                unsafe_allow_html=True)

    def driver_card(driver, revealed=False, val=None, winner=False, loser=False):
        meta = D.SERIES_F1.drivers_meta[driver]
        nat  = meta["nationality"]; teams = meta["teams"]
        team_str = ", ".join(t.title() for t in teams[:2]) + (" …" if len(teams)>2 else "")
        border = "#00c853" if winner else ("#c62828" if loser else "#333")
        bg     = "#0a2a0a" if winner else ("#2a0a0a" if loser else "#1a1a1a")
        num    = str(val) if revealed and val is not None else "?"
        num_c  = "#ffd700" if winner else ("#888" if loser else "#f0f0f0")
        return (f"<div style='background:{bg};border:2px solid {border};"
                f"border-radius:12px;padding:24px 16px;text-align:center'>"
                f"<div style='font-size:2.5rem'>{flag(nat)}</div>"
                f"<div style='font-family:Rajdhani;font-size:1.3rem;font-weight:700;"
                f"color:#f0f0f0;margin:8px 0 4px'>{fmt(driver)}</div>"
                f"<div style='font-size:0.75rem;color:#666;margin-bottom:12px'>{team_str}</div>"
                f"<div style='font-size:2.5rem;font-weight:700;color:{num_c}'>{num}</div>"
                f"<div style='font-size:0.7rem;color:#555;text-transform:uppercase;letter-spacing:2px'>{stat_word}</div></div>")

    revealed = ds.get("revealed", False)
    winner_a = revealed and ds["va"] > ds["vb"]
    winner_b = revealed and ds["vb"] > ds["va"]
    ca, cb   = st.columns(2)
    with ca: st.markdown(driver_card(ds["a"],revealed,ds["va"] if revealed else None,winner=winner_a,loser=revealed and not winner_a),unsafe_allow_html=True)
    with cb: st.markdown(driver_card(ds["b"],revealed,ds["vb"] if revealed else None,winner=winner_b,loser=revealed and not winner_b),unsafe_allow_html=True)

    if not revealed:
        b1, b2 = st.columns(2)
        with b1:
            if st.button(f"◀ {fmt(ds['a'])}", use_container_width=True, type="primary"):
                _duel_answer("a", ds)
        with b2:
            if st.button(f"{fmt(ds['b'])} ▶", use_container_width=True, type="primary"):
                _duel_answer("b", ds)
    else:
        fb_color = "#00c853" if ds["correct"] else "#c62828"
        streak   = st.session_state.duel_streak
        fb_text  = (f"✅ ¡CORRECTO! +{10+max(0,streak-1)*5} pts · Racha: {streak}"
                    if ds["correct"] else "❌ INCORRECTO — Racha perdida")
        st.markdown(f"<div style='text-align:center;font-family:Rajdhani;font-size:1.4rem;"
                    f"font-weight:700;color:{fb_color};padding:12px'>{fb_text}</div>",
                    unsafe_allow_html=True)
        bc1, bc2 = st.columns(2)
        with bc1:
            if ds["correct"] and st.button("➡ Siguiente", use_container_width=True, type="primary"):
                stat = random.choice(list(DUEL_STATS.keys()))
                a, b, va, vb = pick_duel_pair(stat)
                st.session_state.duel_state = {**ds,"a":a,"b":b,"va":va,"vb":vb,"stat":stat,
                    "revealed":False,"correct":None}; st.rerun()
        with bc2:
            if st.button("🔄 Nueva Partida", use_container_width=True):
                st.session_state.duel_streak = 0
                st.session_state.duel_state  = init_duel(); st.rerun()

def _duel_answer(chosen, ds):
    correct_side = "a" if ds["va"] > ds["vb"] else "b"
    correct = chosen == correct_side
    if correct:
        st.session_state.duel_streak += 1
        st.session_state.duel_best   = max(st.session_state.duel_streak, st.session_state.duel_best)
        pts = 10 + (st.session_state.duel_streak - 1) * 5
        st.session_state.duel_total += pts
        add_points(pts)
    else:
        st.session_state.duel_streak = 0
    ds["revealed"] = True; ds["correct"] = correct
    if ds["daily"]: mark_played(f"duel-daily-{datetime.date.today().isoformat()}")
    st.session_state.duel_state = ds; st.rerun()

# ══════════════════════════════════════════════════════════════════
#  MODO 4 — CONSTRUCTOR CHALLENGE
# ══════════════════════════════════════════════════════════════════
def init_constructor():
    cats       = D.CONSTRUCTOR_CATS
    valid_cats = [c for c in cats if len([t for t in D.RAW_CONSTRUCTORS if c["check"](t)])>=2]
    row_cats   = random.sample(valid_cats, 3)
    remaining  = [c for c in valid_cats if c not in row_cats]
    col_cats   = random.sample(remaining, 3)
    grid = {}
    for r, rc in enumerate(row_cats):
        for c, cc in enumerate(col_cats):
            valid = [t for t in D.RAW_CONSTRUCTORS if rc["check"](t) and cc["check"](t)]
            grid[(r,c)] = {"valid":valid,"attempts":3,"answer":"","solved":False,"failed":False}
    return {"row_cats":row_cats,"col_cats":col_cats,"grid":grid,"score":0}

def render_constructor():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🏗️ CONSTRUCTOR CHALLENGE</h2>",
                unsafe_allow_html=True)
    c1, _ = st.columns([1,4])
    with c1:
        if st.button("🆕 Nuevo", use_container_width=True, type="primary"):
            st.session_state.constructor_state = init_constructor(); st.rerun()

    cs = st.session_state.constructor_state
    if cs is None:
        st.info("Presioná **Nuevo** para empezar."); return

    all_constructors = sorted(D.ALL_CONSTRUCTORS)
    hcols = st.columns([1.2]+[1]*3)
    hcols[0].markdown("")
    for c_idx, cc in enumerate(cs["col_cats"]):
        hcols[c_idx+1].markdown(
            f"<div style='background:#1a1a2e;border:1px solid #334;border-radius:6px;"
            f"padding:6px;font-size:11px;font-weight:600;text-align:center;color:#aac;"
            f"min-height:44px;display:flex;align-items:center;justify-content:center'>{cc['label']}</div>",
            unsafe_allow_html=True)

    for r_idx, rc in enumerate(cs["row_cats"]):
        rcols = st.columns([1.2]+[1]*3)
        rcols[0].markdown(
            f"<div style='background:#1a2a1a;border:1px solid #343;border-radius:6px;"
            f"padding:6px;font-size:11px;font-weight:600;text-align:center;color:#aca;"
            f"min-height:44px;display:flex;align-items:center;justify-content:center'>{rc['label']}</div>",
            unsafe_allow_html=True)
        for c_idx in range(3):
            cell = cs["grid"][(r_idx,c_idx)]
            with rcols[c_idx+1]:
                if cell["solved"]:
                    st.markdown(f"<div style='background:#0a2a0a;border:2px solid #2e7d32;"
                                f"border-radius:8px;padding:10px;text-align:center;"
                                f"font-family:Rajdhani;font-size:1rem;color:#00c853'>"
                                f"✅ {cell['answer'].title()}<br>"
                                f"<span style='font-size:0.7rem;color:#666'>{cell['attempts']} int. restantes</span></div>",
                                unsafe_allow_html=True)
                elif cell["failed"]:
                    valid_str = ", ".join(t.title() for t in cell["valid"][:3])
                    st.markdown(f"<div style='background:#2a0a0a;border:2px solid #c62828;"
                                f"border-radius:8px;padding:8px;text-align:center;"
                                f"font-size:0.75rem;color:#e57373'>❌ Sin intentos<br>"
                                f"<span style='color:#666'>{valid_str}</span></div>",
                                unsafe_allow_html=True)
                else:
                    val = st.selectbox(f"Intentos: {cell['attempts']}", [""]+all_constructors,
                                       key=f"constr_{r_idx}_{c_idx}")
                    if st.button("OK", key=f"constr_ok_{r_idx}_{c_idx}", use_container_width=True):
                        if val:
                            if val.lower() in cell["valid"]:
                                cell["solved"]=True; cell["answer"]=val
                                pts=30*cell["attempts"]; cs["score"]+=pts; add_points(pts)
                            else:
                                cell["attempts"]-=1
                                if cell["attempts"]==0: cell["failed"]=True
                            cs["grid"][(r_idx,c_idx)]=cell
                            st.session_state.constructor_state=cs; st.rerun()

    solved = sum(1 for cell in cs["grid"].values() if cell["solved"])
    st.markdown(f"<div style='font-family:Rajdhani;font-size:1.2rem;color:#ffd700;margin-top:12px'>"
                f"✅ {solved}/9 resueltas · ⭐ {cs['score']} pts</div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  MODO 5 — LÍNEA DE TIEMPO
# ══════════════════════════════════════════════════════════════════
TIMELINE_DIFFS = {
    "🟢 Fácil ×1":   {"mult":1,"range":999,"desc":"Décadas distintas"},
    "🟡 Medio ×2":   {"mult":2,"range":30, "desc":"Rango ~30 años"},
    "🔴 Difícil ×3": {"mult":3,"range":15, "desc":"Rango ~15 años"},
}

def pick_timeline_events(diff_key):
    cfg = TIMELINE_DIFFS[diff_key]; events = D.F1_EVENTS[:]
    for _ in range(500):
        sample = random.sample(events, 5)
        if max(e[0] for e in sample) - min(e[0] for e in sample) <= cfg["range"]:
            return sample
    return random.sample(events, 5)

def init_timeline(diff_key):
    events  = pick_timeline_events(diff_key)
    ordered = sorted(events, key=lambda e: e[0])
    shuffled = events[:]; random.shuffle(shuffled)
    return {"diff":diff_key,"events":shuffled,"correct":ordered,"order":list(range(5)),
            "checked":False,"correct_count":0,"score":0,
            "round":st.session_state.get("timeline_round",1),
            "total_score":st.session_state.get("timeline_total",0)}

def render_timeline():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>📅 LÍNEA DE TIEMPO</h2>",
                unsafe_allow_html=True)
    ss("timeline_round",1); ss("timeline_total",0); ss("timeline_diff","🟢 Fácil ×1")

    c1,c2,c3 = st.columns([2,1,1])
    with c1:
        diff = st.selectbox("Dificultad", list(TIMELINE_DIFFS.keys()), key="timeline_diff_sel",
                            index=list(TIMELINE_DIFFS.keys()).index(st.session_state.timeline_diff))
        st.session_state.timeline_diff = diff
    with c2:
        if st.button("▶ Nueva Ronda", use_container_width=True, type="primary"):
            st.session_state.timeline_state = init_timeline(diff); st.rerun()
    with c3:
        st.metric("⭐ Total", st.session_state.timeline_total)

    ts = st.session_state.timeline_state
    if ts is None:
        st.info("Presioná **Nueva Ronda** para empezar."); return

    st.markdown(f"<div style='color:#888;font-size:0.85rem;margin-bottom:12px'>"
                f"Ronda {ts['round']}/10 · {TIMELINE_DIFFS[ts['diff']]['desc']} · "
                f"Ordená de más antiguo (arriba) a más reciente (abajo)</div>",
                unsafe_allow_html=True)

    CAT_ICONS = {"debut":"🏎️","titulo":"👑","accidente":"🚨","reglamento":"📋","victoria":"🏆","record":"⭐"}
    events = ts["events"]; order = ts["order"]

    if not ts["checked"]:
        for i in range(5):
            evt  = events[order[i]]
            icon = CAT_ICONS.get(evt[2],"📌")
            cA, cB = st.columns([4,1])
            with cA:
                st.markdown(f"<div style='background:#1a1a1a;border:1px solid #333;"
                            f"border-radius:8px;padding:10px 14px;margin:3px 0'>"
                            f"{icon} {evt[1]}</div>",unsafe_allow_html=True)
            with cB:
                btn_col = st.columns(2)
                if i > 0 and btn_col[0].button("▲", key=f"tl_up_{i}"):
                    order[i], order[i-1] = order[i-1], order[i]
                    ts["order"] = order; st.session_state.timeline_state = ts; st.rerun()
                if i < 4 and btn_col[1].button("▼", key=f"tl_dn_{i}"):
                    order[i], order[i+1] = order[i+1], order[i]
                    ts["order"] = order; st.session_state.timeline_state = ts; st.rerun()
        if st.button("✔ Verificar orden", type="primary"):
            user_years    = [events[order[i]][0] for i in range(5)]
            correct_years = [ts["correct"][i][0] for i in range(5)]
            hits = sum(1 for a,b in zip(user_years,correct_years) if a==b)
            mult = TIMELINE_DIFFS[ts["diff"]]["mult"]
            pts  = hits*20*mult + (50*mult if hits==5 else 0)
            ts["checked"]=True; ts["correct_count"]=hits; ts["score"]=pts
            st.session_state.timeline_total += pts; add_points(pts)
            st.session_state.timeline_state = ts; st.rerun()
    else:
        user_order = [events[order[i]] for i in range(5)]
        for i in range(5):
            evt = user_order[i]; expected = ts["correct"][i]
            ok  = evt[0] == expected[0]; icon = CAT_ICONS.get(evt[2],"📌")
            color  = "#0a2a0a" if ok else "#2a0a0a"
            border = "#2e7d32" if ok else "#c62828"
            st.markdown(f"<div style='background:{color};border:1px solid {border};"
                        f"border-radius:8px;padding:10px 14px;margin:3px 0'>"
                        f"{'✅' if ok else '❌'} {icon} <b>{evt[0]}</b> — {evt[1]}</div>",
                        unsafe_allow_html=True)
        hits = ts["correct_count"]; mult = TIMELINE_DIFFS[ts["diff"]]["mult"]
        color_pts = "#ffd700" if hits==5 else "#00c853" if hits>=3 else "#888"
        st.markdown(f"<div style='font-family:Rajdhani;font-size:1.3rem;color:{color_pts};margin:12px 0'>"
                    f"{'🏆 ¡PERFECTO!' if hits==5 else f'{hits}/5 correctos'} · ⭐ {ts['score']} pts</div>",
                    unsafe_allow_html=True)
        if ts["round"] < 10:
            if st.button("➡ Siguiente ronda", type="primary"):
                st.session_state.timeline_round = ts["round"]+1
                new_ts = init_timeline(ts["diff"]); new_ts["round"] = ts["round"]+1
                new_ts["total_score"] = st.session_state.timeline_total
                st.session_state.timeline_state = new_ts; st.rerun()
        else:
            st.success(f"🏁 ¡Partida terminada! Total: {st.session_state.timeline_total} pts")
            if st.button("🔄 Nueva Partida"):
                st.session_state.timeline_round=1; st.session_state.timeline_total=0
                st.session_state.timeline_state=None; st.rerun()

# ══════════════════════════════════════════════════════════════════
#  MODO 6 — PILOTO MISTERIOSO
# ══════════════════════════════════════════════════════════════════
PISTAS_DEF = [
    ("época",        "epoca",       500),
    ("nacionalidad", "nac",         400),
    ("equipos",      "equipos",     300),
    ("estadísticas", "stats",       200),
    ("campeonatos",  "campeonatos", 100),
]

def get_pista_html(driver, meta, idx):
    debut = meta["debut"]
    decade = f"{(debut//10)*10}s" if debut else "desconocida"
    key = PISTAS_DEF[idx][1]
    if key == "epoca":       return f"🕰️ Debutó en los <b>{decade}</b>"
    elif key == "nac":       return f"{flag(meta['nationality'])} Nacionalidad: <b>{meta['nationality'].capitalize()}</b>"
    elif key == "equipos":
        teams = meta["teams"]; first = teams[0].title() if teams else "?"; last = teams[-1].title() if teams else "?"
        return f"🏎️ Primer equipo: <b>{first}</b> · Último: <b>{last}</b>"
    elif key == "stats":     return f"🏆 Victorias: <b>{meta['wins']}</b> · Podios: <b>{meta['podiums']}</b>"
    elif key == "campeonatos":
        champ = meta["champion"]; n = champ if isinstance(champ,int) else (1 if champ else 0)
        return f"👑 Campeonatos: <b>{n}</b> · Temporadas: <b>{meta['seasons']}</b>"
    return ""

def init_mystery(daily=False):
    candidates = [(n,d) for n,d in D.RAW_F1.items() if d[2]>0 or d[3]>0 or bool(d[4])]
    if daily:
        rng = random.Random(daily_seed("mystery"))
        name, data = rng.choice(sorted(candidates, key=lambda x:x[0]))
    else:
        name, data = random.choice(candidates)
    teams,nat,wins,pods,champ,debut,academy,birth,seasons,last = data
    return {"name":name,"meta":{"teams":teams,"nationality":nat,"wins":wins,"podiums":pods,
            "champion":champ,"debut":debut,"seasons":seasons,"last_season":last},
            "pistas_vistas":1,"answered":False,"correct":None,"daily":daily}

def render_mystery():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🕵️ PILOTO MISTERIOSO</h2>",
                unsafe_allow_html=True)
    ss("mystery_score",0); ss("mystery_vistos",set())
    all_f1 = sorted(n.title() for n in D.RAW_F1.keys())

    c1,c2,c3 = st.columns([1,1,2])
    with c1:
        if st.button("🆕 Nuevo Piloto", use_container_width=True, type="primary"):
            st.session_state.mystery_state = init_mystery(); st.rerun()
    with c2:
        if st.button("📅 Piloto del Día", use_container_width=True):
            key = f"mystery-daily-{datetime.date.today().isoformat()}"
            if already_played(key): st.warning("Ya adivinaste el piloto del día.")
            else: st.session_state.mystery_state = init_mystery(daily=True); st.rerun()
    with c3:
        st.markdown(f"<div style='font-family:Rajdhani;font-size:1.1rem;color:#888;padding:8px 0'>"
                    f"⭐ {st.session_state.mystery_score} pts</div>",unsafe_allow_html=True)

    ms = st.session_state.mystery_state
    if ms is None:
        st.info("Presioná **Nuevo Piloto** para empezar."); return

    for i in range(ms["pistas_vistas"]):
        if i < len(PISTAS_DEF):
            pts_if = PISTAS_DEF[i][2]
            pista  = get_pista_html(ms["name"], ms["meta"], i)
            border = "#ffd700" if i==0 else "#333"
            st.markdown(
                f"<div style='background:#1a1a1a;border-left:4px solid {border};"
                f"border-radius:0 8px 8px 0;padding:10px 16px;margin:4px 0;font-size:0.95rem'>"
                f"<span style='color:#555;font-size:0.75rem'>Pista {i+1} ({pts_if} pts si acertás ahora)</span>"
                f"<br>{pista}</div>",unsafe_allow_html=True)

    if not ms["answered"]:
        if ms["pistas_vistas"] < len(PISTAS_DEF):
            if st.button("💡 Ver pista adicional"):
                ms["pistas_vistas"] += 1; st.session_state.mystery_state = ms; st.rerun()
        ci, cb = st.columns([3,1])
        with ci:
            guess = st.selectbox("¿Quién es?", [""]+all_f1, key="mystery_guess",
                                 label_visibility="collapsed")
        with cb:
            if st.button("✔ Responder", type="primary", use_container_width=True):
                if guess:
                    correcto = ms["name"]; val = normalize(guess); partes = normalize(correcto).split()
                    acierto  = (val==normalize(correcto) or val==partes[-1] or
                                (len(partes[0])>=4 and val==partes[0]) or
                                (len(val)>=4 and val in normalize(correcto)))
                    pts_idx  = ms["pistas_vistas"]-1
                    pts      = PISTAS_DEF[pts_idx][2] if acierto else 0
                    ms["answered"]=True; ms["correct"]=acierto; ms["pts_earned"]=pts
                    ms["pistas_vistas"] = len(PISTAS_DEF)
                    if acierto:
                        st.session_state.mystery_score += pts; add_points(pts)
                        st.session_state.mystery_vistos.add(correcto)
                    if ms["daily"]: mark_played(f"mystery-daily-{datetime.date.today().isoformat()}")
                    st.session_state.mystery_state = ms; st.rerun()
    else:
        if ms["correct"]:
            st.success(f"✅ ¡CORRECTO! **{fmt(ms['name'])}** — +{ms.get('pts_earned',0)} pts")
        else:
            st.error(f"❌ Era **{fmt(ms['name'])}**")
        if not ms["daily"] and st.button("➡ Siguiente piloto", type="primary"):
            st.session_state.mystery_state = init_mystery(); st.rerun()

# ══════════════════════════════════════════════════════════════════
#  MODO 7 — CADENA DE PILOTOS
# ══════════════════════════════════════════════════════════════════
CHAIN_DIFFS = {
    "🟢 Fácil":   {"min_hops":2,"max_hops":3,"max_steps":8, "pts_base":200},
    "🟡 Medio":   {"min_hops":3,"max_hops":4,"max_steps":6, "pts_base":400},
    "🔴 Difícil": {"min_hops":4,"max_hops":5,"max_steps":5, "pts_base":700},
}

def init_chain(diff_key="🟡 Medio", daily=False):
    cfg = CHAIN_DIFFS[diff_key]
    if daily:
        rng = random.Random(daily_seed("chain"))
        pool = list(D._CHAIN_GRAPH.keys())
        for _ in range(200):
            start = rng.choice(pool); end = rng.choice(pool)
            if start == end: continue
            path = D._chain_bfs(start, end)
            if path and cfg["min_hops"] <= len(path)-1 <= cfg["max_hops"]:
                return {"start":start,"end":end,"chain":[start],
                        "optimal":len(path)-1,"steps_left":cfg["max_steps"],
                        "solved":False,"failed":False,"diff":diff_key,"daily":True}
    else:
        start, end, path = D._pick_chain_pair(cfg["min_hops"], cfg["max_hops"])
    return {"start":start,"end":end,"chain":[start],"optimal":len(path)-1,
            "steps_left":cfg["max_steps"],"solved":False,"failed":False,
            "diff":diff_key,"daily":daily}

def render_chain():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🔗 CADENA DE PILOTOS</h2>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#888;font-size:0.9rem;margin-bottom:12px'>"
                "Conectá los dos pilotos pasando por compañeros de equipo reales</p>",
                unsafe_allow_html=True)
    ss("chain_total",0)

    c1,c2,c3,c4 = st.columns([2,1,1,1])
    with c1:
        diff = st.selectbox("Dificultad", list(CHAIN_DIFFS.keys()), key="chain_diff_sel", index=1)
    with c2:
        if st.button("🆕 Nueva Cadena", use_container_width=True, type="primary"):
            st.session_state.chain_state = init_chain(diff); st.rerun()
    with c3:
        if st.button("📅 Diario", use_container_width=True):
            key = f"chain-daily-{datetime.date.today().isoformat()}"
            if already_played(key): st.warning("Ya jugaste la Cadena del día.")
            else: st.session_state.chain_state = init_chain(diff, daily=True); st.rerun()
    with c4:
        st.metric("⭐ Total", st.session_state.chain_total)

    cs = st.session_state.chain_state
    if cs is None:
        st.info("Presioná **Nueva Cadena** para empezar."); return

    # Header: inicio y destino
    meta_a = D.SERIES_F1.drivers_meta.get(cs["start"],{})
    meta_b = D.SERIES_F1.drivers_meta.get(cs["end"],{})
    ca, cm, cb = st.columns([2,1,2])
    with ca:
        st.markdown(
            f"<div style='background:#1a0000;border:2px solid #e10600;border-radius:8px;"
            f"padding:16px;text-align:center'>"
            f"<div style='font-size:2rem'>{flag(meta_a.get('nationality',''))}</div>"
            f"<div style='font-family:Rajdhani;font-size:1.1rem;font-weight:700;color:#e10600'>"
            f"{fmt(cs['start'])}</div><div style='font-size:0.7rem;color:#666'>INICIO</div></div>",
            unsafe_allow_html=True)
    with cm:
        st.markdown(
            f"<div style='text-align:center;padding:20px 0;font-family:Rajdhani;font-size:0.9rem;color:#888'>"
            f"⏩ {cs['optimal']} saltos óptimo<br>🔢 {cs['steps_left']} pasos restantes</div>",
            unsafe_allow_html=True)
    with cb:
        st.markdown(
            f"<div style='background:#001a00;border:2px solid #2e7d32;border-radius:8px;"
            f"padding:16px;text-align:center'>"
            f"<div style='font-size:2rem'>{flag(meta_b.get('nationality',''))}</div>"
            f"<div style='font-family:Rajdhani;font-size:1.1rem;font-weight:700;color:#2e7d32'>"
            f"{fmt(cs['end'])}</div><div style='font-size:0.7rem;color:#666'>DESTINO</div></div>",
            unsafe_allow_html=True)

    # Cadena construida
    if len(cs["chain"]) > 1 or cs["solved"] or cs["failed"]:
        chain_parts = []
        for i, driver in enumerate(cs["chain"]):
            color = "#e10600" if i==0 else "#2e7d32" if driver==cs["end"] else "#ffd700"
            chain_parts.append(
                f"<span style='background:#1a1a1a;border:1px solid {color};"
                f"border-radius:4px;padding:2px 8px;color:{color}'>{fmt(driver)}</span>")
            if i < len(cs["chain"])-1:
                teams = D._chain_teams_between(driver, cs["chain"][i+1])
                team_str = teams[0] if teams else "?"
                chain_parts.append(f"<span style='color:#444;font-size:0.85rem'> →[{team_str}]→ </span>")
        st.markdown(
            "<div style='margin:12px 0;font-family:monospace;font-size:13px'>"
            f"<b style='color:#aaa'>Tu cadena:</b><br>" + "".join(chain_parts) + "</div>",
            unsafe_allow_html=True)

    # Resultado final
    if cs["solved"]:
        hops  = len(cs["chain"])-1
        bonus = max(0, cs["optimal"]-hops+1)
        pts   = CHAIN_DIFFS[cs["diff"]]["pts_base"] + bonus*100
        msg   = f"🏆 ¡RESUELTO en {hops} saltos! (óptimo: {cs['optimal']}) — +{pts} pts"
        if hops <= cs["optimal"]: msg += " 🌟 ¡CADENA ÓPTIMA!"
        st.success(msg)
        add_points(pts); st.session_state.chain_total += pts
        if cs["daily"]: mark_played(f"chain-daily-{datetime.date.today().isoformat()}")
        cs["solved"] = False  # evitar doble suma
        st.session_state.chain_state = cs
    elif cs["failed"]:
        st.error("❌ Sin pasos restantes. Presioná **Nueva Cadena** para seguir.")

    # Input siguiente eslabón
    if not cs["failed"] and not cs.get("done"):
        current   = cs["chain"][-1]
        neighbors = sorted(D._CHAIN_GRAPH.get(current,set()) - set(cs["chain"]))

        if current == cs["end"]:
            cs["done"] = True; st.session_state.chain_state = cs; st.rerun()

        st.markdown(f"<div style='font-size:0.85rem;color:#888;margin:8px 0'>"
                    f"Compañeros de <b style='color:#ffd700'>{fmt(current)}</b>: {len(neighbors)} disponibles</div>",
                    unsafe_allow_html=True)

        sel_options = [""]+[fmt(n) for n in neighbors]
        selected = st.selectbox("Siguiente eslabón", sel_options, key=f"chain_sel_{len(cs['chain'])}")

        # Feedback preview
        if selected:
            norm_sel = normalize(selected)
            if norm_sel == cs["end"]:
                st.markdown("<span style='color:#00c853;font-size:0.9rem'>🎯 ¡Este es el destino!</span>",
                            unsafe_allow_html=True)
            elif norm_sel in D._CHAIN_GRAPH.get(cs["end"],set()):
                st.markdown("<span style='color:#ffd700;font-size:0.9rem'>🔥 ¡Está a 1 paso del destino!</span>",
                            unsafe_allow_html=True)

        if st.button("➕ Agregar eslabón", type="primary", disabled=not selected):
            norm_sel = normalize(selected)
            cs["chain"].append(norm_sel)
            cs["steps_left"] -= 1
            if norm_sel == cs["end"]:
                cs["solved"] = True
            elif cs["steps_left"] <= 0:
                cs["failed"] = True
            st.session_state.chain_state = cs; st.rerun()

# ══════════════════════════════════════════════════════════════════
#  MODO 8 — ¿QUIÉN GANÓ?
# ══════════════════════════════════════════════════════════════════
def _build_whowon_pool():
    return [(yr, gp, results[0]) for yr, gps in D.GP_RESULTS.items()
            for gp, results in gps.items() if results]

def _all_whowon_winners(pool):
    return list({r[2] for r in pool})

def init_whowon(daily=False):
    pool = _build_whowon_pool()
    if daily:
        rng = random.Random(daily_seed("whowon"))
        yr, gp, winner = rng.choice(pool)
    else:
        yr, gp, winner = random.choice(pool)
    all_w = [w for w in _all_whowon_winners(pool) if w != winner]
    distractors = random.sample(all_w, min(3, len(all_w)))
    options = [winner]+distractors; random.shuffle(options)
    return {"year":yr,"gp":gp,"winner":winner,"options":options,
            "answered":False,"correct":None,"pts":0,"daily":daily,
            "t0":time.time()}

def render_whowon():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🏁 ¿QUIÉN GANÓ?</h2>",
                unsafe_allow_html=True)
    ss("whowon_streak",0); ss("whowon_best",0); ss("whowon_total",0); ss("whowon_correct",0); ss("whowon_games",0)

    c1,c2,c3 = st.columns([1,1,2])
    with c1:
        if st.button("🆕 Nueva Pregunta", use_container_width=True, type="primary"):
            st.session_state.whowon_state = init_whowon(); st.rerun()
    with c2:
        if st.button("📅 Diario", use_container_width=True):
            key = f"whowon-daily-{datetime.date.today().isoformat()}"
            if already_played(key): st.warning("Ya jugaste ¿Quién Ganó? del día.")
            else: st.session_state.whowon_state = init_whowon(daily=True); st.rerun()
    with c3:
        pct = int(st.session_state.whowon_correct/st.session_state.whowon_games*100) if st.session_state.whowon_games else 0
        st.markdown(f"<div style='font-family:Rajdhani;font-size:1rem;color:#888;padding:8px 0'>"
                    f"🔥 {st.session_state.whowon_streak} · ✅ {st.session_state.whowon_correct}/{st.session_state.whowon_games} ({pct}%) · "
                    f"⭐ {st.session_state.whowon_total}</div>",unsafe_allow_html=True)

    ws = st.session_state.whowon_state
    if ws is None:
        st.info("Presioná **Nueva Pregunta** para empezar."); return

    daily_badge = " 📅" if ws["daily"] else ""
    st.markdown(
        f"<div style='background:#111;border:2px solid #e10600;border-radius:10px;"
        f"padding:20px 24px;margin:12px 0;text-align:center'>"
        f"<div style='font-family:Rajdhani;font-size:0.85rem;color:#888;margin-bottom:6px'>"
        f"¿QUIÉN GANÓ?{daily_badge}</div>"
        f"<div style='font-size:1.8rem;font-weight:700;font-family:Rajdhani;color:#ffd700'>"
        f"{ws['year']} — {ws['gp'].upper()}</div></div>",
        unsafe_allow_html=True)

    if not ws["answered"]:
        c1, c2 = st.columns(2)
        for i, opt in enumerate(ws["options"]):
            meta = D.SERIES_F1.drivers_meta.get(opt,{})
            nat  = meta.get("nationality","")
            f    = flag(nat)
            col  = c1 if i % 2 == 0 else c2
            with col:
                if st.button(f"{f} {fmt(opt)}", key=f"whowon_opt_{i}", use_container_width=True):
                    elapsed = time.time() - ws["t0"]
                    ws["answered"] = True
                    ws["correct"]  = (opt == ws["winner"])
                    ws["chosen"]   = opt
                    ws["elapsed"]  = elapsed
                    st.session_state.whowon_games += 1
                    if ws["correct"]:
                        st.session_state.whowon_correct += 1
                        st.session_state.whowon_streak  += 1
                        st.session_state.whowon_best = max(st.session_state.whowon_streak, st.session_state.whowon_best)
                        if   elapsed <  3: pts = 500
                        elif elapsed <  6: pts = 400
                        elif elapsed < 10: pts = 300
                        elif elapsed < 20: pts = 200
                        else:              pts = 100
                        ws["pts"] = pts
                        st.session_state.whowon_total += pts; add_points(pts)
                    else:
                        st.session_state.whowon_streak = 0; ws["pts"] = 0
                    if ws["daily"]: mark_played(f"whowon-daily-{datetime.date.today().isoformat()}")
                    st.session_state.whowon_state = ws; st.rerun()
    else:
        ok      = ws["correct"]; pts = ws["pts"]
        color   = "#00c853" if ok else "#ef9a9a"
        bg      = "#0a2a0a" if ok else "#2a0a0a"
        border  = "#2e7d32" if ok else "#c62828"
        icon    = "✅" if ok else "❌"
        secs    = ws.get("elapsed",0)
        msg     = f"{icon} ¡CORRECTO! +{pts} pts ({secs:.1f}s)" if ok else f"{icon} INCORRECTO — Era {fmt(ws['winner'])}"

        opts_html = "<div style='display:flex;flex-wrap:wrap;gap:8px;margin:10px 0'>"
        for opt in ws["options"]:
            if opt == ws["winner"]:       c,bc,bg2 = "#00c853","#2e7d32","#0a2a0a"
            elif opt==ws.get("chosen"):   c,bc,bg2 = "#ef9a9a","#c62828","#2a0a0a"
            else:                          c,bc,bg2 = "#555","#333","#0a0a0a"
            opts_html += (f"<span style='background:{bg2};border:1px solid {bc};"
                          f"border-radius:6px;padding:6px 14px;font-family:monospace;"
                          f"font-size:13px;color:{c}'>{flag(D.SERIES_F1.drivers_meta.get(opt,{}).get('nationality',''))} {fmt(opt)}</span>")
        opts_html += "</div>"

        meta_w = D.SERIES_F1.drivers_meta.get(ws["winner"],{})
        wins_w = meta_w.get("wins","?"); champs_w = meta_w.get("champion",0)
        champ_str = f" · 🏆×{champs_w}" if champs_w else ""

        st.markdown(
            f"<div style='background:{bg};border:2px solid {border};"
            f"border-radius:8px;padding:12px 16px;font-family:monospace'>"
            f"<div style='font-size:15px;color:{color};margin-bottom:8px'>{msg}</div>"
            f"{opts_html}"
            f"<div style='font-size:11px;color:#666;margin-top:6px'>"
            f"{fmt(ws['winner'])} — {wins_w} victorias en F1{champ_str}</div></div>",
            unsafe_allow_html=True)

        if st.button("▶️ Siguiente", type="primary"):
            st.session_state.whowon_state = init_whowon(); st.rerun()

# ══════════════════════════════════════════════════════════════════
#  MODO 9 — ¿EN QUÉ CIRCUITO?
# ══════════════════════════════════════════════════════════════════
PTS_PER_PISTA = [600, 450, 300, 200, 100, 50]

def init_circuit(daily=False, vistos=None):
    all_keys = list(D.F1_CIRCUITS.keys())
    if daily:
        rng = random.Random(daily_seed("circuit"))
        key = rng.choice(all_keys)
        others = [k for k in all_keys if k != key]
        distractors = rng.sample(others, min(3,len(others)))
    else:
        vistos = vistos or set()
        available = [k for k in all_keys if k not in vistos]
        if not available: available = all_keys
        key = random.choice(available)
        others = [k for k in all_keys if k != key]
        distractors = random.sample(others, min(3,len(others)))
    options = [key]+distractors; random.shuffle(options)
    return {"key":key,"options":options,"pistas_vistas":1,"answered":False,
            "correct":None,"daily":daily}

def render_circuit():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🗺️ ¿EN QUÉ CIRCUITO?</h2>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#888;font-size:0.9rem;margin-bottom:12px'>"
                "Pistas progresivas · Menos pistas usadas = más puntos · 24 circuitos F1</p>",
                unsafe_allow_html=True)
    ss("circuit_streak",0); ss("circuit_best",0); ss("circuit_score",0)
    ss("circuit_total",0); ss("circuit_correct",0); ss("circuit_vistos",set())

    c1,c2,c3 = st.columns([1,1,2])
    with c1:
        if st.button("🆕 Nuevo Circuito", use_container_width=True, type="primary"):
            st.session_state.circuit_vistos.add(
                st.session_state.circuit_state["key"] if st.session_state.circuit_state else "")
            st.session_state.circuit_state = init_circuit(vistos=st.session_state.circuit_vistos)
            st.rerun()
    with c2:
        if st.button("📅 Diario", use_container_width=True):
            key = f"circuit-daily-{datetime.date.today().isoformat()}"
            if already_played(key): st.warning("Ya jugaste el Circuito del día.")
            else: st.session_state.circuit_state = init_circuit(daily=True); st.rerun()
    with c3:
        pct = int(st.session_state.circuit_correct/st.session_state.circuit_total*100) if st.session_state.circuit_total else 0
        st.markdown(
            f"<div style='font-family:Rajdhani;font-size:1rem;color:#888;padding:8px 0'>"
            f"🔥 {st.session_state.circuit_streak} · ✅ {st.session_state.circuit_correct}/{st.session_state.circuit_total} ({pct}%) · "
            f"🏅 {st.session_state.circuit_best} · ⭐ {st.session_state.circuit_score}</div>",
            unsafe_allow_html=True)

    cs = st.session_state.circuit_state
    if cs is None:
        st.info("Presioná **Nuevo Circuito** para empezar."); return

    data = D.F1_CIRCUITS[cs["key"]]
    total_pistas = len(data["caracteristicas"])
    pts_ahora    = PTS_PER_PISTA[min(cs["pistas_vistas"]-1, len(PTS_PER_PISTA)-1)]

    # Mostrar pistas
    st.markdown(f"<div style='color:#888;font-size:0.85rem;margin-bottom:8px'>"
                f"Pistas vistas: <b style='color:#fff'>{cs['pistas_vistas']}/{total_pistas}</b>"
                + (f" · <span style='color:#ffd700'>+{pts_ahora} pts si acertás ahora</span>" if not cs["answered"] else "")
                + "</div>", unsafe_allow_html=True)

    for i in range(cs["pistas_vistas"]):
        if i < len(data["caracteristicas"]):
            pts_si = PTS_PER_PISTA[min(i, len(PTS_PER_PISTA)-1)]
            pts_label = f" · {pts_si} pts" if not cs["answered"] else ""
            st.markdown(
                f"<div style='background:#111;border-left:3px solid #1565c0;"
                f"border-radius:0 6px 6px 0;padding:8px 14px;margin:4px 0;"
                f"font-size:0.95rem;color:#ddd'>"
                f"<span style='color:#555;font-size:0.75rem'>PISTA {i+1}{pts_label}</span>"
                f"<br>{data['caracteristicas'][i]}</div>",
                unsafe_allow_html=True)

    if not cs["answered"]:
        # Botón ver más pistas
        if cs["pistas_vistas"] < total_pistas:
            if st.button("💡 Ver otra pista"):
                cs["pistas_vistas"] += 1
                st.session_state.circuit_state = cs; st.rerun()

        # Opciones
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        for i, opt_key in enumerate(cs["options"]):
            opt_d = D.F1_CIRCUITS[opt_key]
            f     = CIRCUIT_FLAGS.get(opt_d["pais"],"🏁")
            col   = c1 if i % 2 == 0 else c2
            with col:
                if st.button(f"{f} {opt_d['display']}", key=f"circuit_opt_{i}",
                             use_container_width=True):
                    correct = (opt_key == cs["key"])
                    cs["answered"] = True; cs["correct"] = correct; cs["chosen"] = opt_key
                    st.session_state.circuit_total += 1
                    if correct:
                        st.session_state.circuit_correct += 1
                        st.session_state.circuit_streak  += 1
                        if st.session_state.circuit_streak > st.session_state.circuit_best:
                            st.session_state.circuit_best = st.session_state.circuit_streak
                        pts_idx = min(cs["pistas_vistas"]-1, len(PTS_PER_PISTA)-1)
                        pts     = PTS_PER_PISTA[pts_idx]
                        if st.session_state.circuit_streak > 1:
                            pts += min(st.session_state.circuit_streak-1,5)*30
                        cs["pts_earned"] = pts
                        st.session_state.circuit_score += pts; add_points(pts)
                    else:
                        st.session_state.circuit_streak = 0; cs["pts_earned"] = 0
                    if cs["daily"]: mark_played(f"circuit-daily-{datetime.date.today().isoformat()}")
                    st.session_state.circuit_state = cs; st.rerun()
    else:
        # Resultado
        ok = cs["correct"]; pts = cs.get("pts_earned",0)
        color  = "#00c853" if ok else "#ef9a9a"
        bg     = "#0a2a0a" if ok else "#2a0a0a"
        border = "#2e7d32" if ok else "#c62828"
        icon   = "✅" if ok else "❌"
        streak_bonus = (min(st.session_state.circuit_streak-1,5)*30
                        if ok and st.session_state.circuit_streak>1 else 0)
        if ok:
            msg = f"{icon} ¡CORRECTO! +{pts} pts" + (f" (racha ×{st.session_state.circuit_streak} +{streak_bonus})" if streak_bonus else "")
        else:
            msg = f"{icon} INCORRECTO — Era <b style='color:#ffd700'>{data['display']}</b>"

        # Opciones coloreadas
        opts_html = "<div style='display:flex;flex-wrap:wrap;gap:8px;margin:10px 0'>"
        for opt_key in cs["options"]:
            opt_d = D.F1_CIRCUITS[opt_key]; f = CIRCUIT_FLAGS.get(opt_d["pais"],"🏁")
            if opt_key == cs["key"]:                    c,bc,bg2 = "#00c853","#2e7d32","#0a2a0a"
            elif opt_key == cs.get("chosen") and not ok: c,bc,bg2 = "#ef9a9a","#c62828","#2a0a0a"
            else:                                         c,bc,bg2 = "#555","#333","#0a0a0a"
            opts_html += (f"<span style='background:{bg2};border:1px solid {bc};"
                          f"border-radius:6px;padding:6px 14px;font-family:monospace;"
                          f"font-size:13px;color:{c}'>{f} {opt_d['display']}</span>")
        opts_html += "</div>"

        win_str   = " · ".join(w.title() for w in data["ganadores"][:3])
        info_html = (f"<div style='font-size:11px;color:#666;margin-top:6px'>"
                     f"📍 {data['ciudad']}, {data['pais']} &nbsp;·&nbsp; "
                     f"📏 {data['longitud']} km &nbsp;·&nbsp; "
                     f"🏁 Primer GP: {data['primer_gp']}<br>"
                     f"🏆 Ganadores históricos: {win_str}<br>"
                     f"💬 Apodo: <i>{data.get('apodo','')}</i></div>")

        st.markdown(
            f"<div style='background:{bg};border:2px solid {border};"
            f"border-radius:8px;padding:12px 16px;font-family:monospace'>"
            f"<div style='font-size:15px;color:{color};margin-bottom:8px'>{msg}</div>"
            f"{opts_html}{info_html}</div>",
            unsafe_allow_html=True)

        # Todas las pistas reveladas
        with st.expander("Ver todas las pistas"):
            for i, pista in enumerate(data["caracteristicas"]):
                op = "1.0" if i < cs["pistas_vistas"] else "0.4"
                st.markdown(
                    f"<div style='opacity:{op};font-size:0.85rem;color:#aaa;"
                    f"padding:3px 8px;border-left:2px solid #333;margin:2px 0'>"
                    f"Pista {i+1}: {pista}</div>",
                    unsafe_allow_html=True)

        if st.button("▶️ Siguiente Circuito", type="primary"):
            st.session_state.circuit_vistos.add(cs["key"])
            st.session_state.circuit_state = init_circuit(vistos=st.session_state.circuit_vistos)
            st.rerun()

# ══════════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ══════════════════════════════════════════════════════════════════
render_header()

mode = st.session_state.mode
if   mode == "home":        render_home()
elif mode == "grid":        render_grid()
elif mode == "podium":      render_podium()
elif mode == "duel":        render_duel()
elif mode == "constructor": render_constructor()
elif mode == "timeline":    render_timeline()
elif mode == "mystery":     render_mystery()
elif mode == "chain":       render_chain()
elif mode == "whowon":      render_whowon()
elif mode == "circuit":     render_circuit()
