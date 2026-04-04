# Arquitectura del Repositorio y Funcionamiento

**ProyectoFinal23** — Análisis del Mercado Musical con ML
**Stack:** Python 3.11 · Streamlit · scikit-learn · pandas · Last.fm API

---

## Estructura de carpetas

```
ProyectoFinal23/
│
├── src/                          # Código fuente de la aplicación
│   ├── app.py                    # Punto de entrada Streamlit
│   ├── utils.py                  # Utilidades (conexión DB — sin uso activo)
│   ├── data/
│   │   ├── __init__.py
│   │   ├── load_data.py          # Carga y unión de CSVs
│   │   └── process_data.py       # Limpieza y feature engineering
│   ├── models/
│   │   ├── __init__.py
│   │   └── predict.py            # Carga modelo y expone predict_hit()
│   └── visualization/
│       ├── __init__.py
│       └── charts.py             # Todas las funciones de gráficos
│
├── data/
│   ├── raw/                      # Datos originales de la API (no modificar)
│   │   ├── backup_tracks.csv     # ~34k tracks con metadata completa
│   │   ├── lastfm_dataset.csv    # 60k filas con rankings por país/género
│   │   └── tags_dataset.csv      # Géneros/tags de Last.fm
│   ├── interim/                  # Datos intermedios (en uso: vacío)
│   └── processed/
│       └── df_merged-data.csv    # Dataset unificado (~34k tracks únicos, 41 MB)
│
├── models/                       # Artefactos ML entrenados
│   ├── modelo_hits_clf.pkl       # RandomForestClassifier (generado por train_model.py)
│   ├── le_tag.pkl                # LabelEncoder de géneros
│   └── features.txt              # Lista de features del modelo
│
├── notebooks/                    # Exploración y desarrollo
│   ├── PF_v1_paraStreamlit.ipynb         # Notebook principal de desarrollo
│   ├── PF_v1_paraStreamlit-2.ipynb       # Segunda versión del notebook
│   ├── Apuntes.ipynb                     # Notas y experimentos
│   ├── Problemas-Resoluciones-Durante.ipynb
│   └── Recolectar_Data.ipynb             # Pipeline de recolección Last.fm
│
├── docs/                         # Documentación del proyecto
│   ├── arquitectura.md           # Este documento
│   ├── CHANGELOG.md              # Historial de cambios por versión
│   ├── errores.md                # Cuaderno de errores y soluciones
│   └── specs_streamlit.md        # Especificaciones técnicas de la app
│
├── train_model.py                # Script de entrenamiento ML
├── requirements.txt              # Dependencias Python
├── pipeline.log                  # Log del pipeline de recolección
├── README.md                     # Documentación principal
└── .devcontainer/                # Configuración de GitHub Codespaces
    ├── devcontainer.json
    ├── docker-compose.yml
    └── Dockerfile
```

---

## Flujo de datos

```
Last.fm API
    │
    ├── chart.getTopTracks  ──┐
    ├── geo.getTopTracks    ──┼──► lastfm_dataset.csv (60k filas)
    └── tag.getTopTracks    ──┘
                               │
    track.getInfo ────────────► backup_tracks.csv (~34k tracks)
                               │
                               ▼
                    load_data.py::build_df_merged()
                    [merge por mbid + deduplicación por país]
                               │
                               ▼
                    df_merged-data.csv (~34k tracks únicos)
                               │
                               ▼
                    process_data.py::clean_and_feature_engineer()
                    [limpieza + 10 nuevas features]
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             df_clean                le_tag, FEATURES
          (Streamlit app)          (train_model.py → .pkl)
                    │
                    ▼
            src/app.py (Streamlit)
            └── 6 páginas de visualización
```

---

## Módulos Python

### `src/data/load_data.py`

| Función | Descripción |
|---------|-------------|
| `load_backup_tracks()` | Carga `backup_tracks.csv` — metadata de tracks |
| `load_lastfm_dataset()` | Carga `lastfm_dataset.csv` — rankings y países |
| `load_tags_dataset()` | Carga `tags_dataset.csv` |
| `build_df_merged()` | Une backup_tracks + país de lastfm por `mbid`. Deduplica por prioridad: país real > GLOBAL > UNKNOWN |
| `load_df_merged()` | Carga `df_merged-data.csv` si existe; si no, llama a `build_df_merged()` |

**Rutas:** usa `os.path.dirname(__file__)` con `'..', '..'` → resuelve a la raíz del repo.

---

### `src/data/process_data.py`

| Función | Descripción |
|---------|-------------|
| `get_first_tag(x)` | Extrae el nombre del primer tag de la lista de dicts de Last.fm |
| `clean_and_feature_engineer(df_merged)` | Pipeline completo de limpieza. Devuelve `(df_clean, le_tag, FEATURES)` |
| `prepare_ml_dataset(df_clean, FEATURES)` | Devuelve `X, y_clf, y_reg` listos para `train_test_split` |

**Features generadas:**

| Feature | Tipo | Descripción |
|---------|------|-------------|
| `duration_min` | float | Duración en minutos (ms / 60000) |
| `is_short_track` | int | 1 si duración < 2.5 min |
| `is_hit` | int | 1 si playcount >= percentil 90 |
| `playcount_per_listener` | float | Engagement por oyente |
| `log_playcount` | float | log(1 + playcount) |
| `log_listeners` | float | log(1 + listeners) |
| `popularity_ratio` | float | Fracción del playcount total del dataset |
| `artist_track_count` | int | Nº de tracks del artista en el dataset |
| `track_share_of_artist` | float | % del playcount del artista que representa este track |
| `tag_encoded` | int | Género codificado con LabelEncoder |

---

### `src/models/predict.py`

