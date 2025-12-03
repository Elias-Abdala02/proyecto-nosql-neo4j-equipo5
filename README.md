# Proyecto Extra – Aplicación Web (FastAPI + Neo4j Aura)

Aplicación web desplegada en la nube que expone las operaciones CRUD definidas en el proyecto principal. Esta versión utiliza **Neo4j Aura** (base de datos en la nube) y está desplegada en **Render**.

## 🌐 Acceso Web

**✨ Accede a la aplicación en funcionamiento:**

### [https://proyecto-nosql-neo4j-equipo5.onrender.com](https://proyecto-nosql-neo4j-equipo5.onrender.com)

No requiere instalación ni configuración. Los datos ya están precargados en Neo4j Aura.

## 📋 Acerca de esta versión

Esta rama (`proyecto-extra-web`) contiene la versión **100% en la nube** de la aplicación:

- **Backend**: FastAPI desplegado en Render
- **Base de datos**: Neo4j Aura (instancia gratuita en la nube)
- **Datos**: Precargados con 3,900 clientes y 3,099 productos
- **Sin Docker**: No requiere instalación local

### Diferencias con la versión Docker

Si buscas ejecutar la aplicación **localmente con Docker**, consulta la rama [`proyecto-extra-docker`](https://github.com/Elias-Abdala02/proyecto-nosql-neo4j-equipo5/tree/proyecto-extra-docker).

| Característica | proyecto-extra-web (esta rama) | proyecto-extra-docker |
|----------------|--------------------------------|----------------------|
| Despliegue | ☁️ Nube (Render + Neo4j Aura) | 🐳 Local (Docker) |
| Instalación | No requiere | Docker Desktop |
| Base de datos | Neo4j Aura (remota) | Neo4j container (local) |
| Datos | Precargados | Se cargan con `/seed` |
| Acceso | https://proyecto-nosql-neo4j-equipo5.onrender.com | http://localhost:8000 |

## Estructura del Proyecto

```
proyecto-extra/
├── docker-compose.aura.yml  # Configuración para despliegue en la nube
├── .env.example             # Variables de entorno para Neo4j Aura
├── run-aura.sh              # Script de ejecución para Mac/Linux (Aura)
├── run-aura.bat             # Script de ejecución para Windows (Aura)
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py              # FastAPI con conexión a Neo4j Aura
│   └── static/
│       └── index.html       # UI en HTML/JS con vis-network
└── neo4j-data/
    └── import/
        └── shopping_behavior.csv  # Dataset (3,900 clientes)
```

## 🚀 Acceso a la Aplicación Web

### Opción 1: Acceso directo (recomendado)

Simplemente accede a la URL desplegada:

**[https://proyecto-nosql-neo4j-equipo5.onrender.com](https://proyecto-nosql-neo4j-equipo5.onrender.com)**

La aplicación ya está funcionando con:
- ✅ Neo4j Aura configurado y conectado
- ✅ Datos precargados (3,900 clientes, 3,099 productos)
- ✅ API REST disponible
- ✅ Interfaz gráfica interactiva

### Opción 2: Ejecutar localmente con Neo4j Aura

Si deseas ejecutar la aplicación en tu máquina pero conectándote a Neo4j Aura:

#### Prerequisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado y corriendo
- Credenciales de Neo4j Aura (ya configuradas en `.env.example`)

#### Mac/Linux:
```bash
cd proyecto-extra
./run-aura.sh
```

#### Windows:
```cmd
cd proyecto-extra
run-aura.bat
```

La aplicación se abrirá en http://localhost:8000

### Opción 3: Despliegue manual con variables de entorno

```bash
cd proyecto-extra
cp .env.example .env
docker compose -f docker-compose.aura.yml up -d --build
```

## 🔌 Conexión a Neo4j Aura

La aplicación está configurada para conectarse a Neo4j Aura usando variables de entorno:

- **URI**: `neo4j+s://257b501e.databases.neo4j.io`
- **Database**: `neo4j`
- **Autenticación**: Credenciales almacenadas de forma segura

### Variables de entorno

```bash
NEO4J_URI=neo4j+s://257b501e.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<contraseña>
NEO4J_DATABASE=neo4j
```

## 💾 Datos y Seed

### ⚠️ Importante: Botón Seed Deshabilitado

En esta versión cloud, el botón **Seed** está **deshabilitado** porque:

- Los datos ya están **precargados en Neo4j Aura**
- La carga masiva de CSV desde URLs externas está optimizada para la nube
- No es necesario ejecutar el seed nuevamente

Si intentas usar el endpoint `/seed`, recibirás un mensaje informativo explicando que la base de datos ya contiene los datos necesarios.

### Dataset incluido

- **3,900 clientes** con información demográfica y comportamiento de compra
- **3,099 productos** únicos con categorías, temporadas y ratings
- **Relaciones de compra** con montos, descuentos y métodos de pago

## 🖥️ Uso de la Interfaz Web

### Acceso a la interfaz

- **Producción**: [https://proyecto-nosql-neo4j-equipo5.onrender.com](https://proyecto-nosql-neo4j-equipo5.onrender.com)
- **Local** (si ejecutas con run-aura.sh): `http://localhost:8000/`
- **Documentación API**: Agrega `/docs` a cualquiera de las URLs anteriores para Swagger

### Características de la UI

- ✅ **Healthcheck**: Verifica conectividad con Neo4j Aura
- ✅ **Top productos**: Productos más comprados
- ✅ **CRUD rápido**: Crear, actualizar y eliminar clientes
- ✅ **Visualización de grafo**: Interactúa con la red de datos usando vis-network

### Guía rápida de uso

1. Abre [https://proyecto-nosql-neo4j-equipo5.onrender.com](https://proyecto-nosql-neo4j-equipo5.onrender.com)
2. Verifica con **Healthcheck** (debe mostrar status: ok)
3. Consulta **Top productos** para ver los artículos más vendidos
4. **CRUD rápida**:
   - Crear cliente: completa campos y pulsa "Crear / MERGE"
   - Actualizar edad: ingresa ID y nueva edad
   - Eliminar cliente: ingresa ID y pulsa "Eliminar"
5. **Visualización de grafo**:
   - Elige centro (categoría/producto/cliente)
   - El selector de valores se rellena automáticamente
   - Ajusta **Profundidad** (niveles de relaciones) y **Límite** (número de nodos)
   - Pulsa **Cargar grafo** y explora
   - Clic en un nodo muestra sus propiedades

## 🏗️ Arquitectura de la Aplicación

### Componentes principales

- **FastAPI**: Framework web moderno para Python
  - Endpoints REST para operaciones CRUD
  - Documentación automática con Swagger
  - CORS habilitado para acceso desde navegadores
- **Neo4j Aura**: Base de datos de grafos en la nube
  - Conexión segura mediante `neo4j+s://` (SSL/TLS)
  - Driver oficial de Neo4j para Python (~5.28.0)
  - Base de datos: `neo4j`
- **vis-network**: Biblioteca JavaScript para visualización de grafos
  - Renderizado interactivo de nodos y relaciones
  - Navegación y zoom en el grafo
  - Panel de detalles de nodos

### Estructura del código

- `app/main.py`:
  - Configura el driver de Neo4j con autenticación por tupla `(username, password)`
  - `/seed` deshabilitado para Aura (datos precargados)
  - CRUD: endpoints `CREATE/READ/UPDATE/DELETE` mapean las 5 sentencias de cada operación
  - `/graph/options` devuelve valores disponibles para los selectores de la UI
  - `/graph/sample` genera un subgrafo centrado en el nodo elegido
  - `/` sirve la UI estática
- `app/static/index.html`:
  - HTML/JS con vis-network
  - Formularios para llamadas CRUD básicas
  - Selector de centro/valor/profundidad para el grafo
  - Usa `window.location.origin` para compatibilidad con despliegues

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
- **Base de datos**: Neo4j Aura (driver ~5.28.0)
- **Deployment**: Render (web service)
- **Dataset**: `shopping_behavior.csv` con 3,900 registros
- **Frontend**: HTML/JS con vis-network 9.1.2

## 📝 Notas importantes

- Esta versión está optimizada para despliegue en la nube con Neo4j Aura
- Los datos se cargan desde GitHub usando URLs públicas (https://)
- El botón seed está deshabilitado intencionalmente en producción
- La aplicación usa `window.location.origin` para funcionar tanto en local como en Render
- CORS está configurado para permitir acceso desde cualquier origen (producción)
