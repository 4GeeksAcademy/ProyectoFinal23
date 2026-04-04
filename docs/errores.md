# Cuaderno de Errores, Soluciones y Evolución del Proyecto

🎵 **ProyectoFinal23**
Análisis del Mercado Musical y Detección de Fraude en Streams

- **Repositorio:** github.com/JaimeAFL/ProyectoFinal23
- **Fuentes:** Last.fm API + AcousticBrainz API
- **Última actualización:** 04/04/2026

---

## Propósito del documento

Registro cronológico de errores, decisiones técnicas y evolución del proyecto. Dos objetivos:

- **Depuración:** volver a cualquier error pasado con diagnóstico y solución exactos.
- **Entrevistas técnicas:** cada error incluye la terminología profesional y la respuesta tipo que usaría un desarrollador senior.

El proyecto tiene dos módulos independientes en notebooks separados:

- **Módulo 1** — Análisis del mercado musical: EDA + predicción de popularidad.
- **Módulo 2** — Detección de fraude en streams: anomaly detection sobre comportamiento de usuario.

**Requisitos:** 60.000 registros mínimo, 20 columnas.

---

## Sistema de etiquetas

| Etiqueta | Qué significa |
|----------|--------------|
| [ENV] | Environment — entorno Python, dependencias, rutas |
| [VCS] | Version Control System — Git, GitHub |
| [HTTP] | HTTP / Networking — llamadas a APIs |
| [AUTH] | Authentication — API keys, tokens |
| [DATA] | Data Quality — calidad o estructura de datos |
| [CONFIG] | Configuration — variables de entorno, secrets |
| [ML] | Machine Learning — modelos, features, métricas |
| [EDA] | Exploratory Data Analysis |
| [SCRAPING] | Web Scraping |
| [NOTEBOOK] | Jupyter Notebook |

| Subcategoría | Qué significa |
|--------------|--------------|
| [DEPS] | Dependencies |
| [RATE-LIMIT] | Rate Limit |
| [TIMEOUT] | Timeout |
| [MISSING-DATA] | Missing Data |
| [SCHEMA] | Schema Mismatch |
| [SECRETS] | Secrets Management |
| [BATCH] | Batch Processing |
| [PAGINATION] | Pagination |
| [FEATURE-ENG] | Feature Engineering |
| [COVERAGE] | Coverage — baja cobertura entre fuentes |
| [DEPRECATION] | Deprecation — API discontinuada |
| [SILENT-FAIL] | Silent Failure — fallo sin error visible |
| [LEAKAGE] | Data Leakage — datos del futuro en el entrenamiento |

---

## Índice de errores y decisiones

| # | Fecha | Error / Decisión | Módulo | Categorías | Estado |
|---|-------|-----------------|--------|------------|--------|
| 1 | 20/03/2026 | ModuleNotFoundError: No module named 'requests' | M1+M2 | [ENV][DEPS] | ✅ Resuelto |
| 2 | 20/03/2026 | .gitignore en carpeta incorrecta — .env expuesto | M1+M2 | [VCS][CONFIG][SECRETS] | ✅ Resuelto |
| 3 | 20/03/2026 | 403 Forbidden en Wikipedia REST API | M1 | [HTTP][AUTH] | ✅ Resuelto |
| 4 | 20/03/2026 | 429 Too Many Requests en Last.fm — volumen insuficiente | M1+M2 | [HTTP][RATE-LIMIT][BATCH] | ✅ Resuelto |
| 5 | 20/03/2026 | 0 key prices en scraping de Numbeo (silent failure) | M1 | [SCRAPING][DATA][SILENT-FAIL] | ✅ Resuelto |
| 6 | 20/03/2026 | 46 errores, 0 lugares en Google Places API (New) | M1 | [HTTP][AUTH][SCHEMA] | ⏳ Pendiente |
| 7 | 27/03/2026 | AcousticBrainz: ~98% NaN — API discontinuada | M1 | [DATA][MISSING-DATA][DEPRECATION][COVERAGE] | ✅ Documentado |
| 8 | 27/03/2026 | KeyboardInterrupt en pipeline AcousticBrainz (~45 min) | M1 | [HTTP][TIMEOUT][BATCH] | ✅ Resuelto |
| 9 | 27/03/2026 | ModuleNotFoundError: No module named 'bs4' | M1 | [ENV][DEPS] | ✅ Resuelto |
| 10 | 27/03/2026 | duration=0 tratada como dato válido — error silencioso | M1 | [DATA][SILENT-FAIL][EDA] | ✅ Corregido |
| 11 | 27/03/2026 | Duration en segundos etiquetada como 'minutos' | M1 | [DATA][EDA] | ✅ Corregido |
| 12 | 28/03/2026 | df_clean no definido entre notebooks | M1 | [NOTEBOOK][DATA] | ⏳ Pendiente |
| 13 | 03/04/2026 | Archivos Python en raíz en vez de `src/` | M1 | [VCS][CONFIG] | ✅ Resuelto |
| 14 | 03/04/2026 | CONFLICT (file/directory): `src/data` durante rebase | M1 | [VCS] | ✅ Resuelto |
| 15 | 03/04/2026 | `git push origin nombre-de-la-rama` copiado literalmente | M1+M2 | [VCS] | ✅ Resuelto |
| 16 | 03/04/2026 | PR apuntaba a `4GeeksAcademy:main` en vez de fork | M1+M2 | [VCS] | ✅ Resuelto |
| 17 | 04/04/2026 | RandomForest accuracy=1.00 — data leakage | M1 | [ML][FEATURE-ENG][LEAKAGE] | ⚠️ Documentado |

