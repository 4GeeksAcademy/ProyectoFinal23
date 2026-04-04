"""
src/app.py
App Streamlit — Análisis del Mercado Musical
Ejecutar: streamlit run src/app.py
"""

import os
import sys
import streamlit as st
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))

from data.load_data     import load_df_merged
from data.process_data  import clean_and_feature_engineer
from models.predict     import load_model, predict_hit
from visualization.charts import (
    plot_playcount_distribution,
    plot_top_artists,
    plot_top_genres,
    plot_duration_vs_popularity,
    plot_geo_analysis,
    plot_correlation_heatmap,
    plot_tracks_per_year,
    plot_avg_playcount_by_year,
    plot_top_tracks,
    plot_top_engagement,
)

# ── Configuración ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title='🎵 Análisis Musical',
    page_icon='🎵',
    layout='wide',
)

# ── Carga de datos (cacheada) ─────────────────────────────────────────────────
@st.cache_data
def get_data():
    df_merged = load_df_merged()
    df_clean, le_tag, FEATURES = clean_and_feature_engineer(df_merged)
    return df_clean, le_tag, FEATURES

@st.cache_resource
def get_model():
    try:
        rf_clf, le_tag, FEATURES = load_model()
        return rf_clf, le_tag, FEATURES, None
    except FileNotFoundError as e:
        return None, None, None, str(e)

df_clean, le_tag_data, FEATURES_data = get_data()
rf_clf, le_tag_model, FEATURES_model, model_error = get_model()

# Usar encoder del modelo si está disponible; si no, el generado en proceso
le_tag   = le_tag_model   if le_tag_model   is not None else le_tag_data
FEATURES = FEATURES_model if FEATURES_model is not None else FEATURES_data

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title('🎵 Mercado Musical')
pagina = st.sidebar.radio(
    'Sección',
    ['🔮 Predictor de hit', '📊 Dashboard', '🌍 Geografía', '📈 Correlaciones', '📅 Tendencias', '🏆 Rankings']
)

# ════════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 — Predictor
# ════════════════════════════════════════════════════════════════════════════════
if pagina == '🔮 Predictor de hit':
    st.title('🔮 Predictor de Hit')
    st.markdown('Introduce las características de tu canción y el modelo estimará su potencial.')

    if model_error:
        st.error(f'⚠️ Modelo no disponible: {model_error}')
        st.info(
            'Ejecuta las celdas 173-183 del notebook y luego el bloque de guardado '
            '(corrección en `correcciones_notebook.ipynb`) para activar el predictor.'
        )
        st.stop()

    # Géneros disponibles según el encoder entrenado
    generos = sorted(le_tag.classes_.tolist())

    col1, col2 = st.columns(2)
    with col1:
        nombre  = st.text_input('Nombre de la canción', value='Mi Canción')
        artista = st.text_input('Nombre del artista',   value='Mi Artista')
        genero  = st.selectbox('Género musical (tag de Last.fm)', generos)
    with col2:
        duracion = st.slider('Duración (minutos)', 0.5, 10.0, 3.2, 0.1)
        oyentes  = st.number_input('Oyentes estimados', 100, 10_000_000, 50_000, 1000)

    st.markdown('---')

    if st.button('🎵 Predecir potencial de hit', use_container_width=True):
        resultado = predict_hit(
            duracion_min=duracion,
            genero=genero,
            oyentes_estimados=oyentes,
            rf_clf=rf_clf,
            le_tag=le_tag,
            FEATURES=FEATURES,
        )
        prob  = resultado['probability']
        label = resultado['label']
        emoji = resultado['emoji']

        st.markdown(f'### {emoji} {nombre} — {artista}')
        c1, c2, c3 = st.columns(3)
        c1.metric('Probabilidad de hit', f'{prob:.1f}%')
        c2.metric('Clasificación', label)
        c3.metric('Duración', f'{duracion:.1f} min')
        st.progress(prob / 100)

        if prob >= 70:
            st.success('🚀 Alta probabilidad. ¡Buenas señales!')
        elif prob >= 45:
            st.warning('🟡 Potencial medio. Considera ajustar duración u oyentes iniciales.')
        else:
            st.error('📉 Potencial bajo según el modelo.')

        if duracion < 2.5:
            st.info('⏱️ Canción corta (<2.5 min): compatible con formato TikTok/Reels.')

