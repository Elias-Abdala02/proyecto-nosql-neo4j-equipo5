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
- Neo4J en `bolt://localhost:7687` (HTTP 7474), usuario `neo4j`, password `test123`.
- FastAPI en `http://localhost:8000/docs` (Swagger).

## Sembrar datos (seed)

Una vez levantado, ejecutar el endpoint de seed para crear constraints e importar el CSV:

```
POST http://localhost:8000/seed
```

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

## Notas

- El contenedor Neo4J monta el CSV en `/import/shopping_behavior.csv`; el endpoint `/seed` usa `LOAD CSV` para crear nodos y relaciones.
- Los scripts Cypher originales siguen en `../neo4j/` y se montan en `/scripts` por si se quieren ejecutar manualmente.