---

## Errores detallados

---

### #1 — ModuleNotFoundError: No module named 'requests'
**Fecha:** 20/03/2026 | **Módulo:** M1+M2 | **Estado:** ✅ Resuelto
**Etiquetas:** [ENV] [DEPS]

**Causa raíz**
El entorno virtual `.venv` se creó vacío. Las librerías necesarias no estaban instaladas.

**Solución**
```bash
pip install requests beautifulsoup4 python-dotenv
pip freeze > requirements.txt
```

**Para recordar en una entrevista**
> Uso entornos virtuales para aislar dependencias. Al crear un venv hay que instalar explícitamente las dependencias y documentarlas en `requirements.txt` con `pip freeze`.

---

### #2 — .gitignore en carpeta incorrecta — .env expuesto
**Fecha:** 20/03/2026 | **Módulo:** M1+M2 | **Estado:** ✅ Resuelto
**Etiquetas:** [VCS] [CONFIG] [SECRETS]

**Causa raíz**
El `.gitignore` estaba en una subcarpeta. Git solo lo aplica desde su nivel hacia abajo.

**Solución**
```bash
mv subcarpeta/.gitignore .gitignore
git rm --cached .env
```

**Para recordar en una entrevista**
> El `.gitignore` debe estar en la raíz. Si una key se sube accidentalmente, hay que revocarla inmediatamente — aunque se elimine del histórico de Git, cualquier bot puede haberla capturado.

---

### #3 — 403 Forbidden en Wikipedia REST API
**Fecha:** 20/03/2026 | **Módulo:** M1 | **Estado:** ✅ Resuelto
**Etiquetas:** [HTTP] [AUTH]

**Causa raíz**
Wikipedia rechaza peticiones sin User-Agent identificado.

**Solución**
```python
headers = {'User-Agent': 'ProyectoFinal23/1.0 (bootcamp-data-analysis)'}
response = requests.get(url, headers=headers)
```

---

### #4 — 429 Too Many Requests en Last.fm — volumen insuficiente
**Fecha:** 20/03/2026 → 27/03/2026 | **Módulo:** M1+M2 | **Estado:** ✅ Resuelto
**Etiquetas:** [HTTP] [RATE-LIMIT] [BATCH] [PAGINATION]

**Causa raíz**
Sin throttling adecuado. Un solo endpoint no alcanza los 60.000 registros objetivo.

**Solución**
```python
DELAY = 0.25  # 4 req/s — margen bajo el límite de 5/s
# Estrategia multi-endpoint:
# chart.getTopTracks + geo.getTopTracks (10 países) + tag.getTopTracks (10 géneros)
# Checkpoints cada 25 páginas para tolerar interrupciones
```

**Para recordar en una entrevista**
> Implemento throttling con `time.sleep()` y combino múltiples endpoints. Guardo checkpoints cada N páginas para tolerar interrupciones. Para errores 429 uso retry con backoff exponencial: 2s, 4s, 8s...

---

### #5 — 0 key prices en scraping de Numbeo (silent failure)
**Fecha:** 20/03/2026 | **Módulo:** M1 | **Estado:** ✅ Resuelto
**Etiquetas:** [SCRAPING] [DATA] [SILENT-FAIL]

