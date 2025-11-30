# Proyecto Extra – Aplicación Web (FastAPI + Neo4J)

Aplicación web simple que expone las operaciones CRUD definidas en el proyecto principal, corriendo en Docker junto a un contenedor Neo4J.

## Estructura

```
proyecto-extra/
├── docker-compose.yml
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
└── neo4j-data/       # datos/logs/import/plugins/conf del contenedor Neo4J
```

## Requisitos

- Docker + Docker Compose plugin.
- El dataset `data/shopping_behavior.csv` ya está en la raíz del repositorio.

## Cómo levantar

```bash
cd proyecto-extra
docker compose up -d
```

Servicios:
- Neo4J en `bolt://localhost:7687` (HTTP 7474), usuario `neo4j`, password `test1234`.
- FastAPI en `http://localhost:8000/docs` (Swagger).

## Sembrar datos (seed)

Una vez levantado, ejecutar el endpoint de seed para crear constraints e importar el CSV:

```
POST http://localhost:8000/seed
```

## UI mínima

- Visita `http://localhost:8000/` para usar la UI básica en HTML/JS.
- Incluye botones para `seed`, healthcheck, top de productos y formularios simples para crear/actualizar/eliminar clientes.
- Swagger sigue disponible en `http://localhost:8000/docs`.

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

## Notas

- El contenedor Neo4J monta el CSV en `/import/shopping_behavior.csv`; el endpoint `/seed` usa `LOAD CSV` para crear nodos y relaciones.
- Los scripts Cypher originales siguen en `../neo4j/` y se montan en `/scripts` por si se quieren ejecutar manualmente.
