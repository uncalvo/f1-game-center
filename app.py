"""
F1 Game Center — Streamlit app
Requiere: pip install streamlit
Ejecutar: streamlit run app.py
"""
import streamlit as st
import random
import hashlib
import datetime
import json
import pathlib
import unicodedata

# ── Importar lógica de datos ──────────────────────────────────────
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

# ── CSS global ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1,h2,h3 { font-family: 'Rajdhani', sans-serif !important; }

/* Ocultar header de Streamlit */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 1rem; max-width: 1100px; }

/* Botones */
.stButton > button {
    border-radius: 6px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    font-size: 15px;
    letter-spacing: 0.5px;
    transition: all 0.15s;
}
.stButton > button:hover { transform: translateY(-1px); }

/* Celda de grid */
.grid-cell { 
    border: 2px solid #333;
    border-radius: 8px;
    padding: 6px;
    background: #111;
    min-height: 60px;
    text-align: center;
}
.grid-cell.correct { border-color: #2e7d32 !important; background: #0a1f0a !important; }
.grid-cell.wrong   { border-color: #c62828 !important; background: #1f0a0a !important; }
.grid-cell.repeat  { border-color: #e65100 !important; }

/* Header de categoría */
.cat-header {
    background: #1a1a2e;
    border-radius: 6px;
    padding: 6px 8px;
    font-size: 12px;
    font-weight: 600;
    text-align: center;
    color: #ddd;
    min-height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Tarjetas de modo */
.mode-card {
    background: #111;
    border: 1px solid #222;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}
.mode-card:hover { border-color: #e10600; transform: translateY(-2px); }

/* Separador rojo F1 */
.f1-divider {
    height: 3px;
    background: linear-gradient(90deg, #e10600, #ff6b35, #e10600);
    border-radius: 2px;
    margin: 8px 0 16px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PERSISTENCIA (JSON local)
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

def flag(nat: str) -> str:
    return FLAGS.get(nat, "🏁")

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════
def ss(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

ss("mode", "home")
ss("grid_state", None)
ss("podium_state", None)
ss("duel_state", None)
ss("constructor_state", None)
ss("timeline_state", None)
ss("mystery_state", None)

# ══════════════════════════════════════════════════════════════════
#  HEADER GLOBAL
# ══════════════════════════════════════════════════════════════════
def render_header():
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        st.markdown(
            "<h1 style='font-family:Rajdhani;color:#e10600;margin:0;font-size:2.2rem'>"
            "🏎️ F1 GAME CENTER</h1>"
            "<div class='f1-divider'></div>",
            unsafe_allow_html=True,
        )
    with c2:
        pts = get_total_pts()
        st.metric("⭐ Puntos", f"{pts:,}")
    with c3:
        if st.session_state.mode != "home":
            if st.button("🏠 Inicio", use_container_width=True):
                st.session_state.mode = "home"
                st.rerun()

# ══════════════════════════════════════════════════════════════════
#  HOME — SELECTOR DE MODO
# ══════════════════════════════════════════════════════════════════
MODES = [
    ("🔲", "Grid Challenge",       "grid",        "Completá el grid F1/F2/F3 con pilotos"),
    ("🏆", "Podium Challenge",     "podium",      "Adiviná el top 10 de un GP histórico"),
    ("⚔️",  "Duelo de Pilotos",    "duel",        "¿Quién tiene más? Victorias · Podios · Títulos"),
    ("🏗️", "Constructor Challenge","constructor", "Adivina la escudería que cumple la condición"),
    ("📅", "Línea de Tiempo",      "timeline",    "Ordená 5 eventos F1 cronológicamente"),
    ("🕵️", "¿Quién Soy?",         "mystery",     "Adiviná el piloto con las mínimas pistas"),
]

def render_home():
    st.markdown(
        "<p style='color:#888;font-size:1rem;margin-bottom:24px'>"
        "Elegí un modo para jugar</p>",
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    for i, (icon, name, mode_key, desc) in enumerate(MODES):
        with cols[i % 3]:
            st.markdown(
                f"<div style='background:#111;border:1px solid #222;border-radius:12px;"
                f"padding:20px;text-align:center;margin-bottom:12px'>"
                f"<div style='font-size:2.2rem'>{icon}</div>"
                f"<div style='font-family:Rajdhani;font-size:1.3rem;font-weight:700;"
                f"color:#f0f0f0;margin:6px 0 4px'>{name}</div>"
                f"<div style='font-size:0.8rem;color:#777'>{desc}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            if st.button(f"Jugar", key=f"btn_mode_{mode_key}", use_container_width=True):
                st.session_state.mode = mode_key
                st.rerun()

# ══════════════════════════════════════════════════════════════════
#  MODO 1 — GRID CHALLENGE
# ══════════════════════════════════════════════════════════════════
def init_grid(series_name, difficulty, daily=False):
    series = D.SERIES_MAP[series_name]
    cfg    = D.DIFFICULTY_CONFIG[difficulty]
    size   = cfg["grid_size"]

    if daily:
        rng_state = random.getstate()
        random.seed(daily_seed(f"grid-{series_name}-{difficulty}"))
        row_cats, col_cats = series.generate_grid(cfg)
        random.setstate(rng_state)
    else:
        row_cats, col_cats = series.generate_grid(cfg)

    return {
        "series_name": series_name,
        "difficulty":  difficulty,
        "daily":       daily,
        "size":        size,
        "row_cats":    row_cats,
        "col_cats":    col_cats,
        "answers":     {},          # {(r,c): driver_name}
        "results":     {},          # {(r,c): "correct"|"wrong"|"repeat"|"notfound"}
        "checked":     False,
        "correct":     0,
        "score":       0,
        "start_time":  datetime.datetime.now().isoformat(),
        "finished":    False,
        "used":        set(),
    }

def render_grid():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🔲 GRID CHALLENGE</h2>",
                unsafe_allow_html=True)

    # ── Controles ────────────────────────────────────────────────
    col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
    with col1:
        series_name = st.selectbox(
            "Serie", list(D.SERIES_MAP.keys()),
            key="grid_series",
            index=0,
        )
    with col2:
        difficulty = st.selectbox(
            "Dificultad", list(D.DIFFICULTY_CONFIG.keys()),
            key="grid_diff",
            index=1,
        )
    with col3:
        if st.button("🆕 Nuevo Grid", use_container_width=True, type="primary"):
            st.session_state.grid_state = init_grid(series_name, difficulty)
            st.rerun()
    with col4:
        daily_key = f"grid-daily-{series_name}-{difficulty}-{datetime.date.today().isoformat()}"
        if st.button("📅 Diario", use_container_width=True):
            if already_played(daily_key):
                st.warning("Ya jugaste el grid del día. ¡Volvé mañana!")
            else:
                st.session_state.grid_state = init_grid(series_name, difficulty, daily=True)
                st.rerun()
    with col5:
        if st.button("💡 Soluciones", use_container_width=True):
            gs = st.session_state.grid_state
            if gs:
                st.session_state.grid_show_solutions = not st.session_state.get("grid_show_solutions", False)
                st.rerun()

    gs = st.session_state.grid_state
    if gs is None:
        st.info("Presioná **Nuevo Grid** para empezar.")
        return

    series  = D.SERIES_MAP[gs["series_name"]]
    size    = gs["size"]
    cfg     = D.DIFFICULTY_CONFIG[gs["difficulty"]]
    row_cats = gs["row_cats"]
    col_cats = gs["col_cats"]

    # ── Colores por serie ────────────────────────────────────────
    COLORS = {
        "🏎️ Fórmula 1": ("#e10600", "#1565c0"),
        "🚀 Fórmula 2": ("#1565c0", "#e10600"),
        "🔵 Fórmula 3": ("#2e7d32", "#1b5e20"),
        "🔀 Modo Mixto": ("#6a1b9a", "#4a148c"),
    }
    col_color, row_color = COLORS.get(gs["series_name"], ("#e10600", "#1565c0"))

    # ── Grid ─────────────────────────────────────────────────────
    all_drivers = sorted(d.title() for d in series.all_drivers)

    # Header row
    header_cols = st.columns([1] + [1]*size)
    header_cols[0].markdown("&nbsp;", unsafe_allow_html=True)
    for c_idx, cc in enumerate(col_cats):
        header_cols[c_idx+1].markdown(
            f"<div style='background:{col_color}22;border:1px solid {col_color}55;"
            f"border-radius:6px;padding:6px;font-size:11px;font-weight:600;"
            f"text-align:center;color:{col_color};min-height:48px;"
            f"display:flex;align-items:center;justify-content:center'>"
            f"{cc['label']}</div>",
            unsafe_allow_html=True,
        )

    # Data rows
    for r_idx, rc in enumerate(row_cats):
        row_cols = st.columns([1] + [1]*size)
        row_cols[0].markdown(
            f"<div style='background:{row_color}22;border:1px solid {row_color}55;"
            f"border-radius:6px;padding:6px;font-size:11px;font-weight:600;"
            f"text-align:center;color:{row_color};min-height:48px;"
            f"display:flex;align-items:center;justify-content:center'>"
            f"{rc['label']}</div>",
            unsafe_allow_html=True,
        )
        for c_idx, cc in enumerate(col_cats):
            key = f"grid_inp_{r_idx}_{c_idx}"
            result = gs["results"].get((r_idx, c_idx), "")
            border = {"correct": "2px solid #2e7d32",
                      "wrong":   "2px solid #c62828",
                      "repeat":  "2px solid #e65100",
                      "notfound":"2px solid #555"}.get(result, "2px solid #333")
            bg     = {"correct": "#0a1f0a",
                      "wrong":   "#1f0a0a"}.get(result, "#0d0d0d")

            with row_cols[c_idx+1]:
                st.markdown(
                    f"<div style='border:{border};border-radius:6px;"
                    f"background:{bg};padding:2px'>",
                    unsafe_allow_html=True,
                )
                current_val = gs["answers"].get((r_idx, c_idx), "")
                val = st.selectbox(
                    label="",
                    options=[""] + all_drivers,
                    index=(all_drivers.index(current_val) + 1
                           if current_val in all_drivers else 0),
                    key=key,
                    label_visibility="collapsed",
                )
                gs["answers"][(r_idx, c_idx)] = val
                st.markdown("</div>", unsafe_allow_html=True)

    # ── Verificar ────────────────────────────────────────────────
    st.markdown("")
    btn_c1, btn_c2, _ = st.columns([1, 1, 3])
    with btn_c1:
        if st.button("✔ Verificar", type="primary", use_container_width=True):
            allow_repeat = cfg.get("allow_repeat", False)
            used   = set()
            results = {}
            correct = 0
            total   = size * size
            for r in range(size):
                for c in range(size):
                    raw = gs["answers"].get((r, c), "")
                    driver = normalize(raw)
                    if not driver:
                        results[(r,c)] = ""
                        continue
                    if driver not in series.drivers_meta:
                        results[(r,c)] = "notfound"
                        continue
                    rc2 = row_cats[r]; cc2 = col_cats[c]
                    possible = series.drivers_satisfying(rc2, cc2)
                    if driver in used and (not allow_repeat or len(possible) > 1):
                        results[(r,c)] = "repeat"
                        continue
                    if rc2["check"](driver) and cc2["check"](driver):
                        results[(r,c)] = "correct"
                        used.add(driver)
                        correct += 1
                    else:
                        results[(r,c)] = "wrong"

            gs["results"]  = results
            gs["checked"]  = True
            gs["correct"]  = correct
            elapsed = (datetime.datetime.now() -
                       datetime.datetime.fromisoformat(gs["start_time"])).seconds
            diff_mult = {"🟢 Fácil":1,"🟡 Medio":2,"🔴 Difícil":3,"💀 Experto":5}
            mult = diff_mult.get(gs["difficulty"], 1)
            base = correct * 100 * mult
            tlim = cfg.get("time_limit")
            bonus = max(0, tlim - elapsed) * 5 * mult if tlim else 0
            gs["score"] = base + bonus
            gs["elapsed"] = elapsed

            if correct == total:
                gs["finished"] = True
                add_points(gs["score"])
                if gs["daily"]:
                    mark_played(daily_key)

            st.session_state.grid_state = gs
            st.rerun()

    with btn_c2:
        if gs.get("checked"):
            correct = gs["correct"]
            total   = size * size
            score   = gs["score"]
            color   = "#00c853" if correct == total else "#ffd700" if correct > 0 else "#888"
            st.markdown(
                f"<div style='font-family:Rajdhani;font-size:1.3rem;font-weight:700;"
                f"color:{color};padding:6px 0'>"
                f"✅ {correct}/{total} · ⭐ {score} pts</div>",
                unsafe_allow_html=True,
            )
            if correct == total:
                st.balloons()

    # ── Soluciones ───────────────────────────────────────────────
    if st.session_state.get("grid_show_solutions"):
        st.markdown("---")
        st.markdown("**💡 Soluciones posibles:**")
        for r in range(size):
            for c in range(size):
                sol = sorted(series.drivers_satisfying(row_cats[r], col_cats[c]))
                st.markdown(
                    f"**[{row_cats[r]['label']}] × [{col_cats[c]['label']}]:** "
                    f"{', '.join(fmt(d) for d in sol[:8])}"
                    + (f" ... (+{len(sol)-8})" if len(sol) > 8 else "")
                )

# ══════════════════════════════════════════════════════════════════
#  MODO 2 — PODIUM CHALLENGE
# ══════════════════════════════════════════════════════════════════
def init_podium(year=None, gp=None, daily=False):
    if daily:
        seed = daily_seed("podium")
        rng  = random.Random(seed)
        year = rng.choice(sorted(D.GP_RESULTS.keys()))
        gp   = rng.choice(sorted(D.GP_RESULTS[year].keys()))
    elif year is None or gp is None:
        year = random.choice(sorted(D.GP_RESULTS.keys()))
        gp   = random.choice(sorted(D.GP_RESULTS[year].keys()))

    answer = [normalize(d) for d in D.GP_RESULTS[year][gp]]
    return {
        "year": year, "gp": gp, "answer": answer,
        "inputs": [""] * 10,
        "results": [],
        "checked": False,
        "score":   0,
        "daily":   daily,
    }

def render_podium():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🏆 PODIUM CHALLENGE</h2>",
                unsafe_allow_html=True)

    all_f1 = sorted(d.title() for d in D.RAW_F1.keys())
    decades = ["Todos"] + [f"{d}s" for d in range(1950, 2030, 10) if any(
        (d//10)*10 <= y < (d//10)*10+10 for y in D.GP_RESULTS)]

    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        dec_filter = st.selectbox("Filtrar por época", decades, key="podium_dec")
    with c2:
        if st.button("🎲 Aleatorio", use_container_width=True, type="primary"):
            filtered_years = [y for y in D.GP_RESULTS
                              if dec_filter == "Todos" or
                              str((y//10)*10) + "s" == dec_filter]
            if filtered_years:
                yr = random.choice(filtered_years)
                gp = random.choice(list(D.GP_RESULTS[yr].keys()))
                st.session_state.podium_state = init_podium(yr, gp)
                st.rerun()
    with c3:
        if st.button("📅 Diario", use_container_width=True):
            key = f"podium-daily-{datetime.date.today().isoformat()}"
            if already_played(key):
                st.warning("Ya jugaste el Podio del día. ¡Volvé mañana!")
            else:
                st.session_state.podium_state = init_podium(daily=True)
                st.rerun()
    with c4:
        ps = st.session_state.podium_state
        if ps and ps.get("checked") and st.button("🔄 Otro GP", use_container_width=True):
            st.session_state.podium_state = None
            st.rerun()

    ps = st.session_state.podium_state
    if ps is None:
        st.info("Presioná **Aleatorio** o **Diario** para empezar.")
        return

    st.markdown(
        f"<div style='background:#1a1a1a;border:1px solid #333;border-radius:10px;"
        f"padding:16px;margin:12px 0'>"
        f"<h3 style='font-family:Rajdhani;color:#ffd700;margin:0'>"
        f"🏁 {ps['gp']} {ps['year']}</h3>"
        f"<p style='color:#888;margin:4px 0 0;font-size:0.85rem'>"
        f"Ingresá los 10 pilotos en orden — P1 a P10</p></div>",
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i in range(10):
        col = cols[i % 2]
        with col:
            result = ps["results"][i] if ps.get("checked") and i < len(ps["results"]) else None
            color_map = {
                "correct_pos":  ("🟢", "#00c853"),
                "correct_any":  ("🟡", "#ffd700"),
                "wrong":        ("🔴", "#c62828"),
                "empty":        ("⚪", "#555"),
            }
            icon, color = color_map.get(result or "empty", ("⚪", "#555"))
            prefix = f"P{i+1}"
            val = st.selectbox(
                f"{icon} {prefix}",
                [""] + all_f1,
                index=(all_f1.index(ps["inputs"][i]) + 1
                       if ps["inputs"][i] in all_f1 else 0),
                key=f"podium_inp_{i}",
                label_visibility="visible",
            )
            ps["inputs"][i] = val

    st.markdown("")
    b1, b2 = st.columns([1, 3])
    with b1:
        if st.button("✔ Verificar", type="primary", use_container_width=True,
                     disabled=ps.get("checked", False)):
            answer  = ps["answer"]
            results = []
            pts = 0
            for i in range(10):
                raw    = normalize(ps["inputs"][i])
                if not raw:
                    results.append("empty")
                    continue
                driver = raw
                if driver == (answer[i] if i < len(answer) else ""):
                    results.append("correct_pos")
                    pts += 100
                elif driver in answer:
                    results.append("correct_any")
                    pts += 20
                else:
                    results.append("wrong")
            ps["results"] = results
            ps["checked"] = True
            ps["score"]   = pts
            add_points(pts)
            if ps["daily"]:
                mark_played(f"podium-daily-{datetime.date.today().isoformat()}")
            st.session_state.podium_state = ps
            st.rerun()

    with b2:
        if ps.get("checked"):
            correct_pos = ps["results"].count("correct_pos")
            correct_any = ps["results"].count("correct_any")
            st.markdown(
                f"<div style='font-family:Rajdhani;font-size:1.2rem;padding:6px 0'>"
                f"🟢 {correct_pos} exactos · 🟡 {correct_any} en el top10 · "
                f"⭐ <b>{ps['score']} pts</b></div>",
                unsafe_allow_html=True,
            )

    if ps.get("checked"):
        with st.expander("🏁 Ver resultado completo"):
            answer = D.GP_RESULTS[ps["year"]][ps["gp"]]
            for i, d in enumerate(answer):
                res = ps["results"][i] if i < len(ps["results"]) else "empty"
                icon = {"correct_pos":"🟢","correct_any":"🟡","wrong":"🔴","empty":"⚪"}.get(res,"⚪")
                inp = ps["inputs"][i]
                marker = f" ← ✅ {fmt(d)}" if res == "correct_pos" else \
                         f" ← ⚠️ era {fmt(d)}" if res in ("correct_any","wrong","empty") else ""
                st.markdown(f"**P{i+1}** {icon} {inp or '_(vacío)_'}{marker}")

# ══════════════════════════════════════════════════════════════════
#  MODO 3 — DUELO DE PILOTOS
# ══════════════════════════════════════════════════════════════════
DUEL_STATS = {
    "wins":     ("🏆 VICTORIAS",   "victorias"),
    "podiums":  ("🥇 PODIOS",      "podios"),
    "champion": ("👑 CAMPEONATOS", "campeonatos"),
}

def get_stat(driver: str, stat: str) -> int:
    m = D.SERIES_F1.drivers_meta[driver]
    if stat == "champion":
        c = m["champion"]
        return c if isinstance(c, int) else (1 if c else 0)
    return m[stat]

def pick_duel_pair(stat: str):
    pool = [d for d, m in D.SERIES_F1.drivers_meta.items() if m["podiums"] >= 1]
    for _ in range(300):
        a, b = random.sample(pool, 2)
        va, vb = get_stat(a, stat), get_stat(b, stat)
        if va != vb:
            return a, b, va, vb
    a, b = random.sample(pool, 2)
    return a, b, get_stat(a, stat), get_stat(b, stat)

def init_duel(daily=False):
    stat = random.choice(list(DUEL_STATS.keys()))
    if daily:
        rng  = random.Random(daily_seed("duel"))
        pool = sorted(d for d, m in D.SERIES_F1.drivers_meta.items() if m["podiums"] >= 1)
        stat = list(DUEL_STATS.keys())[rng.randint(0, 2)]
        for _ in range(300):
            a, b = rng.sample(pool, 2)
            va, vb = get_stat(a, stat), get_stat(b, stat)
            if va != vb:
                break
    else:
        a, b, va, vb = pick_duel_pair(stat)
    return {
        "a": a, "b": b, "va": va, "vb": vb,
        "stat": stat, "revealed": False, "correct": None,
        "streak": st.session_state.get("duel_streak", 0),
        "best":   st.session_state.get("duel_best", 0),
        "total":  st.session_state.get("duel_total", 0),
        "daily":  daily,
        "round":  st.session_state.get("duel_round", 0),
    }

def render_duel():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>⚔️ DUELO DE PILOTOS</h2>",
                unsafe_allow_html=True)

    ss("duel_streak", 0); ss("duel_best", 0); ss("duel_total", 0); ss("duel_round", 0)

    c1, c2, c3 = st.columns([1, 1, 3])
    with c1:
        if st.button("🆕 Nueva Partida", use_container_width=True):
            st.session_state.duel_streak = 0
            st.session_state.duel_round  = 0
            st.session_state.duel_state  = init_duel()
            st.rerun()
    with c2:
        if st.button("📅 Duelo del Día", use_container_width=True):
            key = f"duel-daily-{datetime.date.today().isoformat()}"
            if already_played(key):
                st.warning("Ya jugaste el Duelo del día.")
            else:
                st.session_state.duel_streak = 0
                st.session_state.duel_round  = 0
                st.session_state.duel_state  = init_duel(daily=True)
                st.rerun()

    ds = st.session_state.duel_state
    if ds is None:
        st.info("Presioná **Nueva Partida** para empezar.")
        return

    # Stats header
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("🔥 Racha", st.session_state.duel_streak)
    sc2.metric("🏅 Mejor", st.session_state.duel_best)
    sc3.metric("⭐ Puntos", st.session_state.duel_total)

    stat_label, stat_word = DUEL_STATS[ds["stat"]]
    st.markdown(
        f"<div style='text-align:center;font-family:Rajdhani;font-size:1.3rem;"
        f"color:#bbb;padding:12px 0'>¿Quién tiene más "
        f"<span style='color:#ffd700;font-size:1.5rem'>{stat_word.upper()}</span>"
        f" en F1?</div>",
        unsafe_allow_html=True,
    )

    # Cartas
    def driver_card(driver, stat, revealed=False, val=None, winner=False, loser=False):
        meta  = D.SERIES_F1.drivers_meta[driver]
        nat   = meta["nationality"]
        teams = meta["teams"]
        team_str = ", ".join(t.title() for t in teams[:2])
        if len(teams) > 2: team_str += " …"
        border = "#00c853" if winner else ("#c62828" if loser else "#333")
        bg     = "#0a2a0a" if winner else ("#2a0a0a" if loser else "#1a1a1a")
        num    = str(val) if revealed and val is not None else "?"
        num_c  = "#ffd700" if winner else ("#888" if loser else "#f0f0f0")
        return (
            f"<div style='background:{bg};border:2px solid {border};"
            f"border-radius:12px;padding:24px 16px;text-align:center'>"
            f"<div style='font-size:2.5rem'>{flag(nat)}</div>"
            f"<div style='font-family:Rajdhani;font-size:1.3rem;font-weight:700;"
            f"color:#f0f0f0;margin:8px 0 4px'>{fmt(driver)}</div>"
            f"<div style='font-size:0.75rem;color:#666;margin-bottom:12px'>{team_str}</div>"
            f"<div style='font-size:2.5rem;font-weight:700;color:{num_c}'>{num}</div>"
            f"<div style='font-size:0.7rem;color:#555;text-transform:uppercase;"
            f"letter-spacing:2px'>{stat_word}</div></div>"
        )

    ca, cb = st.columns(2)
    revealed = ds.get("revealed", False)
    winner_a = revealed and ds["va"] > ds["vb"]
    winner_b = revealed and ds["vb"] > ds["va"]
    with ca:
        st.markdown(driver_card(ds["a"], ds["stat"], revealed, ds["va"] if revealed else None,
                                winner=winner_a, loser=revealed and not winner_a),
                    unsafe_allow_html=True)
    with cb:
        st.markdown(driver_card(ds["b"], ds["stat"], revealed, ds["vb"] if revealed else None,
                                winner=winner_b, loser=revealed and not winner_b),
                    unsafe_allow_html=True)

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
        fb_text  = f"✅ ¡CORRECTO! +{10 + max(0,ds['streak']-1)*5} pts · Racha: {ds['streak']}" \
                   if ds["correct"] else "❌ INCORRECTO — Racha perdida"
        st.markdown(
            f"<div style='text-align:center;font-family:Rajdhani;font-size:1.4rem;"
            f"font-weight:700;color:{fb_color};padding:12px'>{fb_text}</div>",
            unsafe_allow_html=True,
        )
        bc1, bc2 = st.columns(2)
        with bc1:
            if ds["correct"] and st.button("➡ Siguiente", use_container_width=True, type="primary"):
                st.session_state.duel_round += 1
                st.session_state.duel_state = _next_duel(ds)
                st.rerun()
        with bc2:
            if st.button("🔄 Nueva Partida", use_container_width=True):
                st.session_state.duel_streak = 0
                st.session_state.duel_round  = 0
                st.session_state.duel_state  = init_duel()
                st.rerun()

def _duel_answer(chosen: str, ds: dict):
    va, vb = ds["va"], ds["vb"]
    correct_side = "a" if va > vb else "b"
    correct = chosen == correct_side
    streak  = st.session_state.duel_streak
    if correct:
        streak += 1
        best = max(streak, st.session_state.duel_best)
        pts  = 10 + (streak - 1) * 5
        st.session_state.duel_streak = streak
        st.session_state.duel_best   = best
        st.session_state.duel_total += pts
    else:
        st.session_state.duel_streak = 0
    ds["revealed"] = True
    ds["correct"]  = correct
    ds["streak"]   = st.session_state.duel_streak
    st.session_state.duel_state = ds
    if ds["daily"]:
        mark_played(f"duel-daily-{datetime.date.today().isoformat()}")
    st.rerun()

def _next_duel(ds: dict):
    stat = random.choice(list(DUEL_STATS.keys()))
    a, b, va, vb = pick_duel_pair(stat)
    return {**ds, "a": a, "b": b, "va": va, "vb": vb,
            "stat": stat, "revealed": False, "correct": None,
            "streak": st.session_state.duel_streak,
            "best":   st.session_state.duel_best,
            "total":  st.session_state.duel_total}

# ══════════════════════════════════════════════════════════════════
#  MODO 4 — CONSTRUCTOR CHALLENGE
# ══════════════════════════════════════════════════════════════════
def init_constructor():
    cats = D.CONSTRUCTOR_CATS
    valid_cats = [c for c in cats if len([t for t in D.RAW_CONSTRUCTORS
                                          if c["check"](t)]) >= 2]
    row_cats = random.sample(valid_cats, 3)
    remaining = [c for c in valid_cats if c not in row_cats]
    col_cats = random.sample(remaining, 3)
    grid = {}
    for r, rc in enumerate(row_cats):
        for c, cc in enumerate(col_cats):
            valid = [t for t in D.RAW_CONSTRUCTORS if rc["check"](t) and cc["check"](t)]
            grid[(r, c)] = {"valid": valid, "attempts": 3, "answer": "", "solved": False, "failed": False}
    return {
        "row_cats": row_cats, "col_cats": col_cats,
        "grid": grid, "score": 0, "finished": False,
    }

def render_constructor():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🏗️ CONSTRUCTOR CHALLENGE</h2>",
                unsafe_allow_html=True)

    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("🆕 Nuevo", use_container_width=True, type="primary"):
            st.session_state.constructor_state = init_constructor()
            st.rerun()

    cs = st.session_state.constructor_state
    if cs is None:
        st.info("Presioná **Nuevo** para empezar.")
        return

    row_cats = cs["row_cats"]; col_cats = cs["col_cats"]; grid = cs["grid"]
    all_constructors = sorted(D.ALL_CONSTRUCTORS)

    # Header
    hcols = st.columns([1.2] + [1]*3)
    hcols[0].markdown("")
    for c_idx, cc in enumerate(col_cats):
        hcols[c_idx+1].markdown(
            f"<div style='background:#1a1a2e;border:1px solid #334;border-radius:6px;"
            f"padding:6px;font-size:11px;font-weight:600;text-align:center;color:#aac;"
            f"min-height:44px;display:flex;align-items:center;justify-content:center'>"
            f"{cc['label']}</div>", unsafe_allow_html=True)

    for r_idx, rc in enumerate(row_cats):
        rcols = st.columns([1.2] + [1]*3)
        rcols[0].markdown(
            f"<div style='background:#1a2a1a;border:1px solid #343;border-radius:6px;"
            f"padding:6px;font-size:11px;font-weight:600;text-align:center;color:#aca;"
            f"min-height:44px;display:flex;align-items:center;justify-content:center'>"
            f"{rc['label']}</div>", unsafe_allow_html=True)
        for c_idx in range(3):
            cell = grid[(r_idx, c_idx)]
            with rcols[c_idx+1]:
                if cell["solved"]:
                    st.markdown(
                        f"<div style='background:#0a2a0a;border:2px solid #2e7d32;"
                        f"border-radius:8px;padding:10px;text-align:center;"
                        f"font-family:Rajdhani;font-size:1rem;color:#00c853'>"
                        f"✅ {cell['answer'].title()}<br>"
                        f"<span style='font-size:0.7rem;color:#666'>"
                        f"{cell['attempts']} intentos restantes</span></div>",
                        unsafe_allow_html=True,
                    )
                elif cell["failed"]:
                    valid_str = ", ".join(t.title() for t in cell["valid"][:3])
                    st.markdown(
                        f"<div style='background:#2a0a0a;border:2px solid #c62828;"
                        f"border-radius:8px;padding:8px;text-align:center;"
                        f"font-size:0.75rem;color:#e57373'>"
                        f"❌ Sin intentos<br><span style='color:#666'>{valid_str}</span></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    val = st.selectbox(
                        f"Intentos: {cell['attempts']}",
                        [""] + all_constructors,
                        key=f"constr_{r_idx}_{c_idx}",
                    )
                    if st.button("OK", key=f"constr_ok_{r_idx}_{c_idx}",
                                 use_container_width=True):
                        if val:
                            if val.lower() in cell["valid"]:
                                cell["solved"] = True
                                cell["answer"] = val
                                pts = 30 * cell["attempts"]
                                cs["score"] += pts
                                add_points(pts)
                            else:
                                cell["attempts"] -= 1
                                if cell["attempts"] == 0:
                                    cell["failed"] = True
                            cs["grid"][(r_idx, c_idx)] = cell
                            st.session_state.constructor_state = cs
                            st.rerun()

    solved = sum(1 for cell in grid.values() if cell["solved"])
    st.markdown(
        f"<div style='font-family:Rajdhani;font-size:1.2rem;color:#ffd700;margin-top:12px'>"
        f"✅ {solved}/9 resueltas · ⭐ {cs['score']} pts</div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════
#  MODO 5 — LÍNEA DE TIEMPO
# ══════════════════════════════════════════════════════════════════
TIMELINE_DIFFS = {
    "🟢 Fácil ×1":  {"mult": 1, "range": 999, "desc": "Décadas distintas"},
    "🟡 Medio ×2":  {"mult": 2, "range": 30,  "desc": "Rango ~30 años"},
    "🔴 Difícil ×3":{"mult": 3, "range": 15,  "desc": "Rango ~15 años"},
}

def pick_timeline_events(diff_key: str):
    cfg     = TIMELINE_DIFFS[diff_key]
    events  = D.F1_EVENTS[:]
    max_range = cfg["range"]
    for _ in range(500):
        sample = random.sample(events, 5)
        years  = [e[0] for e in sample]
        if max(years) - min(years) <= max_range:
            return sample
    return random.sample(events, 5)

def init_timeline(diff_key: str):
    events  = pick_timeline_events(diff_key)
    ordered = sorted(events, key=lambda e: e[0])
    shuffled = events[:]
    random.shuffle(shuffled)
    return {
        "diff":     diff_key,
        "events":   shuffled,   # lista desordenada que el usuario reordena
        "correct":  ordered,
        "order":    list(range(5)),   # índices en el orden actual del usuario
        "checked":  False,
        "correct_count": 0,
        "score":    0,
        "round":    st.session_state.get("timeline_round", 1),
        "total_score": st.session_state.get("timeline_total", 0),
    }

def render_timeline():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>📅 LÍNEA DE TIEMPO</h2>",
                unsafe_allow_html=True)

    ss("timeline_round", 1); ss("timeline_total", 0); ss("timeline_diff", "🟢 Fácil ×1")

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        diff = st.selectbox("Dificultad", list(TIMELINE_DIFFS.keys()),
                            key="timeline_diff_sel",
                            index=list(TIMELINE_DIFFS.keys()).index(st.session_state.timeline_diff))
        st.session_state.timeline_diff = diff
    with c2:
        if st.button("▶ Nuevo Ronda", use_container_width=True, type="primary"):
            st.session_state.timeline_state = init_timeline(diff)
            st.rerun()
    with c3:
        st.metric("⭐ Total", st.session_state.timeline_total)

    ts = st.session_state.timeline_state
    if ts is None:
        st.info("Presioná **Nuevo Ronda** para empezar.")
        return

    st.markdown(
        f"<div style='color:#888;font-size:0.85rem;margin-bottom:12px'>"
        f"Ronda {ts['round']}/10 · {TIMELINE_DIFFS[ts['diff']]['desc']} · "
        f"Ordená de más antiguo (arriba) a más reciente (abajo)</div>",
        unsafe_allow_html=True,
    )

    events  = ts["events"]
    order   = ts["order"]

    if not ts["checked"]:
        for i in range(5):
            evt = events[order[i]]
            year_hint = str(evt[0]) if ts["checked"] else "????"
            cat_icons = {"debut":"🏎️","titulo":"👑","accidente":"🚨",
                         "reglamento":"📋","victoria":"🏆","record":"⭐"}
            icon = cat_icons.get(evt[2], "📌")
            cA, cB = st.columns([4, 1])
            with cA:
                st.markdown(
                    f"<div style='background:#1a1a1a;border:1px solid #333;"
                    f"border-radius:8px;padding:10px 14px;margin:3px 0'>"
                    f"{icon} {evt[1]}</div>",
                    unsafe_allow_html=True,
                )
            with cB:
                btn_col = st.columns(2)
                if i > 0:
                    if btn_col[0].button("▲", key=f"tl_up_{i}"):
                        order[i], order[i-1] = order[i-1], order[i]
                        ts["order"] = order
                        st.session_state.timeline_state = ts
                        st.rerun()
                if i < 4:
                    if btn_col[1].button("▼", key=f"tl_dn_{i}"):
                        order[i], order[i+1] = order[i+1], order[i]
                        ts["order"] = order
                        st.session_state.timeline_state = ts
                        st.rerun()

        if st.button("✔ Verificar orden", type="primary"):
            user_years   = [events[order[i]][0] for i in range(5)]
            correct_years = [ts["correct"][i][0] for i in range(5)]
            hits = sum(1 for a, b in zip(user_years, correct_years) if a == b)
            mult = TIMELINE_DIFFS[ts["diff"]]["mult"]
            pts  = hits * 20 * mult + (50 * mult if hits == 5 else 0)
            ts["checked"] = True
            ts["correct_count"] = hits
            ts["score"]   = pts
            st.session_state.timeline_total += pts
            add_points(pts)
            st.session_state.timeline_state = ts
            st.rerun()
    else:
        # Mostrar resultado
        correct_order = ts["correct"]
        user_order    = [events[order[i]] for i in range(5)]
        cat_icons = {"debut":"🏎️","titulo":"👑","accidente":"🚨",
                     "reglamento":"📋","victoria":"🏆","record":"⭐"}
        for i in range(5):
            evt      = user_order[i]
            expected = correct_order[i]
            ok       = evt[0] == expected[0]
            icon     = cat_icons.get(evt[2], "📌")
            color    = "#0a2a0a" if ok else "#2a0a0a"
            border   = "#2e7d32" if ok else "#c62828"
            mark     = "✅" if ok else "❌"
            st.markdown(
                f"<div style='background:{color};border:1px solid {border};"
                f"border-radius:8px;padding:10px 14px;margin:3px 0'>"
                f"{mark} {icon} <b>{evt[0]}</b> — {evt[1]}</div>",
                unsafe_allow_html=True,
            )
        hits = ts["correct_count"]
        mult = TIMELINE_DIFFS[ts["diff"]]["mult"]
        pts  = ts["score"]
        color_pts = "#ffd700" if hits == 5 else "#00c853" if hits >= 3 else "#888"
        st.markdown(
            f"<div style='font-family:Rajdhani;font-size:1.3rem;color:{color_pts};"
            f"margin:12px 0'>"
            f"{'🏆 ¡PERFECTO!' if hits==5 else f'{hits}/5 correctos'} · ⭐ {pts} pts</div>",
            unsafe_allow_html=True,
        )
        if ts["round"] < 10:
            if st.button("➡ Siguiente ronda", type="primary"):
                st.session_state.timeline_round = ts["round"] + 1
                st.session_state.timeline_state = init_timeline(ts["diff"])
                st.session_state.timeline_state["round"] = ts["round"] + 1
                st.rerun()
        else:
            st.success(f"🏁 ¡Partida terminada! Total: {st.session_state.timeline_total} pts")
            if st.button("🔄 Nueva Partida"):
                st.session_state.timeline_round = 1
                st.session_state.timeline_total = 0
                st.session_state.timeline_state = None
                st.rerun()

# ══════════════════════════════════════════════════════════════════
#  MODO 6 — ¿QUIÉN SOY? (MYSTERY DRIVER)
# ══════════════════════════════════════════════════════════════════
PISTAS_DEF = [
    ("época",        "epoca",       500),
    ("nacionalidad", "nac",         400),
    ("equipos",      "equipos",     300),
    ("estadísticas", "stats",       200),
    ("campeonatos",  "campeonatos", 100),
]

def get_pista_html(driver: str, meta: dict, pista_idx: int) -> str:
    key = PISTAS_DEF[pista_idx][1]
    debut = meta["debut"]
    decade = f"{(debut // 10) * 10}s" if debut else "desconocida"
    if key == "epoca":
        return f"🕰️ Debutó en los <b>{decade}</b>"
    elif key == "nac":
        nat = meta["nationality"]
        return f"{flag(nat)} Nacionalidad: <b>{nat.capitalize()}</b>"
    elif key == "equipos":
        teams = meta["teams"]
        first = teams[0].title() if teams else "?"
        last  = teams[-1].title() if teams else "?"
        return f"🏎️ Primer equipo: <b>{first}</b> · Último: <b>{last}</b>"
    elif key == "stats":
        return f"🏆 Victorias: <b>{meta['wins']}</b> · Podios: <b>{meta['podiums']}</b>"
    elif key == "campeonatos":
        champ = meta["champion"]
        n = champ if isinstance(champ, int) else (1 if champ else 0)
        return f"👑 Campeonatos: <b>{n}</b> · Temporadas: <b>{meta['seasons']}</b>"
    return ""

def init_mystery(daily=False):
    candidates = [(n, d) for n, d in D.RAW_F1.items()
                  if d[2] > 0 or d[3] > 0 or bool(d[4])]
    if daily:
        rng  = random.Random(daily_seed("mystery"))
        cands_sorted = sorted(candidates, key=lambda x: x[0])
        name, data = rng.choice(cands_sorted)
    else:
        name, data = random.choice(candidates)

    teams, nat, wins, pods, champ, debut, academy, birth, seasons, last = data
    meta = {
        "teams": teams, "nationality": nat, "wins": wins, "podiums": pods,
        "champion": champ, "debut": debut, "seasons": seasons, "last_season": last,
    }
    return {
        "name": name, "meta": meta,
        "pistas_vistas": 1,
        "answered": False, "correct": None,
        "score_session": st.session_state.get("mystery_score", 0),
        "vistos": st.session_state.get("mystery_vistos", set()),
        "daily": daily,
    }

def render_mystery():
    st.markdown("<h2 style='font-family:Rajdhani;color:#e10600'>🕵️ ¿QUIÉN SOY?</h2>",
                unsafe_allow_html=True)

    ss("mystery_score", 0); ss("mystery_vistos", set())

    all_f1 = sorted(n.title() for n in D.RAW_F1.keys())

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("🆕 Nuevo Piloto", use_container_width=True, type="primary"):
            vistos = st.session_state.mystery_vistos
            candidates = [n for n, d in D.RAW_F1.items()
                          if (d[2] > 0 or d[3] > 0 or bool(d[4])) and n not in vistos]
            if not candidates:
                st.session_state.mystery_vistos = set()
                candidates = [n for n, d in D.RAW_F1.items()
                              if d[2] > 0 or d[3] > 0 or bool(d[4])]
            st.session_state.mystery_state = init_mystery()
            st.rerun()
    with c2:
        if st.button("📅 Piloto del Día", use_container_width=True):
            key = f"mystery-daily-{datetime.date.today().isoformat()}"
            if already_played(key):
                st.warning("Ya adivinaste el piloto del día. ¡Volvé mañana!")
            else:
                st.session_state.mystery_state = init_mystery(daily=True)
                st.rerun()
    with c3:
        total = len([n for n, d in D.RAW_F1.items() if d[2]>0 or d[3]>0 or bool(d[4])])
        vistos = len(st.session_state.mystery_vistos)
        st.markdown(
            f"<div style='font-family:Rajdhani;font-size:1.1rem;color:#888;padding:8px 0'>"
            f"⭐ {st.session_state.mystery_score} pts · "
            f"Vistos: {vistos}/{total}</div>",
            unsafe_allow_html=True,
        )

    ms = st.session_state.mystery_state
    if ms is None:
        st.info("Presioná **Nuevo Piloto** para empezar.")
        return

    # Mostrar pistas
    for i in range(ms["pistas_vistas"]):
        if i < len(PISTAS_DEF):
            pts_if_correct = PISTAS_DEF[i][2]
            pista_html = get_pista_html(ms["name"], ms["meta"], i)
            border = "#ffd700" if i == 0 else "#333"
            st.markdown(
                f"<div style='background:#1a1a1a;border-left:4px solid {border};"
                f"border-radius:0 8px 8px 0;padding:10px 16px;margin:4px 0;"
                f"font-size:0.95rem'>"
                f"<span style='color:#555;font-size:0.75rem'>Pista {i+1} "
                f"({pts_if_correct} pts si acertás ahora)</span><br>"
                f"{pista_html}</div>",
                unsafe_allow_html=True,
            )

    if not ms["answered"]:
        # Botón ver pista adicional
        if ms["pistas_vistas"] < len(PISTAS_DEF):
            if st.button("💡 Ver pista adicional"):
                ms["pistas_vistas"] += 1
                st.session_state.mystery_state = ms
                st.rerun()

        # Input respuesta
        col_inp, col_btn = st.columns([3, 1])
        with col_inp:
            guess = st.selectbox(
                "¿Quién es?",
                [""] + all_f1,
                key="mystery_guess",
                label_visibility="collapsed",
                placeholder="Escribí o elegí el piloto...",
            )
        with col_btn:
            if st.button("✔ Responder", type="primary", use_container_width=True):
                if guess:
                    correcto = ms["name"]
                    val      = normalize(guess)
                    partes   = normalize(correcto).split()
                    acierto  = (
                        val == normalize(correcto) or
                        val == partes[-1] or
                        (len(partes[0]) >= 4 and val == partes[0]) or
                        (len(val) >= 4 and val in normalize(correcto))
                    )
                    pts_idx  = ms["pistas_vistas"] - 1
                    pts      = PISTAS_DEF[pts_idx][2] if acierto else 0
                    ms["answered"] = True
                    ms["correct"]  = acierto
                    if acierto:
                        ms["score_session"] = ms.get("score_session", 0) + pts
                        st.session_state.mystery_score += pts
                        st.session_state.mystery_vistos.add(correcto)
                        add_points(pts)
                    ms["pts_earned"] = pts
                    if ms["daily"]:
                        mark_played(f"mystery-daily-{datetime.date.today().isoformat()}")
                    # Revelar todas las pistas
                    ms["pistas_vistas"] = len(PISTAS_DEF)
                    st.session_state.mystery_state = ms
                    st.rerun()
    else:
        # Resultado
        if ms["correct"]:
            pts = ms.get("pts_earned", 0)
            st.success(f"✅ ¡CORRECTO! **{fmt(ms['name'])}** — +{pts} pts")
        else:
            st.error(f"❌ Era **{fmt(ms['name'])}**")

        if not ms["daily"]:
            if st.button("➡ Siguiente piloto", type="primary"):
                st.session_state.mystery_state = None
                # Auto-iniciar con nuevo piloto
                vistos = st.session_state.mystery_vistos
                candidates = [n for n, d in D.RAW_F1.items()
                              if (d[2]>0 or d[3]>0 or bool(d[4])) and n not in vistos]
                if not candidates:
                    st.session_state.mystery_vistos = set()
                st.session_state.mystery_state = init_mystery()
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
