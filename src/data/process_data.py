"""
src/data/process_data.py
Feature engineering — replica la lógica del notebook (secciones 6-7).

COLUMNA DE GÉNERO:
  El notebook usa 'tag' (de backup_tracks, limpiada con get_first_tag).
  El encoder se llama le_tag y produce 'tag_encoded'.
  FEATURES = ['log_listeners', 'duration_min', 'is_short_track', 'tag_encoded',
              'artist_track_count', 'track_share_of_artist', 'playcount_per_listener']
"""

import ast
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def get_first_tag(x):
    """
    Extrae el nombre del primer tag válido de la lista de dicts de Last.fm.
    Réplica de la función get_first_tag del notebook (celda 69).
    """
    if pd.isna(x):
        return np.nan
    try:
        tags = ast.literal_eval(x)
        if isinstance(tags, list) and len(tags) > 0:
            return tags[0].get('name', np.nan)
    except Exception:
        return np.nan
    return np.nan


def clean_and_feature_engineer(df_merged: pd.DataFrame):
    """
    Aplica la limpieza y feature engineering del notebook sobre df_merged.
    Devuelve (df_clean, le_tag, FEATURES).

    FEATURES resultantes:
        log_listeners, duration_min, is_short_track, tag_encoded,
        artist_track_count, track_share_of_artist, playcount_per_listener
    """
    df = df_merged.copy()

    # ── Tipos correctos (celda 80) ────────────────────────────────────────────
    for col in ['duration', 'listeners', 'playcount']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # ── Limpiar name/artist (celda 84 corregida) ──────────────────────────────
    df = df.dropna(subset=['name', 'artist'])

    # ── Columna tag (celda 69) ────────────────────────────────────────────────
    df['tag_clean'] = df['tag'].apply(get_first_tag)
    df['tag']       = df['tag_clean']

    # ── Fecha publicación (celda 72) ──────────────────────────────────────────
    df['published_date'] = pd.to_datetime(
        df['published'], format='%d %b %Y, %H:%M', errors='coerce'
    ).dt.date
    df['published'] = df['published_date']

    # ── duration_min (celda 74) — duración en MILISEGUNDOS en backup_tracks ───
    df['duration_min'] = (df['duration'] / 60000).round(2)

    # ── Features (sección 7) ──────────────────────────────────────────────────

    # is_short_track: < 2.5 min (celda 109 — la correcta, NO la 110)
    df['is_short_track'] = (df['duration_min'] < 2.5).astype(int)

    # is_hit: top 10% por playcount (celda 112)
    threshold = df['playcount'].quantile(0.90)
    df['is_hit'] = (df['playcount'] >= threshold).astype(int)

    # Engagement (celda 116)
    df['playcount_per_listener'] = (
        df['playcount'] / df['listeners'].replace(0, np.nan)
    )

    # Transformaciones logarítmicas (celda 118)
    df['log_playcount'] = np.log1p(df['playcount'])
    df['log_listeners'] = np.log1p(df['listeners'])

    # Ratios de popularidad (celdas 122, 124)
    df['popularity_ratio']      = df['playcount'] / df['playcount'].sum()
    df['listener_to_play_ratio'] = df['listeners'] / df['playcount'].replace(0, np.nan)

    # Estadísticas por artista (celda 126)
    artist_stats = df.groupby('artist').agg(
        artist_track_count    =('name', 'count'),
        artist_total_playcount=('playcount', 'sum')
    ).reset_index()
    df = df.merge(artist_stats, on='artist', how='left')

    # Top artistas (celda 130-131)
    top_artists = (
        df.groupby('artist')[['playcount', 'name']]
        .agg({'playcount': 'sum', 'name': 'count'})
        .rename(columns={'playcount': 'total_plays', 'name': 'n_tracks'})
        .sort_values('total_plays', ascending=False)
    )
    df = df.merge(top_artists, on='artist', how='left')

    # track_share_of_artist (celda 133)
    df['track_share_of_artist'] = df['playcount'] / df['total_plays']

    # ── Encoding de género — le_tag sobre columna 'tag' (celda 173) ──────────
    le_tag = LabelEncoder()
    df['tag_encoded'] = le_tag.fit_transform(df['tag'].fillna('unknown'))

    # ── FEATURES: mismo orden y nombres que el notebook ───────────────────────
    FEATURES = [
        'log_listeners',
        'duration_min',
        'is_short_track',
        'tag_encoded',
        'artist_track_count',
        'track_share_of_artist',
        'playcount_per_listener',
    ]
    FEATURES = [f for f in FEATURES if f in df.columns]

    df_clean = df.copy()
    return df_clean, le_tag, FEATURES


def prepare_ml_dataset(df_clean: pd.DataFrame, FEATURES: list):
    """Devuelve X, y_clf, y_reg listos para train_test_split."""
    df_ml_ok = df_clean[FEATURES + ['log_playcount', 'is_hit']].dropna()
    X     = df_ml_ok[FEATURES]
    y_clf = df_ml_ok['is_hit']
    y_reg = df_ml_ok['log_playcount']
    return X, y_clf, y_reg
