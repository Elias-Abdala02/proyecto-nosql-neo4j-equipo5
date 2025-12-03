# Proyecto Extra – Aplicación Web (FastAPI + Neo4j Docker)

Aplicación web que expone las operaciones CRUD definidas en el proyecto principal, corriendo **completamente en local con Docker**. Esta versión incluye tanto el contenedor de FastAPI como el de Neo4j.

## 🐳 Acerca de esta versión

Esta rama (`proyecto-extra-docker`) contiene la versión **100% local con Docker** de la aplicación:

- **Backend**: FastAPI en contenedor Docker
- **Base de datos**: Neo4j 5.15 en contenedor Docker
- **Datos**: Se cargan con el endpoint `/seed` desde archivo CSV local
- **Requisito**: Docker Desktop instalado

### Diferencias con la versión Web

Si buscas acceder a la aplicación **desplegada en la nube**, consulta la rama [`proyecto-extra-web`](https://github.com/Elias-Abdala02/proyecto-nosql-neo4j-equipo5/tree/proyecto-extra-web).

**O accede directamente:** [https://proyecto-nosql-neo4j-equipo5.onrender.com](https://proyecto-nosql-neo4j-equipo5.onrender.com)

| Característica | proyecto-extra-docker (esta rama) | proyecto-extra-web |
|----------------|-----------------------------------|--------------------|
| Despliegue | 🐳 Local (Docker) | ☁️ Nube (Render + Neo4j Aura) |
| Instalación | Docker Desktop requerido | No requiere instalación |
| Base de datos | Neo4j container (local) | Neo4j Aura (remota) |
| Datos | Se cargan con `/seed` | Precargados |
| Acceso | http://localhost:8000 | https://proyecto-nosql-neo4j-equipo5.onrender.com |

## Estructura del Proyecto

```
proyecto-extra/
├── docker-compose.yml    # Orquesta Neo4j + FastAPI
├── run.sh               # Script de ejecución para Mac/Linux
├── run.bat              # Script de ejecución para Windows
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py          # FastAPI con conexión a Neo4j local
│   └── static/
│       └── index.html   # UI en HTML/JS con vis-network
└── neo4j-data/          # Datos persistentes del contenedor Neo4j
    ├── data/            # Base de datos
    ├── logs/            # Logs del servidor
    ├── import/
    │   └── shopping_behavior.csv  # Dataset (3,900 clientes)
    ├── plugins/
    └── conf/
```

## 🚀 Inicio Rápido

### Prerequisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado y corriendo

### Ejecución en un solo comando

#### Mac/Linux:
```bash
cd proyecto-extra
./run.sh
```

#### Windows:
```cmd
cd proyecto-extra
run.bat
```

La aplicación se abrirá automáticamente en http://localhost:8000

### Método alternativo (manual):

```bash
cd proyecto-extra
docker compose up -d --build
```

**Servicios desplegados:**
- Neo4j en `bolt://localhost:7687` (HTTP 7474)
  - Usuario: `neo4j`
  - Password: `test1234`
- FastAPI en `http://localhost:8000/docs` (Swagger)

### Detener la aplicación

```bash
docker compose down
```

Para eliminar también los volúmenes de datos:
```bash
docker compose down -v
```

## 💾 Sembrar datos (seed)

Una vez levantada la aplicación, **debes ejecutar el endpoint de seed** para crear constraints e importar el CSV:

```
POST http://localhost:8000/seed
```

Esto creará:
- ✅ Constraints de unicidad para Customer, Category y Product
- ✅ 3,900 clientes con información demográfica
- ✅ 3,099 productos únicos
- ✅ Relaciones de compra con montos, ratings y métodos de pago

**Puedes hacerlo desde:**
- La UI web: http://localhost:8000/ → botón "Seed Database"
- Swagger: http://localhost:8000/docs → POST /seed → Try it out → Execute
- cURL: `curl -X POST http://localhost:8000/seed`

Si ya tienes datos cargados, puedes saltar este paso.

## 🖥️ Uso de la Interfaz Web

### Acceso a la interfaz

- **Aplicación principal**: `http://localhost:8000/`
- **Documentación API (Swagger)**: `http://localhost:8000/docs`
- **Neo4j Browser**: `http://localhost:7474/` (usuario: `neo4j`, password: `test1234`)

### Características de la UI

- ✅ **Seed Database**: Carga datos desde el CSV local
- ✅ **Healthcheck**: Verifica conectividad con Neo4j
- ✅ **Top productos**: Productos más comprados
- ✅ **CRUD rápido**: Crear, actualizar y eliminar clientes
- ✅ **Visualización de grafo**: Interactúa con la red de datos usando vis-network

### Guía rápida de uso

1. Abre `http://localhost:8000/`
2. Pulsa **Seed Database** (solo la primera vez para cargar datos)
3. Verifica con **Healthcheck** (debe mostrar status: ok)
4. Consulta **Top productos** para ver los artículos más vendidos
5. **CRUD rápida**:
   - Crear cliente: completa campos y pulsa "Crear / MERGE"
   - Actualizar edad: ingresa ID y nueva edad
   - Eliminar cliente: ingresa ID y pulsa "Eliminar"
6. **Visualización de grafo**:
   - Elige centro (categoría/producto/cliente)
   - El selector de valores se rellena automáticamente
   - Ajusta **Profundidad** (niveles de relaciones) y **Límite** (número de nodos)
   - Pulsa **Cargar grafo** y explora
   - Clic en un nodo muestra sus propiedades

## 🏗️ Arquitectura de la Aplicación

### Componentes principales

- **Docker Compose**: Orquesta dos servicios
  - **neo4j**: Imagen `neo4j:5.15` con volúmenes persistentes
  - **app**: Imagen construida desde `app/` exponiendo FastAPI en puerto 8000
- **FastAPI**: Framework web moderno para Python
  - Endpoints REST para operaciones CRUD
  - Documentación automática con Swagger
  - CORS habilitado para desarrollo
- **Neo4j**: Base de datos de grafos
  - Conexión local mediante `bolt://neo4j:7687`
  - Driver oficial de Neo4j para Python
  - Datos persistentes en `neo4j-data/`
- **vis-network**: Biblioteca JavaScript para visualización de grafos
  - Renderizado interactivo de nodos y relaciones
  - Navegación y zoom en el grafo
  - Panel de detalles de nodos

### Estructura del código

- `docker-compose.yml`: Orquesta los servicios
  - Monta `neo4j-data/` para persistencia
  - Monta `neo4j-data/import/` en `/import` para el CSV
- `app/Dockerfile` + `requirements.txt`: Define la imagen de FastAPI
  - Python 3.11
  - FastAPI + Uvicorn + neo4j-driver
- `app/main.py`:
  - Configura el driver de Neo4j para conexión local
  - `/seed` crea constraints y carga nodos/relaciones con `LOAD CSV`
  - CRUD: endpoints `CREATE/READ/UPDATE/DELETE` mapean las 5 sentencias de cada operación
  - `/graph/options` devuelve valores disponibles para los selectores de la UI
  - `/graph/sample` genera un subgrafo centrado en el nodo elegido
  - `/` sirve la UI estática
- `app/static/index.html`:
  - HTML/JS con vis-network
  - Formularios para llamadas CRUD básicas
  - Selector de centro/valor/profundidad para el grafo

## Endpoints principales (CRUD)

- **CREATE**:
  - `POST /customers`, `POST /categories`, `POST /products`, `POST /purchases`, `POST /products/with-category`
- **READ**:
  - `GET /read/customers-over-50`, `GET /read/top-products`, `GET /read/customers-by-category/{category}`, `GET /read/payment-summary`, `GET /read/premium-customers`
- **UPDATE**:
  - `PATCH /update/customer-age/{customerId}`, `PATCH /update/subscription-by-location`, `POST /update/product-rating/{name}`, `POST /update/increment-previous/{customerId}`, `PATCH /update/product/{name}`
- **DELETE**:
  - `DELETE /delete/customer/{customerId}`, `DELETE /delete/purchases-low-rating`, `DELETE /delete/products-no-purchases`, `DELETE /delete/product-category/{name}`, `DELETE /delete/inactive-customers`

**Healthcheck**: `GET /health`

### Endpoints de grafo

- `GET /graph/options?type=category|product|customer` — valores disponibles para el selector
- `GET /graph/sample?centerType=...&centerValue=...&depth=...&limit=...` — devuelve nodos y relaciones para el subgrafo
- `GET /graph/full?limit=...` — obtiene el grafo completo

## Operaciones que realiza la aplicación

- Crea y asegura clientes, categorías y productos; registra relaciones de compra
- Consultas analíticas: clientes >50, top productos, clientes por categoría, resumen por método de pago, clientes premium
- Actualizaciones: edad, suscripción por ubicación, rating promedio, incremento de compras previas, propiedades de producto
- Eliminaciones: clientes (con relaciones), compras con rating bajo, productos sin compras, relaciones producto-categoría, clientes inactivos

## 🛠️ Tecnologías utilizadas

- **Backend**: FastAPI 0.115.0, Uvicorn 0.30.6
- **Base de datos**: Neo4j 5.15 (contenedor Docker)
- **Contenedores**: Docker Compose para orquestar app + Neo4j
- **Dataset**: `shopping_behavior.csv` con 3,900 registros montado en `/import`
- **Frontend**: HTML/JS con vis-network 9.1.2

## 📝 Notas importantes

- Los datos se persisten en `neo4j-data/data/` para sobrevivir reinicios de contenedores
- El CSV se monta en `/import/shopping_behavior.csv` dentro del contenedor Neo4j
- El endpoint `/seed` usa `LOAD CSV` con ruta `file:///shopping_behavior.csv`
- Los logs de Neo4j están en `neo4j-data/logs/`
- Scripts Cypher originales están en `../neo4j/` y se montan en `/scripts` (opcional)

## 🔧 Troubleshooting

### El contenedor Neo4j no inicia
- Verifica que Docker Desktop esté corriendo
- Asegúrate de que los puertos 7474 y 7687 no estén en uso
- Revisa logs: `docker compose logs neo4j`

### Error al cargar datos con /seed
- Verifica que el archivo `neo4j-data/import/shopping_behavior.csv` exista
- Revisa que el CSV tenga 3,901 líneas (header + 3,900 datos)
- Ejecuta seed solo una vez; si hay error, reinicia contenedores

### No puedo acceder a la UI
- Verifica que ambos contenedores estén corriendo: `docker compose ps`
- Asegúrate de que el puerto 8000 no esté en uso
- Revisa logs de la app: `docker compose logs app`
