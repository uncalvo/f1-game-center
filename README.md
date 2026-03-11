# 🏎️ F1 Game Center — Streamlit

Juego de F1 con 6 modos: Grid Challenge, Podium Challenge, Duelo de Pilotos,
Constructor Challenge, Línea de Tiempo y ¿Quién Soy?

---

## Cómo ejecutarlo localmente

### 1. Instalá Python
Si no tenés Python instalado, bajalo de https://python.org (versión 3.9 o más nueva).

### 2. Instalá Streamlit
Abrí una terminal (cmd en Windows, Terminal en Mac/Linux) y escribí:
```
pip install streamlit
```

### 3. Ejecutá el juego
En la terminal, navegá a esta carpeta y ejecutá:
```
streamlit run app.py
```

Se va a abrir automáticamente en tu navegador en http://localhost:8501

---

## Cómo subirlo gratis a internet (Streamlit Cloud)

1. Creá una cuenta gratis en https://github.com y otra en https://streamlit.io
2. Subí estos 3 archivos a un repositorio de GitHub:
   - `app.py`
   - `f1_data.py`
   - `requirements.txt`
3. En https://share.streamlit.io → "New app" → elegí tu repositorio
4. En "Main file path" escribí `app.py`
5. Hacé click en "Deploy" — en 2-3 minutos tenés la URL pública

---

## Archivos
- `app.py` — Interfaz web (Streamlit)
- `f1_data.py` — Base de datos y lógica del juego
- `requirements.txt` — Dependencias
