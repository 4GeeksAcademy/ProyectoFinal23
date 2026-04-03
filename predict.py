"""
src/models/predict.py
Carga el modelo desde disco y expone predict_hit().

El modelo fue entrenado con FEATURES (notebook celdas 173-183):
    log_listeners, duration_min, is_short_track, tag_encoded,
    artist_track_count, track_share_of_artist, playcount_per_listener

El encoder de género es le_tag (columna 'tag' de backup_tracks).
"""

import os
import numpy as np
import pandas as pd
import joblib

MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'models')


def load_model():
    """
    Carga rf_clf, le_tag y FEATURES desde disco.
    Lanza FileNotFoundError si los archivos no existen aún.
    """
    clf_path      = os.path.join(MODELS_DIR, 'modelo_hits_clf.pkl')
    le_tag_path   = os.path.join(MODELS_DIR, 'le_tag.pkl')
    features_path = os.path.join(MODELS_DIR, 'features.txt')

    if not os.path.exists(clf_path):
        raise FileNotFoundError(
            f'Modelo no encontrado en {clf_path}. '
            'Ejecuta las celdas 173-183 del notebook y luego el bloque de guardado.'
        )

    rf_clf = joblib.load(clf_path)
    le_tag = joblib.load(le_tag_path)
    with open(features_path) as f:
        FEATURES = [line.strip() for line in f if line.strip()]

    return rf_clf, le_tag, FEATURES


def predict_hit(
    duracion_min: float,
    genero: str,
    oyentes_estimados: float,
    rf_clf=None,
    le_tag=None,
    FEATURES: list = None
) -> dict:
    """
    Predice la probabilidad de que una canción sea un hit.

    Devuelve dict con: probability (0-100), label, emoji.
    """
    if rf_clf is None:
        rf_clf, le_tag, FEATURES = load_model()

    # Encoding de género con le_tag
    genero_enc = (
        le_tag.transform([genero])[0]
        if genero in le_tag.classes_
        else 0
    )

    fila = {
        'log_listeners'          : np.log1p(oyentes_estimados),
        'duration_min'           : duracion_min,
        'is_short_track'         : int(duracion_min < 2.5),
        'tag_encoded'            : genero_enc,
        'artist_track_count'     : 1,
        'track_share_of_artist'  : 1.0,
        'playcount_per_listener' : 5.0,
    }

    datos = pd.DataFrame([fila])[FEATURES]
    prob  = rf_clf.predict_proba(datos)[0][1] * 100

    if prob >= 70:
        label, emoji = 'Hit potencial', '🚀'
    elif prob >= 45:
        label, emoji = 'Potencial medio', '🟡'
    else:
        label, emoji = 'Bajo potencial', '📉'

    return {'probability': prob, 'label': label, 'emoji': emoji}
