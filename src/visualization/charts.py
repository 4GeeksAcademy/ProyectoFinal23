"""
src/visualization/charts.py
Funciones de visualización para Streamlit.
Réplica de las celdas EDA del notebook (secciones 8-9), adaptadas a Streamlit.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns


def plot_playcount_distribution(df_clean: pd.DataFrame):
    """Réplica de celda 140: histogramas playcount lineal vs log."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    p99 = df_clean['playcount'].quantile(0.99)

    axes[0].hist(df_clean['playcount'].clip(upper=p99), bins=50,
                 color='steelblue', edgecolor='white')
    axes[0].set_title('Distribución playcount (lineal)')
    axes[0].set_xlabel('Reproducciones')
    axes[0].xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'{x/1e6:.0f}M')
    )

    axes[1].hist(df_clean['log_playcount'], bins=50,
                 color='coral', edgecolor='white')
    axes[1].set_title('Distribución log_playcount')
    axes[1].set_xlabel('log(1 + playcount)')

    plt.suptitle('Transformación logarítmica', fontweight='bold')
    plt.tight_layout()
    return fig


def plot_top_artists(df_clean: pd.DataFrame, n: int = 15):
    """Réplica de celda 144: barplot top N artistas."""
    top = (
        df_clean
        .groupby('artist')[['playcount', 'name']]
        .agg({'playcount': 'sum', 'name': 'count'})
        .rename(columns={'playcount': 'total_plays', 'name': 'n_tracks'})
        .sort_values('total_plays', ascending=False)
        .head(n)
    )

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    top.sort_values('total_plays').plot.barh(
        y='total_plays', ax=axes[0], color='steelblue', legend=False
    )
    axes[0].set_title(f'Top {n} artistas por reproducciones')
    axes[0].set_xlabel('Reproducciones totales')
    axes[0].xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'{x/1e6:.0f}M')
    )

    top.sort_values('n_tracks').plot.barh(
        y='n_tracks', ax=axes[1], color='coral', legend=False
    )
    axes[1].set_title(f'Top {n} artistas por nº de tracks')
    axes[1].set_xlabel('Nº de tracks')

    plt.tight_layout()
    return fig


def plot_top_genres(df_clean: pd.DataFrame, n: int = 10):
    """Réplica de celda 146: barplot top géneros por tag."""
    df_con_tag = df_clean.dropna(subset=['tag'])
    if len(df_con_tag) == 0:
        return None

    stats = (
        df_con_tag
        .groupby('tag')
        .agg(plays_total=('playcount', 'sum'), n_tracks=('name', 'count'))
        .reset_index()
        .sort_values('plays_total', ascending=False)
        .head(n)
    )

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].barh(stats['tag'], stats['plays_total'] / 1e6,
                 color=sns.color_palette('Blues_r', n))
    axes[0].invert_yaxis()
    axes[0].set_title(f'Top {n} géneros por reproducciones')
    axes[0].set_xlabel('Millones')

    axes[1].barh(stats['tag'], stats['n_tracks'],
                 color=sns.color_palette('Oranges_r', n))
    axes[1].invert_yaxis()
    axes[1].set_title(f'Top {n} géneros por nº de tracks')
    axes[1].set_xlabel('Nº de tracks')

    plt.tight_layout()
    return fig


def plot_duration_vs_popularity(df_clean: pd.DataFrame):
    """Réplica de celda 164: duración por rangos + boxplot corta vs larga."""
    rangos = pd.cut(
        df_clean['duration_min'],
        bins=[0, 1.5, 2.5, 3.5, 4.5, 6, 100],
        labels=['<1.5m', '1.5-2.5m', '2.5-3.5m', '3.5-4.5m', '4.5-6m', '>6m']
    )
    pop = df_clean.groupby(rangos, observed=True)['log_playcount'].mean()

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    pop.plot.bar(ax=axes[0], color=sns.color_palette('RdYlGn', 6))
    axes[0].set_title('Popularidad media por rango de duración')
    axes[0].set_ylabel('log_playcount medio')
    axes[0].tick_params(axis='x', rotation=30)

    df_clean.boxplot(column='log_playcount', by='is_short_track', ax=axes[1])
    axes[1].set_xlabel('is_short_track (0=Larga, 1=Corta)')
    axes[1].set_ylabel('log_playcount')
    plt.sca(axes[1])
    plt.title('Popularidad: corta vs larga')
    plt.suptitle('')

    plt.tight_layout()
    return fig


