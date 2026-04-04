"""
train_model.py
Entrena el RandomForestClassifier y guarda los artefactos en models/.

Uso:
    python train_model.py

Genera:
    models/modelo_hits_clf.pkl
    models/le_tag.pkl
    models/features.txt
"""

import os
import sys
import joblib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from data.load_data import load_df_merged
from data.process_data import clean_and_feature_engineer, prepare_ml_dataset

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

print('Cargando datos...')
df_merged = load_df_merged()

print('Limpieza y feature engineering...')
df_clean, le_tag, FEATURES = clean_and_feature_engineer(df_merged)

print('Preparando dataset ML...')
X, y_clf, _ = prepare_ml_dataset(df_clean, FEATURES)
print(f'  Filas válidas: {len(X):,} | Features: {FEATURES}')
print(f'  Hits: {y_clf.sum():,} ({y_clf.mean()*100:.1f}%)')

X_train, X_test, y_train, y_test = train_test_split(
    X, y_clf, test_size=0.2, random_state=42, stratify=y_clf
)

print('Entrenando RandomForestClassifier...')
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_clf.fit(X_train, y_train)

y_pred = rf_clf.predict(X_test)
print('\n=== Clasificación (is_hit) ===')
print(classification_report(y_test, y_pred, target_names=['No hit', 'Hit']))

print('Guardando artefactos...')
joblib.dump(rf_clf, os.path.join(MODELS_DIR, 'modelo_hits_clf.pkl'))
joblib.dump(le_tag, os.path.join(MODELS_DIR, 'le_tag.pkl'))
with open(os.path.join(MODELS_DIR, 'features.txt'), 'w') as f:
    f.write('\n'.join(FEATURES))

print('✅ Modelos guardados en models/')
print('   modelo_hits_clf.pkl')
print('   le_tag.pkl')
print('   features.txt')
print('\nAhora puedes lanzar: streamlit run src/app.py')
