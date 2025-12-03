# Proyecto Extra – Aplicación Web (FastAPI + Neo4J Aura)

Aplicación web simple que expone las operaciones CRUD definidas en el proyecto principal. **Esta versión usa Neo4j Aura (cloud) en lugar de un contenedor local.**

## ⚠️ Versiones Disponibles

Este repositorio tiene dos ramas principales:

- **`proyecto-extra-solo`**: Versión 100% local con Docker (Neo4j + FastAPI)
- **`proyecto-extra-aura`**: Versión cloud con Neo4j Aura (solo FastAPI en Docker) ← **Estás aquí**

## Estructura

```
proyecto-extra/
├── docker-compose.yml        # Configuración local (Neo4j + FastAPI)
├── docker-compose.aura.yml   # Configuración cloud (solo FastAPI)
├── .env.example              # Variables de entorno para Aura
├── run.sh                    # Script local (Mac/Linux)
├── run.bat                   # Script local (Windows)
├── run-aura.sh              # Script cloud (Mac/Linux)
├── run-aura.bat             # Script cloud (Windows)
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
│   └── static/
│       └── index.html       # UI en HTML/JS con vis-network
└── neo4j-data/              # Solo para versión local
```

## 🚀 Inicio Rápido (Versión Cloud con Aura)

### Prerequisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado y corriendo
- Cuenta de [Neo4j Aura](https://neo4j.com/cloud/aura/) (tier gratuito disponible)

### Ejecución en un solo comando

#### Mac/Linux:
```bash
./run-aura.sh
```

#### Windows:
```cmd
run-aura.bat
```

La aplicación se abrirá automáticamente en http://localhost:8000

### Método alternativo (manual):

```bash
docker compose -f docker-compose.aura.yml up -d --build
```

**Servicios:**
- Neo4j Aura en la nube: `neo4j+s://257b501e.databases.neo4j.io`
- FastAPI en `http://localhost:8000/docs` (Swagger)

### Detener la aplicación

```bash
docker compose -f docker-compose.aura.yml down
```

## 🔧 Configuración de Neo4j Aura

Las credenciales de Aura están configuradas en `app/main.py` y pueden sobrescribirse con variables de entorno:

```python
NEO4J_URI=neo4j+s://257b501e.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=6euITjyHAIxRU3dtVQHZ5Y9kjKEUNfOMzLUsH3s9IGU
NEO4J_DATABASE=neo4j
```

## Sembrar datos (seed)

Una vez levantado, ejecutar el endpoint de seed para crear constraints e importar el CSV desde GitHub:

```
POST http://localhost:8000/seed
```

**Nota:** El CSV se carga automáticamente desde la URL de GitHub raw, no requiere archivos locales.

Si ya tienes datos cargados, puedes saltar este paso.

## UI (HTML/JS)

- Visita `http://localhost:8000/` para usar la UI básica en HTML/JS.
- Incluye botones para `seed`, healthcheck, top de productos y formularios simples para crear/actualizar/eliminar clientes.
- Swagger sigue disponible en `http://localhost:8000/docs`.
- Visualización de grafo con vis-network:
  - Selecciona tipo de centro (categoría/producto/cliente) y valor desde listas pobladas vía `/graph/options`.
  - Ajusta profundidad (niveles) y límite de relaciones.
  - Al cargar, se obtiene un subgrafo desde `/graph/sample` y se dibuja. Clic en un nodo muestra sus propiedades en el panel de detalle.

### Guía rápida de uso (UI)

1. Abre `http://localhost:8000/`.
2. Pulsa **seed** si es la primera vez (carga datos en Neo4J).
3. Verifica con **Healthcheck** y **Top productos**.
4. Sección CRUD rápida:
   - Crear cliente: completa campos y pulsa “Crear / MERGE”.
   - Actualizar edad: ingresa ID y nueva edad.
   - Eliminar cliente: ingresa ID y pulsa “Eliminar”.
5. Sección grafo:
   - Elige centro (categoría/producto/cliente); el selector de valores se rellena automáticamente.
   - Ajusta **Profundidad** (niveles de relaciones) y **Límite** (número de relaciones a traer).
   - Pulsa **Cargar grafo** y explora; al hacer clic en un nodo se muestran sus propiedades.

### Cómo está estructurada la app web

- `docker-compose.yml`: orquesta dos servicios:
  - **neo4j** (imagen `neo4j:5.15`) con volúmenes en `neo4j-data/` y el CSV montado en `/import`.
  - **app** (imagen construida desde `app/`) exponiendo FastAPI en 8000.
- `app/Dockerfile` + `requirements.txt`: definen la imagen de la API (Python 3.11 + FastAPI + neo4j-driver).
- `app/main.py`:
  - Configura el driver de Neo4J y expone todos los endpoints.
  - `/seed` crea constraints y carga nodos/relaciones con `LOAD CSV`.
  - CRUD: endpoints `CREATE/READ/UPDATE/DELETE` mapean las 5 sentencias de cada operación.
  - `/graph/options` devuelve valores disponibles para los selectores de la UI.
  - `/graph/sample` genera un subgrafo centrado en el nodo elegido con profundidad y límite configurables.
  - `/` sirve la UI estática.
- `app/static/index.html`:
  - HTML/JS simple con vis-network.
  - Formularios para llamadas CRUD básicas.
  - Selector de centro/valor/profundidad para el grafo; muestra propiedades al hacer clic en nodos.


## Endpoints principales (CRUD)

- CREATE:
  - `POST /customers`, `POST /categories`, `POST /products`, `POST /purchases`, `POST /products/with-category`
- READ:
  - `GET /read/customers-over-50`, `GET /read/top-products`, `GET /read/customers-by-category/{category}`, `GET /read/payment-summary`, `GET /read/premium-customers`
- UPDATE:
  - `PATCH /update/customer-age/{customerId}`, `PATCH /update/subscription-by-location`, `POST /update/product-rating/{name}`, `POST /update/increment-previous/{customerId}`, `PATCH /update/product/{name}`
- DELETE:
  - `DELETE /delete/customer/{customerId}`, `DELETE /delete/purchases-low-rating`, `DELETE /delete/products-no-purchases`, `DELETE /delete/product-category/{name}`, `DELETE /delete/inactive-customers`

Healthcheck: `GET /health`

### Endpoints de grafo

- `GET /graph/options?type=category|product|customer` — valores disponibles para el selector.
- `GET /graph/sample?centerType=...&centerValue=...&depth=...&limit=...` — devuelve nodos y relaciones para el subgrafo centrado en el nodo indicado.

## Operaciones que realiza la aplicación

- Crea y asegura clientes, categorías y productos; registra relaciones de compra.
- Consultas analíticas: clientes >50, top productos, clientes por categoría, resumen por método de pago, clientes premium.
- Actualizaciones: edad, suscripción por ubicación, rating promedio, incremento de compras previas, propiedades de producto.
- Eliminaciones: clientes (con relaciones), compras con rating bajo, productos sin compras, relaciones producto-categoría, clientes inactivos.

## Lenguaje y herramientas utilizadas

- Backend: FastAPI (Python 3.11), Uvicorn, neo4j-driver.
- Base de datos: Neo4J 5.15 (contenedor Docker).
- Contenedores: Docker Compose para orquestar app + Neo4J.
- Dataset: `data/shopping_behavior.csv` montado en `/import` y cargado con `LOAD CSV`.
- UI: HTML/JS simple con vis-network para visualizar subgrafos interactivos.

## Notas

- El contenedor Neo4J monta el CSV en `/import/shopping_behavior.csv`; el endpoint `/seed` usa `LOAD CSV` para crear nodos y relaciones.
- Los scripts Cypher originales siguen en `../neo4j/` y se montan en `/scripts` por si se quieren ejecutar manualmente.