def plot_geo_analysis(df_clean: pd.DataFrame):
    """Réplica de celda 148: análisis geográfico."""
    df_geo = df_clean[
        ~df_clean['country'].isin(['UNKNOWN', 'GLOBAL'])
    ].dropna(subset=['country'])

    if len(df_geo) == 0:
        return None

    stats = (
        df_geo.groupby('country')
        .agg(plays_medio=('playcount', 'mean'), n_tracks=('name', 'count'))
        .sort_values('plays_medio', ascending=False)
        .reset_index()
    )

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].barh(stats['country'], stats['plays_medio'] / 1e6,
                 color=sns.color_palette('Blues_r', len(stats)))
    axes[0].invert_yaxis()
    axes[0].set_title('Popularidad media por país')
    axes[0].set_xlabel('Playcount medio (millones)')

    axes[1].barh(stats['country'], stats['n_tracks'],
                 color=sns.color_palette('Oranges_r', len(stats)))
    axes[1].invert_yaxis()
    axes[1].set_title('Nº de tracks por país')

    plt.suptitle('Análisis geográfico (excluye GLOBAL y UNKNOWN)', fontweight='bold')
    plt.tight_layout()
    return fig


def plot_correlation_heatmap(df_clean: pd.DataFrame):
    """Réplica de celda 155: heatmap de correlaciones Spearman."""
    cols_posibles = [
        'log_playcount', 'log_listeners', 'playcount_per_listener',
        'duration_min', 'is_short_track', 'is_hit',
        'artist_track_count', 'track_share_of_artist', 'popularity_ratio'
    ]
    cols = [c for c in cols_posibles if c in df_clean.columns]
    corr = df_clean[cols].corr(method='spearman')

    fig, ax = plt.subplots(figsize=(10, 7))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, vmin=-1, vmax=1, linewidths=0.5, ax=ax)
    ax.set_title('Correlaciones de Spearman', fontweight='bold')
    plt.xticks(rotation=35, ha='right')
    plt.tight_layout()
    return fig


def plot_tracks_per_year(df_clean: pd.DataFrame):
    """Bar chart de tracks publicados por año."""
    df_time = df_clean.dropna(subset=['published']).copy()
    df_time['year'] = pd.to_datetime(df_time['published'], errors='coerce').dt.year
    df_time = df_time[(df_time['year'] >= 1950) & (df_time['year'] <= 2030)]

    if len(df_time) == 0:
        return None

    por_año = df_time.groupby('year').size().reset_index(name='n_tracks')

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.bar(por_año['year'], por_año['n_tracks'], color='steelblue', edgecolor='white')
    ax.set_title('Tracks por año de publicación', fontweight='bold')
    ax.set_xlabel('Año')
    ax.set_ylabel('Nº de tracks')
    plt.tight_layout()
    return fig


def plot_avg_playcount_by_year(df_clean: pd.DataFrame):
    """Line chart de playcount medio por año de publicación."""
    df_time = df_clean.dropna(subset=['published', 'playcount']).copy()
    df_time['year'] = pd.to_datetime(df_time['published'], errors='coerce').dt.year
    df_time = df_time[(df_time['year'] >= 1950) & (df_time['year'] <= 2030)]

    if len(df_time) == 0:
        return None

    por_año = df_time.groupby('year')['playcount'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(por_año['year'], por_año['playcount'], color='coral', marker='o', linewidth=2, markersize=4)
    ax.set_title('Playcount medio por año de publicación', fontweight='bold')
    ax.set_xlabel('Año')
    ax.set_ylabel('Reproducciones medias')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
    plt.tight_layout()
    return fig


def plot_top_tracks(df_clean: pd.DataFrame, n: int = 25):
    """Horizontal bar chart de los top N tracks por playcount."""
    top = (
        df_clean
        .dropna(subset=['playcount'])
        .nlargest(n, 'playcount')
        .sort_values('playcount')
    )
    top['label'] = top['artist'] + ' — ' + top['name']

    fig, ax = plt.subplots(figsize=(12, max(4, n * 0.35)))
    ax.barh(top['label'], top['playcount'], color='steelblue')
    ax.set_title(f'Top {n} tracks por reproducciones', fontweight='bold')
    ax.set_xlabel('Reproducciones')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.0f}M'))
    plt.tight_layout()
    return fig


def plot_top_engagement(df_clean: pd.DataFrame, n: int = 25):
    """Horizontal bar chart de los top N tracks por playcount_per_listener."""
    top = (
        df_clean
        .replace([float('inf'), float('-inf')], np.nan)
        .dropna(subset=['playcount_per_listener'])
        .nlargest(n, 'playcount_per_listener')
        .sort_values('playcount_per_listener')
    )
    top['label'] = top['artist'] + ' — ' + top['name']

    fig, ax = plt.subplots(figsize=(12, max(4, n * 0.35)))
    ax.barh(top['label'], top['playcount_per_listener'], color='coral')
    ax.set_title(f'Top {n} tracks por engagement (plays / oyente)', fontweight='bold')
    ax.set_xlabel('Reproducciones por oyente')
    plt.tight_layout()
    return fig