| Función | Descripción |
|---------|-------------|
| `load_model()` | Carga `modelo_hits_clf.pkl`, `le_tag.pkl`, `features.txt` desde `models/` |
| `predict_hit(duracion_min, genero, oyentes_estimados, ...)` | Devuelve `{probability, label, emoji}` |

**Umbrales de clasificación:**
- ≥ 70% → "Hit potencial" 🚀
- ≥ 45% → "Potencial medio" 🟡
- < 45% → "Bajo potencial" 📉

---

### `src/visualization/charts.py`

| Función | Página | Descripción |
|---------|--------|-------------|
| `plot_playcount_distribution(df)` | Dashboard | Histogramas playcount lineal vs log |
| `plot_top_artists(df, n)` | Dashboard | Top N artistas por reproducciones y tracks |
| `plot_top_genres(df, n)` | Dashboard | Top N géneros |
| `plot_duration_vs_popularity(df)` | Dashboard | Duración por rangos + boxplot |
| `plot_geo_analysis(df)` | Geografía | Popularidad y tracks por país |
| `plot_correlation_heatmap(df)` | Correlaciones | Heatmap Spearman |
| `plot_tracks_per_year(df)` | Tendencias | Bar chart de tracks por año de publicación |
| `plot_avg_playcount_by_year(df)` | Tendencias | Line chart de playcount medio por año |
| `plot_top_tracks(df, n)` | Rankings | Horizontal bar top N por playcount |
| `plot_top_engagement(df, n)` | Rankings | Horizontal bar top N por engagement |

Todas las funciones devuelven una figura `matplotlib.figure.Figure` para usar con `st.pyplot(fig)`.

---

### `src/app.py`

Punto de entrada de la aplicación Streamlit. Estructura:

```python
# 1. Imports y sys.path
sys.path.insert(0, os.path.dirname(__file__))  # añade src/ al path

# 2. Carga de datos (cacheada)
@st.cache_data
def get_data():
    df_merged = load_df_merged()
    df_clean, le_tag, FEATURES = clean_and_feature_engineer(df_merged)
    return df_clean, le_tag, FEATURES

@st.cache_resource
def get_model():
    ...  # carga .pkl, maneja FileNotFoundError

# 3. Sidebar con radio de navegación
pagina = st.sidebar.radio('Sección', [...6 páginas...])

# 4. Bloques if/elif por página
if pagina == '🔮 Predictor de hit':   ...
elif pagina == '📊 Dashboard':        ...
elif pagina == '🌍 Geografía':        ...
elif pagina == '📈 Correlaciones':    ...
elif pagina == '📅 Tendencias':       ...
elif pagina == '🏆 Rankings':         ...
```

---

## Páginas de la app Streamlit

| # | Página | Datos usados | Gráficos |
|---|--------|-------------|----------|
| 1 | 🔮 Predictor de hit | Modelo ML + le_tag | — (formulario + métricas) |
| 2 | 📊 Dashboard | df_clean | Distribuciones, top artistas, géneros, duración |
| 3 | 🌍 Geografía | df_clean (country ≠ GLOBAL/UNKNOWN) | Popularidad y tracks por país |
| 4 | 📈 Correlaciones | df_clean (columnas numéricas) | Heatmap Spearman + tabla ranking |
| 5 | 📅 Tendencias | df_clean (published date) | Tracks/año, playcount medio/año |
| 6 | 🏆 Rankings | df_clean (playcount, playcount_per_listener) | Horizontal bars + tablas filtrables |

---

## Cómo ejecutar el proyecto

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Entrenar el modelo ML
```bash
python train_model.py
```
Genera `models/modelo_hits_clf.pkl`, `models/le_tag.pkl`, `models/features.txt`.
Sin este paso, la página 🔮 Predictor mostrará un aviso pero el resto de la app funciona.

### 3. Lanzar la app
```bash
streamlit run src/app.py
```

### En GitHub Codespaces
El paso 1 se ejecuta automáticamente al crear el Codespace (configurado en `.devcontainer/devcontainer.json`).

---

## Decisiones de arquitectura

| Decisión | Alternativa descartada | Razón |
|----------|----------------------|-------|
| `sys.path.insert` en app.py | Instalar src como paquete | Más simple para Codespaces sin setup.py |
| Rutas relativas con `__file__` | Rutas absolutas o variables de entorno | Portabilidad entre Codespaces y local |
| `@st.cache_data` para df_clean | Sin caché | El procesado tarda ~5s — con caché solo ocurre al arrancar |
| `@st.cache_resource` para modelo | `@st.cache_data` | Los modelos sklearn no son serializables con st.cache_data |
| Matplotlib + seaborn | Plotly / Altair | Ya era el stack del notebook; no rompe nada |
| CSV como formato de datos | Parquet / SQLite | Los datos ya estaban en CSV; sin ventaja real en escalar a Parquet |
| joblib para serialización | pickle | joblib es más eficiente con arrays numpy grandes (Random Forest) |

---

## Limitaciones conocidas

| Limitación | Impacto | Posible solución |
|-----------|---------|-----------------|
| Data leakage en modelo ML | Accuracy=1.00 inflada, no generaliza a canciones nuevas | Temporal split o redefinir target |
| `df_merged-data.csv` (41 MB) en git | Lento en clonar, límite de GitHub | Git LFS o cargar desde cloud storage |
| AcousticBrainz discontinuada | Solo ~1.75% de tracks con features de audio | Spotify Audio Features API |
| `published` date: baja cobertura | Página Tendencias con pocos datos | Enriquecer con MusicBrainz API |
| Modelo no versionado | `.pkl` en `.gitignore` recomendado | MLflow o DVC para tracking de modelos |
