# BI Project

Resumen

Este proyecto es un dashboard BI sencillo con backend en FastAPI (Python) y frontend estático (HTML/JS). Permite consultar colecciones tipo fact (ventas, inventario, distribución, abastecimiento, fabricación, combos), calcular métricas y ejecutar clustering y recomendación.

Características principales

- Endpoints para consultas por tabla de hechos.
- Cálculo de métricas por tabla usando pandas.
- Clustering por tabla con KMeans (resúmenes, interpretaciones, conteos).
- Recomendadores: filtrado colaborativo (por cliente), recomendador por similitud basado en inventario, y content-based.
- Frontend ligero con visualizaciones (Chart.js) y controles para seleccionar tablas, generar clusters y pedir recomendaciones.

Estructura del proyecto

- back/: backend FastAPI
  - app/
    - main.py                 -> aplicación FastAPI, inclusión de rutas
    - routes/
      - metrics_routes.py
      - clustering_routes.py
      - recommendation_routes.py
      - query_routes.py
    - services/
      - clustering_service.py
      - metrics_service.py
      - general_service.py
      - recommendation/
        - collaborative.py
        - content_based.py
        - similarity.py
        - inventory_similarity.py
    - repositories/
      - general_repository.py
      - ventas_repository.py
      - inventario_repository.py
    - utils/
      - dataframe_builder.py
  - requirements.txt
  - run.py                  -> entry para iniciar uvicorn

- front/: frontend estático
  - index.html
  - js/
    - api.js                 -> `API_URL` base
    - app.js
    - clustering.js
    - recommendation.js
    - metrics.js
  - css/
    - styles.css

Endpoints principales

- Consultas (GET)
  - `/factventas`, `/factinventario`, `/factdistribucion`, `/factfabricacion`, `/factabastecimiento`, `/factventascombo`

- Métricas (GET)
  - `/metrics/{table}`  — `table` en minúsculas: `factventas`, `factinventario`, etc.

- Clustering (GET)
  - `/clusters/{table}?k=3&sample=500` — devuelve `summaries`, `counts`, `interpretations` y opcionalmente `records` (muestreo)

- Recomendaciones (GET)
  - `/recommend/collaborative/{cliente_key}?n=5` — filtrado colaborativo (item-based) por cliente
  - `/recommend/content/{producto}?n=5` — content-based por nombre de producto
  - `/recommend/similarity/{producto}` — similitud por ventas (método previo)
  - `/recommend/inventory/similarity/{producto}?n=5` — nueva similitud basada en inventario (Stock/Ventas/Reposiciones)

Notas de implementación

- El backend usa pandas y scikit-learn para procesado y modelos (KMeans, StandardScaler, cosine similarity).
- Para evitar sobrecargar el frontend con grandes volúmenes, los endpoints de clustering aceptan `sample`, `limit` y `page` que permiten devolver solo una muestra o una página de `records` mientras `summaries` y `counts` cubren los gráficos.
- Las reglas de asociación fueron removidas y reemplazadas por el recomendador de inventario según requerimiento.

Instalación y ejecución

1. Crear un entorno virtual (recomendado) e instalar dependencias:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r back/requirements.txt
```

2. Iniciar backend (desde `back/`):

```bash
py .\run.py
# o
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

3. Servir frontend (desde `front/`):

```bash
# desde la carpeta front
py -m http.server 5500
# abrir http://localhost:5500
```

Consideraciones y recomendaciones

- Rendimiento: si los conjuntos son grandes (p. ej. >100k filas), conviene:
  - paginar respuestas o devolver solo `summaries` + muestras, y
  - cachear resultados de operaciones costosas (Apriori, similitudes precomputadas, clusters) con TTL.

- Serialización: el backend convierte tipos numpy/pandas a tipos nativos para JSON.

- Seguridad / Producción: revisar CORS, límites de petición, y configurar un servidor ASGI en producción (Gunicorn/uvicorn con workers), además de la protección de acceso a la base de datos.

Cómo contribuir

- Ejecuta tests locales (si los añades) y sigue el patrón repo->service->route para nuevas funcionalidades.
- Mantén las dependencias en `back/requirements.txt`.

Contacto

- Este README fue generado y actualizado automáticamente por el asistente de desarrollo. Para cambios adicionales dime qué sección quieres ampliar.
