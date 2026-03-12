# 🏎️ F1 Game Center

12 juegos de Fórmula 1 construidos con Streamlit.

## Juegos incluidos

| Juego | Descripción |
|---|---|
| 🔲 Grid Challenge | Encontrá el piloto que cumple fila y columna |
| 🏆 Podium Challenge | Adiviná el Top 10 de un GP histórico |
| ⚔️ Duelo de Pilotos | ¿Quién tiene más victorias/podios/títulos? |
| 🏗️ Constructor | Encontrá la escudería que cumple ambas condiciones |
| 📅 Línea de Tiempo | Ordená eventos de F1 cronológicamente |
| 🕵️ Piloto Misterioso | Adiviná el piloto con pistas progresivas |
| 🔗 Cadena de Pilotos | Conectá dos pilotos por compañeros de equipo |
| 📊 Stats Extremas | Verdadero o Falso sobre récords de F1 |
| ⏱️ Adivina la Vuelta | Adiviná el tiempo de clasificación |
| 🧩 F1 Wordle | Adiviná el apellido del piloto en 6 intentos |
| 🔢 ¿Cuántos Puntos? | Adiviná los puntos del piloto en esa temporada |
| 🗺️ ¿En qué Circuito? | Pistas progresivas para identificar el circuito |

## Instalación local

```bash
git clone https://github.com/TU_USUARIO/f1-game-center.git
cd f1-game-center
pip install -r requirements.txt
streamlit run app.py
```

## Deploy en Streamlit Cloud

1. Subí este repositorio a GitHub
2. Entrá a [share.streamlit.io](https://share.streamlit.io)
3. Conectá tu repositorio
4. Archivo principal: `app.py`
5. ¡Listo!

## Estructura

```
f1-game-center/
├── app.py              # Entrada principal
├── f1_data.py          # Base de datos F1 (pilotos, GPs, circuitos)
├── requirements.txt
├── .streamlit/
│   └── config.toml     # Tema oscuro F1
└── games/
    ├── grid.py
    ├── podium.py
    ├── duelo.py
    ├── constructor.py
    ├── timeline.py
    ├── piloto_misterioso.py
    ├── cadena.py
    ├── stats_extremas.py
    ├── adivina_vuelta.py
    ├── wordle.py
    ├── cuantos_puntos.py
    └── circuito.py
```