**Causa raíz**
Matching de texto exacto. Numbeo puede cambiar 'City Centre' por 'City Center' sin previo aviso.

**Solución**
```python
# ❌ Matching exacto, frágil:
key_map = {'rent_1br_center': 'Apartment (1 bedroom) in City Centre'}
# ✅ Keyword parcial estable:
key_map = {'rent_1br_center': '1 bedroom) in City'}
```

---

### #6 — 46 errores, 0 lugares en Google Places API (New)
**Fecha:** 20/03/2026 | **Módulo:** M1 | **Estado:** ⏳ Pendiente activación en Google Cloud Console
**Etiquetas:** [HTTP] [AUTH] [SCHEMA]

**Causa raíz**
Google tiene dos versiones de Places API con URLs y autenticación distintas. La key solo tenía permisos para la legacy.

**Solución pendiente**
Ir a `console.cloud.google.com` → APIs → Biblioteca → activar "Places API (New)".

---

### #7 — AcousticBrainz: ~98% NaN — API discontinuada
**Fecha:** 27/03/2026 | **Módulo:** M1 | **Estado:** ✅ Documentado
**Etiquetas:** [DATA] [MISSING-DATA] [DEPRECATION] [COVERAGE]

**Contexto**
AcousticBrainz se discontinuó en septiembre de 2022. Los tracks de Last.fm son mayoritariamente recientes (2022-2025) — sus MBIDs no existen en la base de datos congelada.

**Decisión**
Mantener como enriquecimiento para el subset válido (~1.75%). Documentar explícitamente la limitación. Alternativa futura: Spotify Audio Features API.

**Para recordar en una entrevista**
> Un 98% de NaN indica que la fuente no es viable como columna principal. Identifiqué la causa raíz (API discontinuada, no error de código) y la decisión fue mantenerla como enriquecimiento para un subset válido.

---

### #8 — KeyboardInterrupt en pipeline AcousticBrainz (~45 min)
**Fecha:** 27/03/2026 | **Módulo:** M1 | **Estado:** ✅ Resuelto
**Etiquetas:** [HTTP] [TIMEOUT] [BATCH]

**Solución — checkpoints e idempotencia**
```python
CHECKPOINT_EVERY_N = 500
# Al reanudar, cargar el último checkpoint:
checkpoints = sorted(glob.glob('checkpoint_*.csv'))
if checkpoints:
    df_resultado = pd.read_csv(checkpoints[-1])
    ya_procesados = set(df_resultado['mbid'].dropna())
    df_restantes = df_clean[~df_clean['mbid'].isin(ya_procesados)]
```

**Para recordar en una entrevista**
> Un pipeline es idempotente si puedes ejecutarlo múltiples veces sin duplicar datos. Los checkpoints permiten reanudar sin reprocesar lo ya hecho.

---

### #9 — ModuleNotFoundError: No module named 'bs4'
**Fecha:** 27/03/2026 | **Módulo:** M1 | **Estado:** ✅ Resuelto
**Etiquetas:** [ENV] [DEPS]

**Solución**
```bash
pip install beautifulsoup4
```
Nina Protocol descartada como fuente por baja fiabilidad del HTML.

---

### #10 — duration=0 tratada como dato válido — error silencioso
**Fecha:** 27/03/2026 | **Módulo:** M1 | **Estado:** ✅ Corregido
**Etiquetas:** [DATA] [SILENT-FAIL] [EDA]

**Causa raíz**
Last.fm devuelve `duration=0` cuando no tiene el dato (valor centinela). El código lo propagaba sin advertencia.

**Corrección**
```python
df['duration'] = df['duration'].replace(0, np.nan)
df['duration'] = df['duration'].fillna(df['duration'].median())
```

**Para recordar en una entrevista**
> Los valores centinela (0, -1, 9999) parecen datos normales pero significan "no disponible". Para detectarlos: revisar la distribución, buscar picos anómalos y cruzar con la documentación de la API.

---

### #11 — duration en segundos etiquetada como 'minutos'
**Fecha:** 27/03/2026 | **Módulo:** M1 | **Estado:** ✅ Corregido
**Etiquetas:** [DATA] [EDA]

**Síntoma**
`Good Luck, Babe! → 218 minutos` ← debería ser 3m 38s.

**Causa raíz**
Last.fm devuelve duración en segundos, no en minutos. El campo se llama `duration` sin especificar unidad.

