# Especificaciones Técnicas — App Streamlit: Análisis del Mercado Musical

## Contexto

App Streamlit de análisis del mercado musical basada en datos de Last.fm.
Entrada: `data/processed/df_merged-data.csv` (≈34k tracks tras deduplicación).
Se ejecuta con: `streamlit run src/app.py`

---

## Fuentes de datos y columnas disponibles

### df_merged (entrada a la app)
| Columna | Tipo | Descripción |
|---------|------|-------------|
| name | str | Nombre del track |
| artist | str | Artista |
| duration | float | Duración en ms |
| mbid | str | MusicBrainz ID |
| tag | str/list | Tags de género (Last.fm) |
| listeners | float | Oyentes únicos |
| playcount | float | Reproducciones totales |
| published | str | Fecha de publicación (`DD Mon YYYY, HH:MM`) |
| country | str | País (o GLOBAL / UNKNOWN) |

### Columnas generadas por `process_data.py`
| Columna | Tipo | Descripción |
|---------|------|-------------|
| duration_min | float | Duración en minutos |
| is_short_track | int | 1 si duración < 2.5 min |
| is_hit | int | 1 si playcount >= percentil 90 |
| playcount_per_listener | float | Engagement por oyente |
| log_playcount | float | log(1 + playcount) |
| log_listeners | float | log(1 + listeners) |
| popularity_ratio | float | Fracción del playcount total |
| artist_track_count | int | Nº de tracks del artista en el dataset |
| track_share_of_artist | float | % del playcount del artista |
| tag (limpio) | str | Primer género extraído del tag list |
| published | date | Fecha de publicación (parseada) |

---

## Estructura de páginas

### Páginas existentes (NO modificar)
1. **🔮 Predictor de hit** — Formulario ML con Random Forest
2. **📊 Dashboard** — KPIs + distribuciones + top artistas/géneros + duración
3. **🌍 Geografía** — Análisis por país
4. **📈 Correlaciones** — Heatmap Spearman

### Páginas nuevas a implementar

#### Página 5: 📅 Tendencias
**Objetivo:** mostrar la evolución temporal del dataset.

**Fuente:** columna `published` (date) de `df_clean`. Solo filas con fecha válida (dropna).

**Componentes:**
- Métricas: nº de tracks con fecha conocida, rango de años, año más representado
- Gráfico 1: `plot_tracks_per_year(df_clean)` — bar chart de tracks publicados por año
- Gráfico 2: `plot_avg_playcount_by_year(df_clean)` — line chart de playcount medio por año
- Nota informativa si hay pocos tracks con fecha (< 10% del dataset)

**Lógica:**
```python
df_time = df_clean.dropna(subset=['published'])
df_time['year'] = pd.to_datetime(df_time['published']).dt.year
# Filtrar años razonables (1950-2030) para excluir ruido
df_time = df_time[(df_time['year'] >= 1950) & (df_time['year'] <= 2030)]
```

---

#### Página 6: 🏆 Rankings
**Objetivo:** explorar los tracks más populares y con mayor engagement.

**Fuente:** `df_clean`, columnas: name, artist, tag, playcount, listeners, playcount_per_listener, duration_min, is_hit.

**Componentes:**
- Slider: "Nº de tracks a mostrar" (10–100, default 25)
- Tab 1 — **Por popularidad (playcount)**:
  - Gráfico: `plot_top_tracks(df_clean, n)` — horizontal bar chart top N por playcount
  - Tabla: top N con columnas [rank, name, artist, tag, playcount, listeners, is_hit]
- Tab 2 — **Por engagement (playcount/listener)**:
  - Gráfico: `plot_top_engagement(df_clean, n)` — horizontal bar chart top N por playcount_per_listener
  - Tabla: top N por engagement con mismas columnas + playcount_per_listener
- Filtros (sidebar o expander): filtrar por género, filtrar solo hits

---

## Nuevas funciones en `src/visualization/charts.py`

### `plot_tracks_per_year(df_clean)`
- Input: df_clean con columna `published` (date)
- Procesa: extrae year, cuenta tracks por año, filtra 1950–2030
- Output: figura matplotlib (1 subplot) — bar chart año vs nº tracks
- Color: steelblue, título "Tracks por año de publicación"

### `plot_avg_playcount_by_year(df_clean)`
- Input: df_clean
- Procesa: agrupa por year, calcula media de playcount
- Output: figura matplotlib (1 subplot) — line chart + markers
- Color: coral, y-axis en millones (formatter)

### `plot_top_tracks(df_clean, n=25)`
- Input: df_clean, n (int)
- Procesa: top N por playcount, ordena ascendente para barh
- Output: figura matplotlib — horizontal bar chart
- Labels: "artista - nombre", x en millones, color steelblue

### `plot_top_engagement(df_clean, n=25)`
- Input: df_clean, n (int)
- Procesa: top N por playcount_per_listener (excluye inf/nan), ordena ascendente
- Output: figura matplotlib — horizontal bar chart
- Labels: "artista - nombre", color coral

---

## Modificaciones a `src/app.py`

1. Añadir `plot_tracks_per_year`, `plot_avg_playcount_by_year`, `plot_top_tracks`, `plot_top_engagement` al import de `visualization.charts`
2. Añadir `'📅 Tendencias'` y `'🏆 Rankings'` a la lista del `st.sidebar.radio`
3. Añadir bloques `elif pagina == '📅 Tendencias':` y `elif pagina == '🏆 Rankings':` al final

---

## Requisitos de calidad

- Todos los gráficos devuelven `fig` (matplotlib) para usar con `st.pyplot(fig)`
- Manejar el caso de datos vacíos (return None o mensaje `st.info`)
- Sin cambios en páginas existentes ni en lógica de carga/procesado
- Compatible con el modelo de carga actual: `@st.cache_data` sobre `get_data()`