# ════════════════════════════════════════════════════════════════════════════════
# PÁGINA 2 — Dashboard
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == '📊 Dashboard':
    st.title('📊 Dashboard del Mercado Musical')

    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Total tracks',     f'{len(df_clean):,}')
    c2.metric('Artistas únicos',  f'{df_clean["artist"].nunique():,}')
    c3.metric('Géneros únicos',   f'{df_clean["tag"].nunique():,}')
    c4.metric('Playcount mediano', f'{df_clean["playcount"].median()/1e6:.1f}M')

    st.markdown('---')
    st.subheader('Distribución de popularidad')
    st.pyplot(plot_playcount_distribution(df_clean))

    st.markdown('---')
    n = st.slider('Nº de artistas', 5, 25, 15)
    st.subheader(f'Top {n} artistas')
    st.pyplot(plot_top_artists(df_clean, n=n))
    top5 = (
        df_clean.groupby('artist')['playcount'].sum()
        .sort_values(ascending=False).head(5).sum()
        / df_clean['playcount'].sum() * 100
    )
    st.caption(f'Los top 5 artistas concentran el **{top5:.1f}%** de reproducciones.')

    st.markdown('---')
    st.subheader('Géneros más populares')
    if df_clean['tag'].notna().sum() > 0:
        ng = st.slider('Nº de géneros', 5, 20, 10)
        fig_gen = plot_top_genres(df_clean, n=ng)
        if fig_gen:
            st.pyplot(fig_gen)
    else:
        st.info('No hay datos de género disponibles en el dataset actual.')

    st.markdown('---')
    st.subheader('Duración vs popularidad')
    st.pyplot(plot_duration_vs_popularity(df_clean))

    st.markdown('---')
    st.subheader('Datos del dataset')
    cols = ['name', 'artist', 'tag', 'duration_min', 'playcount',
            'listeners', 'playcount_per_listener', 'country', 'is_hit']
    cols = [c for c in cols if c in df_clean.columns]
    st.dataframe(
        df_clean[cols].sort_values('playcount', ascending=False).head(100),
        use_container_width=True
    )