**Corrección**
```python
df_clean['duration_min'] = df_clean['duration'] / 60  # segundos → minutos
```

**Para recordar en una entrevista**
> Hago sanity checks cruzando valores conocidos. 'Mr. Brightside' dura 3m 42s: si la API devuelve 222 y el resultado son 222 minutos, algo va mal.

---

### #12 — df_clean no definido entre notebooks
**Fecha:** 28/03/2026 | **Módulo:** M1 | **Estado:** ⏳ Pendiente de solución definitiva
**Etiquetas:** [NOTEBOOK] [DATA]

**Causa raíz**
Cada notebook tiene su propio kernel. Las variables no se comparten entre notebooks.

**Solución**
```python
# Al final del notebook de limpieza:
df_clean.to_csv('lastfm_clean_eda.csv', index=False)
# Al principio del notebook EDA:
df_clean = pd.read_csv('lastfm_clean_eda.csv', low_memory=False)
```

**Para recordar en una entrevista**
> Cada notebook tiene una responsabilidad única. La "comunicación" entre notebooks se hace a través de archivos CSV/Parquet, no variables en memoria.

---

### #13 — Archivos Python en raíz en vez de `src/` — mismatch estructura repo
**Fecha:** 03/04/2026 | **Módulo:** M1 | **Estado:** ✅ Resuelto
**Etiquetas:** [VCS] [CONFIG]

**Síntoma**
`load_data.py`, `process_data.py`, `predict.py` y `charts.py` estaban en la raíz. Los imports de `src/app.py` (`from data.load_data import ...`) fallaban.

**Causa raíz**
Los archivos tenían en su docstring su ubicación correcta y sus rutas relativas escritas para funcionar desde `src/data/` y `src/models/`. Nunca se movieron al lugar correcto durante el desarrollo inicial.

**Impacto adicional**
Las rutas `os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')` eran correctas para `src/data/` pero apuntaban fuera del repo desde la raíz.

**Solución**
```bash
git mv load_data.py src/data/load_data.py
git mv process_data.py src/data/process_data.py
git mv predict.py src/models/predict.py
git mv charts.py src/visualization/charts.py
```
Sin cambios de código — los archivos ya estaban escritos para esta estructura.

**Para recordar en una entrevista**
> La estructura estándar para una app Streamlit separa: `src/data/` (carga/procesado), `src/models/` (inferencia), `src/visualization/` (gráficos). Cada subcarpeta necesita `__init__.py` para ser importable como paquete Python.

---

### #14 — CONFLICT (file/directory): `src/data` durante rebase sobre upstream
**Fecha:** 03/04/2026 | **Módulo:** M1 | **Estado:** ✅ Resuelto
**Etiquetas:** [VCS]

**Mensaje de error**
```
CONFLICT (file/directory): directory in the way of src/data from HEAD;
moving it to src/data~HEAD instead.
```

**Causa raíz**
El upstream (`4GeeksAcademy:main`) ya había hecho la misma reorganización. Ambas ramas gestionaban `src/data/` de formas distintas en su historial, aunque el contenido final era idéntico.

**Diagnóstico clave**
```bash
git ls-tree -r FETCH_HEAD --name-only   # árbol upstream
git ls-tree -r HEAD --name-only          # árbol nuestro
# Resultado: idénticos → conflicto solo de historial, no de contenido
```

**Solución**
```bash
git rebase --abort
git checkout main
git merge origin/claude/organize-streamlit-structure-BdAw0
git push origin main
```

**Para recordar en una entrevista**
> El conflicto file/directory ocurre cuando una rama tiene un fichero donde otra tiene un directorio. Si el contenido final es idéntico, la solución es resetear al upstream y mergear por vía directa.

---

### #15 — `git push origin nombre-de-la-rama` — placeholder copiado literalmente
**Fecha:** 03/04/2026 | **Módulo:** M1+M2 | **Estado:** ✅ Resuelto
**Etiquetas:** [VCS]

**Mensaje de error**
```
[main 6c1d091] fix: forzar re-evaluación de conflicto
error: src refspec nombre-de-la-rama does not match any
```

**Causa raíz**
El comando de ejemplo incluía `nombre-de-la-rama` como placeholder y se ejecutó literalmente. El commit se hizo en `main` local en vez de en la rama de trabajo.

**Solución**
```bash
git reset HEAD~1          # deshace el commit en main local
git checkout claude/organize-streamlit-structure-BdAw0
```

