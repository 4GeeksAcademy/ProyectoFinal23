# 🎵 ProyectoFinal23 — Análisis del Mercado Musical

App de análisis del mercado musical con Machine Learning sobre datos de **Last.fm API**.
Predicción de popularidad de canciones + visualizaciones interactivas con Streamlit.

---

## Qué hace la app

| Página | Descripción |
|--------|-------------|
| 🔮 Predictor de hit | Introduce características de una canción y obtén su probabilidad de ser un hit |
| 📊 Dashboard | KPIs del mercado, distribuciones de popularidad, top artistas y géneros |
| 🌍 Geografía | Popularidad y volumen de tracks por país |
| 📈 Correlaciones | Heatmap de correlaciones Spearman entre variables |
| 📅 Tendencias | Evolución temporal de publicaciones y popularidad por año |
| 🏆 Rankings | Top N tracks por reproducciones totales y por engagement |

---

## Inicio rápido

### En GitHub Codespaces (recomendado)

Las dependencias se instalan automáticamente al crear el Codespace.

```bash
# 1. Entrenar el modelo ML (una sola vez)
python train_model.py

# 2. Lanzar la app
streamlit run src/app.py
```

### En local

```bash
# 1. Clonar el repositorio
git clone https://github.com/JaimeAFL/ProyectoFinal23.git
cd ProyectoFinal23

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Entrenar el modelo
python train_model.py

# 4. Lanzar la app
streamlit run src/app.py
```

---

## Datos

| Archivo | Filas | Descripción |
|---------|-------|-------------|
| `data/raw/backup_tracks.csv` | ~34k | Metadata de tracks: nombre, artista, duración, tags, oyentes, playcount |
| `data/raw/lastfm_dataset.csv` | 60k | Rankings globales y por país/género (multi-endpoint) |
| `data/raw/tags_dataset.csv` | — | Géneros/tags de Last.fm |
| `data/processed/df_merged-data.csv` | ~34k | Dataset unificado y deduplicado (entrada principal de la app) |

**Fuentes:** Last.fm API (`chart.getTopTracks`, `geo.getTopTracks`, `tag.getTopTracks`, `track.getInfo`)

---

## Estructura del proyecto

```
ProyectoFinal23/
├── src/
│   ├── app.py                    # App Streamlit (6 páginas)
│   ├── data/
│   │   ├── load_data.py          # Carga y unión de CSVs
│   │   └── process_data.py       # Limpieza y feature engineering
│   ├── models/
│   │   └── predict.py            # Inferencia con el modelo entrenado
│   └── visualization/
│       └── charts.py             # Funciones de gráficos (matplotlib/seaborn)
├── data/
│   ├── raw/                      # Datos originales
│   └── processed/                # Dataset listo para la app
├── models/                       # Artefactos ML (.pkl, .txt)
├── notebooks/                    # Exploración y desarrollo
├── docs/                         # Documentación
│   ├── arquitectura.md           # Arquitectura y funcionamiento
│   ├── CHANGELOG.md              # Historial de versiones
│   ├── errores.md                # Cuaderno de errores y soluciones
│   └── specs_streamlit.md        # Especificaciones técnicas
├── train_model.py                # Script de entrenamiento ML
└── requirements.txt              # Dependencias
```

---

## Modelo ML

- **Algoritmo:** RandomForestClassifier (n_estimators=100, random_state=42)
- **Target:** `is_hit` — top 10% de tracks por playcount
- **Features:** `log_listeners`, `duration_min`, `is_short_track`, `tag_encoded`, `artist_track_count`, `track_share_of_artist`, `playcount_per_listener`
- **Nota:** el modelo predice popularidad histórica relativa al dataset. Ver `docs/errores.md` #17 para limitaciones.

---

## Documentación

- [Arquitectura y funcionamiento](docs/arquitectura.md)
- [Historial de cambios](docs/CHANGELOG.md)
- [Cuaderno de errores y soluciones](docs/errores.md)
- [Especificaciones técnicas Streamlit](docs/specs_streamlit.md)

---

## Stack tecnológico

`Python 3.11` · `Streamlit` · `pandas` · `scikit-learn` · `matplotlib` · `seaborn` · `joblib` · `Last.fm API`

---

*Proyecto desarrollado como parte del Data Science and Machine Learning Bootcamp — [4Geeks Academy](https://4geeksacademy.com)*