# ════════════════════════════════════════════════════════════════════════════════
# PÁGINA 3 — Geografía
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == '🌍 Geografía':
    st.title('🌍 Análisis Geográfico')
    st.markdown('Tracks con país real asignado (excluye GLOBAL y UNKNOWN).')

    fig_geo = plot_geo_analysis(df_clean)
    if fig_geo:
        st.pyplot(fig_geo)
    else:
        st.warning(
            'Pocos tracks con país asignado. El análisis geográfico es limitado. '
            'Para mejorarlo: aumentar páginas en geo.getTopTracks en el pipeline.'
        )

    df_geo = df_clean[~df_clean['country'].isin(['UNKNOWN', 'GLOBAL'])].dropna(subset=['country'])
    if len(df_geo) > 0:
        st.markdown('---')
        st.subheader('Estadísticas por país')
        stats = (
            df_geo.groupby('country')
            .agg(n_tracks=('name', 'count'),
                 plays_medio=('playcount', 'mean'),
                 engagement_medio=('playcount_per_listener', 'mean'))
            .round(2)
            .sort_values('plays_medio', ascending=False)
            .reset_index()
        )
        st.dataframe(stats, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# PÁGINA 4 — Correlaciones
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == '📈 Correlaciones':
    st.title('📈 Correlaciones entre variables')
    st.markdown('Correlaciones de Spearman (robusta con distribuciones sesgadas).')

    st.pyplot(plot_correlation_heatmap(df_clean))

    st.markdown('---')
    st.subheader('Ranking de correlación con log_playcount')

    cols_posibles = [
        'log_playcount', 'log_listeners', 'playcount_per_listener',
        'duration_min', 'is_short_track', 'is_hit',
        'artist_track_count', 'track_share_of_artist', 'popularity_ratio'
    ]
    cols = [c for c in cols_posibles if c in df_clean.columns]
    corr = df_clean[cols].corr(method='spearman')

    if 'log_playcount' in corr.columns:
        tabla = (
            corr['log_playcount'].drop('log_playcount')
            .abs().sort_values(ascending=False)
            .reset_index()
        )
        tabla.columns = ['Variable', 'Correlación (|ρ|)']
        tabla['Correlación (|ρ|)'] = tabla['Correlación (|ρ|)'].round(3)
        st.dataframe(tabla, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# PÁGINA 5 — Tendencias
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == '📅 Tendencias':
    st.title('📅 Tendencias Temporales')
    st.markdown('Evolución del mercado musical según las fechas de publicación de los tracks.')

    df_time = df_clean.dropna(subset=['published']).copy()
    df_time['year'] = pd.to_datetime(df_time['published'], errors='coerce').dt.year
    df_time = df_time[(df_time['year'] >= 1950) & (df_time['year'] <= 2030)]

    cobertura = len(df_time) / len(df_clean) * 100
    if cobertura < 10:
        st.info(f'Solo el {cobertura:.1f}% de los tracks tiene fecha de publicación conocida ({len(df_time):,} de {len(df_clean):,}). Los resultados representan un subset del dataset.')

    if len(df_time) == 0:
        st.warning('No hay tracks con fecha de publicación válida.')
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric('Tracks con fecha conocida', f'{len(df_time):,}')
        c2.metric('Rango de años', f'{int(df_time["year"].min())} – {int(df_time["year"].max())}')
        año_top = int(df_time['year'].value_counts().idxmax())
        c3.metric('Año más representado', str(año_top))

        st.markdown('---')
        st.subheader('Tracks publicados por año')
        fig_year = plot_tracks_per_year(df_clean)
        if fig_year:
            st.pyplot(fig_year)

        st.markdown('---')
        st.subheader('Popularidad media por año de publicación')
        fig_pop = plot_avg_playcount_by_year(df_clean)
        if fig_pop:
            st.pyplot(fig_pop)
        st.caption('Tracks sin fecha de publicación excluidos del análisis temporal.')

# ════════════════════════════════════════════════════════════════════════════════
# PÁGINA 6 — Rankings
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == '🏆 Rankings':
    st.title('🏆 Rankings de Tracks')
    st.markdown('Los tracks más populares y con mayor engagement del dataset.')

    n = st.slider('Nº de tracks a mostrar', 10, 100, 25)

    tab1, tab2 = st.tabs(['🎵 Por popularidad (playcount)', '🔥 Por engagement (plays/oyente)'])

    with tab1:
        st.subheader(f'Top {n} tracks por reproducciones totales')
        fig_top = plot_top_tracks(df_clean, n=n)
        if fig_top:
            st.pyplot(fig_top)

        st.markdown('---')
        cols_tabla = ['name', 'artist', 'tag', 'playcount', 'listeners', 'duration_min', 'is_hit']
        cols_tabla = [c for c in cols_tabla if c in df_clean.columns]
        top_df = (
            df_clean.dropna(subset=['playcount'])
            .nlargest(n, 'playcount')[cols_tabla]
            .reset_index(drop=True)
        )
        top_df.index += 1
        st.dataframe(top_df, use_container_width=True)

    with tab2:
        st.subheader(f'Top {n} tracks por engagement (reproducciones por oyente)')
        fig_eng = plot_top_engagement(df_clean, n=n)
        if fig_eng:
            st.pyplot(fig_eng)

        st.markdown('---')
        cols_tabla2 = ['name', 'artist', 'tag', 'playcount_per_listener', 'playcount', 'listeners', 'is_hit']
        cols_tabla2 = [c for c in cols_tabla2 if c in df_clean.columns]
        eng_df = (
            df_clean
            .replace([float('inf'), float('-inf')], np.nan)
            .dropna(subset=['playcount_per_listener'])
            .nlargest(n, 'playcount_per_listener')[cols_tabla2]
            .reset_index(drop=True)
        )
        eng_df.index += 1
        st.dataframe(eng_df, use_container_width=True)