**Para recordar en una entrevista**
> Si un commit no se ha pusheado, `git reset HEAD~1` lo deshace preservando los cambios. Si ya se pusheó, usar `git revert` para no reescribir historia compartida.

---

### #16 — PR apuntaba a `4GeeksAcademy:main` en vez de fork propio
**Fecha:** 03/04/2026 | **Módulo:** M1+M2 | **Estado:** ✅ Resuelto
**Etiquetas:** [VCS]

**Causa raíz**
Al crear una PR desde un fork, GitHub apunta por defecto al repositorio original (upstream), no al fork propio.

**Solución**
```bash
# Merge directo en el fork, sin PR hacia el upstream:
git checkout main
git fetch origin
git merge origin/nombre-de-la-rama
git push origin main
```

**Para recordar en una entrevista**
> Un fork es una copia del repositorio bajo tu cuenta. Las PRs desde un fork apuntan por defecto al repo original. Para integrar cambios en tu propio fork, hacer el merge directamente por terminal.

---

### #17 — RandomForest accuracy=1.00 — data leakage
**Fecha:** 04/04/2026 | **Módulo:** M1 | **Estado:** ⚠️ Documentado — limitación conocida
**Etiquetas:** [ML] [FEATURE-ENG] [LEAKAGE]

**Síntoma**
```
=== Clasificación (is_hit) ===
              precision    recall  f1-score
      No hit       1.00      1.00      1.00
         Hit       1.00      1.00      1.00
    accuracy                           1.00
```

**Causa raíz**
`is_hit` se define como "top 10% por `playcount`" sobre el mismo dataset. El modelo usa `log_listeners` como feature, que está altamente correlacionado con `playcount` (Spearman ~0.95). El modelo aprende que "muchos oyentes = hit" de forma trivial, porque esa relación está en los datos de entrenamiento.

Esto es **data leakage**: la variable objetivo (`is_hit`) fue construida con información derivada de las mismas features que usa el modelo.

**Impacto**
- El predictor **funciona** para la app (predice popularidad histórica de un track con características similares)
- **No funciona** para predecir el potencial futuro de una canción nueva que aún no tiene oyentes reales
- Las métricas de evaluación son infladas y no representan capacidad real de generalización

**Alternativas para corregir**
| Enfoque | Descripción |
|---------|-------------|
| Temporal split | Entrenar con tracks de años anteriores, evaluar en tracks recientes |
| Excluir `log_listeners` | No usar features derivadas de la popularidad para predecir popularidad |
| Target engineering | Redefinir `is_hit` usando datos externos (charts, ventas) en vez del mismo dataset |

**Para recordar en una entrevista**
> Data leakage ocurre cuando el modelo tiene acceso (directo o indirecto) a información que no estaría disponible en producción. En este caso, `log_listeners` correlaciona trivialmente con `is_hit` porque ambas son transformaciones del mismo `playcount`. La solución es un temporal split o redefinir el target con datos externos.

---

## Estado actual y próximos pasos

### Módulo 1 — Análisis del Mercado Musical

| Tarea | Prioridad | Estado |
|-------|-----------|--------|
| Recolección multi-endpoint (60k tracks) | 🔴 Alta | ✅ Completado |
| Limpieza y corrección de errores data | 🔴 Alta | ✅ Completado |
| Feature engineering (20 columnas) | 🔴 Alta | ✅ Completado |
| EDA completo | 🔴 Alta | ✅ Completado |
| App Streamlit (6 páginas) | 🔴 Alta | ✅ Completado |
| Modelo ML (Random Forest) | 🔴 Alta | ✅ Completado |
| Corregir data leakage en modelo | 🟡 Media | ⏳ Pendiente |
| Google Places API (New) | 🟡 Media | ⏳ Pendiente |
| Spotify Audio Features (alternativa AcousticBrainz) | 🟡 Media | ⏳ Pendiente |

### Módulo 2 — Detección de Fraude en Streams

| Tarea | Prioridad | Estado |
|-------|-----------|--------|
| Diseño del schema de logs de usuario | 🔴 Alta | ⏳ Pendiente |
| Feature engineering: time_between_streams, entropía | 🔴 Alta | ⏳ Pendiente |
| EDA: distribución de intervalos, outliers | 🟡 Media | ⏳ Pendiente |
| Modelo Isolation Forest | 🟡 Media | ⏳ Pendiente |
| Dashboard: fraud score por usuario | 🟢 Baja | ⏳ Pendiente |
