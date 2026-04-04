# Changelog — ProyectoFinal23
# Análisis del Mercado Musical y Detección de Fraude en Streams

Todos los cambios relevantes del proyecto quedan registrados aquí.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

---

## [0.4.0] — 2026-04-04

### Añadido
- `requirements.txt` con todas las dependencias del proyecto (streamlit, pandas, numpy, matplotlib, seaborn, scikit-learn, joblib, python-dotenv, requests, beautifulsoup4)
- `train_model.py` — script de entrenamiento del modelo ML ejecutable desde la raíz
  - Carga datos con el pipeline existente (`load_data` + `process_data`)
  - Entrena `RandomForestClassifier(n_estimators=100, random_state=42)`
  - Guarda `models/modelo_hits_clf.pkl`, `models/le_tag.pkl`, `models/features.txt`

### Uso
```bash
pip install -r requirements.txt
python train_model.py
streamlit run src/app.py
```

---

## [0.3.1] — 2026-04-03

### Corregido
- `src/visualization/charts.py` — `plot_top_engagement`: reemplaza `pd.NA` por `np.nan` al limpiar infinitos en `playcount_per_listener` para preservar dtype float y evitar `TypeError` en `nlargest`
- `src/app.py` — mismo fix en la tabla de Rankings (tab2)

---

## [0.3.0] — 2026-04-03

### Añadido
- `docs/specs_streamlit.md` — especificaciones técnicas completas de la app
- **Página 5: 📅 Tendencias** en `src/app.py`
  - Métricas de cobertura temporal
  - Bar chart de tracks por año de publicación
  - Line chart de playcount medio por año
- **Página 6: 🏆 Rankings** en `src/app.py`
  - Tabs: por popularidad (playcount) y por engagement (playcount/oyente)
  - Gráficos horizontales + tablas con los top N tracks
  - Slider configurable (10–100 tracks)
- Nuevas funciones en `src/visualization/charts.py`:
  - `plot_tracks_per_year`
  - `plot_avg_playcount_by_year`
  - `plot_top_tracks`
  - `plot_top_engagement`

---

## [0.2.0] — 2026-04-03

### Cambiado (reorganización estructural)
- Archivos Python movidos de la raíz a su ubicación correcta:
  - `load_data.py` → `src/data/load_data.py`
  - `process_data.py` → `src/data/process_data.py`
  - `predict.py` → `src/models/predict.py`
  - `charts.py` → `src/visualization/charts.py`
- `app (1).py` (app real) reemplaza al stub `src/app.py`
- Notebooks movidos de `src/` y `src/Información y notas/` a `notebooks/`
- Añadidos `__init__.py` en `src/data/`, `src/models/`, `src/visualization/`

### Resultado
- `streamlit run src/app.py` funciona sin ningún cambio de código
- Las rutas relativas en `load_data.py` y `predict.py` funcionan correctamente desde sus nuevas ubicaciones

---

## [0.1.0] — 2026-03-20 / 2026-03-28

### Añadido (trabajo en notebooks)
- Pipeline de recolección multi-endpoint Last.fm API:
  - `chart.getTopTracks` (~30k tracks globales)
  - `geo.getTopTracks` (10 países, ~20k tracks)
  - `tag.getTopTracks` (10 géneros, ~15k tracks)
  - Total tras deduplicación: ~34k tracks únicos, ~60k filas
- `data/raw/backup_tracks.csv` — metadata de tracks (Last.fm track.getInfo)
- `data/raw/lastfm_dataset.csv` — dataset multi-endpoint con rankings por país
- `data/raw/tags_dataset.csv` — géneros/tags
- `data/processed/df_merged-data.csv` — dataset unificado y deduplicado
- Análisis exploratorio completo (EDA) en notebooks:
  - Distribuciones de popularidad, top artistas, géneros, duración
  - Análisis geográfico y correlaciones Spearman
- Feature engineering:
  - `duration_min`, `is_short_track`, `is_hit` (top 10% playcount)
  - `playcount_per_listener`, `log_playcount`, `log_listeners`
  - `artist_track_count`, `track_share_of_artist`, `popularity_ratio`
  - `tag_encoded` (LabelEncoder sobre géneros)
- App Streamlit con 4 páginas iniciales:
  - 🔮 Predictor de hit
  - 📊 Dashboard
  - 🌍 Geografía
  - 📈 Correlaciones
