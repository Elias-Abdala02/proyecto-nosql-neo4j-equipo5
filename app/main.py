import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from neo4j import GraphDatabase
from pydantic import BaseModel, Field


# Variables de entorno para Neo4j (compatible con Aura y local)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", os.getenv("NEO4J_USER", "neo4j"))
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test1234")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def get_driver():
    """Crear driver de Neo4j con autenticación"""
    return GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )


# Inicializar driver y verificar conectividad
driver = get_driver()
try:
    driver.verify_connectivity()
    print(f"✅ Conectado a Neo4j: {NEO4J_URI}")
except Exception as e:
    print(f"⚠️  Error conectando a Neo4j: {e}")
    print(f"   URI: {NEO4J_URI}")
    print(f"   Database: {NEO4J_DATABASE}")

app = FastAPI(
    title="Proyecto Extra - Neo4J CRUD",
    description="API FastAPI que expone las operaciones CRUD definidas para el proyecto Neo4J.",
    version="1.0.0",
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).resolve().parent / "static"

# ---------- UI mínima ----------
@app.get("/", include_in_schema=False)
def home():
    index_path = static_dir / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="UI no encontrada")
    return FileResponse(index_path)


# ---------- Modelos de entrada ----------
class CustomerCreate(BaseModel):
    customerId: int
    age: int
    gender: str
    location: str
    subscriptionStatus: str
    previousPurchases: int
    frequency: str


class CategoryCreate(BaseModel):
    name: str


class ProductCreate(BaseModel):
    productId: str
    name: str
    size: str
    color: str
    season: str
    avgReviewRating: Optional[float] = None


class PurchaseCreate(BaseModel):
    customerId: int
    productId: str
    amount: float
    discountApplied: str
    reviewRating: float
    paymentMethod: str


class ProductUpdate(BaseModel):
    color: Optional[str] = None
    avgReviewRating: Optional[float] = None
    season: Optional[str] = None


# ---------- Utilidades ----------
def run_query(query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Ejecutar query en Neo4j usando la base de datos configurada"""
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run(query, params or {})
        return [record.data() for record in result]


# ---------- Seed / carga inicial ----------
@app.post("/seed", summary="Crear constraints e importar dataset si no existe")
def seed_database():
    try:
        # Constraints
        constraints = [
            """
            CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
            FOR (c:Customer) REQUIRE c.customerId IS UNIQUE
            """,
            """
            CREATE CONSTRAINT category_name_unique IF NOT EXISTS
            FOR (cat:Category) REQUIRE cat.name IS UNIQUE
            """,
            """
            CREATE CONSTRAINT product_composite_unique IF NOT EXISTS
            FOR (p:Product) REQUIRE p.productId IS UNIQUE
            """,
        ]
        for c in constraints:
            run_query(c)

        # Importar nodos desde GitHub (funciona en local y cloud)
        csv_url = 'https://raw.githubusercontent.com/Elias-Abdala02/proyecto-nosql-neo4j-equipo5/proyecto-extra-solo/neo4j-data/import/shopping_behavior.csv'
        
        run_query(
            f"""
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MERGE (:Category {{name: row.Category}});
            """
        )
        run_query(
            f"""
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MERGE (c:Customer {{customerId: toInteger(row.`Customer ID`)}})
            ON CREATE SET
                c.age = toInteger(row.Age),
                c.gender = row.Gender,
                c.location = row.Location,
                c.subscriptionStatus = row.`Subscription Status`,
                c.previousPurchases = toInteger(row.`Previous Purchases`),
                c.frequency = row.`Frequency of Purchases`;
            """
        )
        run_query(
            f"""
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            WITH row,
                 row.`Item Purchased` + '_' + row.Color + '_' + row.Size + '_' + row.Season AS productId
            MERGE (p:Product {{productId: productId}})
            ON CREATE SET
                p.name = row.`Item Purchased`,
                p.size = row.Size,
                p.color = row.Color,
                p.season = row.Season,
                p.avgReviewRating = toFloat(row.`Review Rating`);
            """
        )
        # Importar relaciones
        run_query(
            f"""
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            WITH row,
                 row.`Item Purchased` + '_' + row.Color + '_' + row.Size + '_' + row.Season AS productId
            MATCH (p:Product {{productId: productId}})
            MATCH (cat:Category {{name: row.Category}})
            MERGE (p)-[:BELONGS_TO]->(cat);
            """
        )
        run_query(
            f"""
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            WITH row,
                 row.`Item Purchased` + '_' + row.Color + '_' + row.Size + '_' + row.Season AS productId
            MATCH (c:Customer {{customerId: toInteger(row.`Customer ID`)}})
            MATCH (p:Product {{productId: productId}})
            MERGE (c)-[:BOUGHT {{
                amount: toFloat(row.`Purchase Amount (USD)`),
                discountApplied: row.`Discount Applied`,
                reviewRating: toFloat(row.`Review Rating`),
                paymentMethod: row.`Payment Method`,
                purchaseDate: datetime()
            }}]->(p);
            """
        )

        counts = run_query(
            """
            MATCH (n)
            RETURN labels(n)[0] AS tipo, COUNT(n) AS total
            """
        )
        rels = run_query(
            """
            MATCH ()-[r]->()
            RETURN type(r) AS tipo, COUNT(r) AS total
            """
        )
        return {"message": "Carga completada", "nodos": counts, "relaciones": rels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- CREATE ----------
@app.post("/customers", summary="C1: Crear o asegurar un cliente")
def create_customer(payload: CustomerCreate):
    query = """
    MERGE (c:Customer {customerId: $customerId})
    SET c.age = $age,
        c.gender = $gender,
        c.location = $location,
        c.subscriptionStatus = $subscriptionStatus,
        c.previousPurchases = $previousPurchases,
        c.frequency = $frequency
    RETURN c
    """
    result = run_query(query, payload.model_dump())
    return {"customer": result}


@app.post("/categories", summary="C2: Crear o asegurar una categoría")
def create_category(payload: CategoryCreate):
    query = "MERGE (cat:Category {name: $name}) RETURN cat"
    result = run_query(query, {"name": payload.name})
    return {"category": result}


@app.post("/products", summary="C3: Crear o asegurar un producto")
def create_product(payload: ProductCreate):
    query = """
    MERGE (p:Product {productId: $productId})
    SET p.name = $name,
        p.size = $size,
        p.color = $color,
        p.season = $season,
        p.avgReviewRating = $avgReviewRating
    RETURN p
    """
    result = run_query(query, payload.model_dump())
    return {"product": result}


@app.post("/purchases", summary="C4: Crear una relación de compra")
def create_purchase(payload: PurchaseCreate):
    query = """
    MATCH (c:Customer {customerId: $customerId})
    MATCH (p:Product {productId: $productId})
    MERGE (c)-[b:BOUGHT {
        amount: $amount,
        discountApplied: $discountApplied,
        reviewRating: $reviewRating,
        paymentMethod: $paymentMethod
    }]->(p)
    RETURN c.customerId AS customerId, p.productId AS productId, b
    """
    result = run_query(query, payload.model_dump())
    if not result:
        raise HTTPException(status_code=404, detail="Cliente o producto no encontrado")
    return result[0]


@app.post("/products/with-category", summary="C5: Crear producto y relacionarlo con categoría")
def create_product_with_category(payload: ProductCreate, category: CategoryCreate):
    params = {**payload.model_dump(), "category": category.name}
    query = """
    MERGE (cat:Category {name: $category})
    MERGE (p:Product {productId: $productId})
    SET p.name = $name,
        p.size = $size,
        p.color = $color,
        p.season = $season,
        p.avgReviewRating = $avgReviewRating
    MERGE (p)-[:BELONGS_TO]->(cat)
    RETURN p, cat
    """
    result = run_query(query, params)
    return {"product": result}


# ---------- READ ----------
@app.get("/read/customers-over-50", summary="R1: Clientes mayores de 50")
def read_customers_over_50():
    query = """
    MATCH (c:Customer)
    WHERE c.age > 50
    RETURN c.customerId AS customerId, c.age AS age, c.gender AS gender, c.location AS location
    ORDER BY age DESC
    """
    return run_query(query)


@app.get("/read/top-products", summary="R2: Productos más comprados")
def read_top_products(limit: int = 10):
    query = """
    MATCH (c:Customer)-[b:BOUGHT]->(p:Product)
    RETURN p.name AS name, COUNT(b) AS totalPurchases, AVG(b.amount) AS avgPrice
    ORDER BY totalPurchases DESC
    LIMIT $limit
    """
    return run_query(query, {"limit": limit})


@app.get("/read/customers-by-category/{category}", summary="R3: Clientes por categoría")
def read_customers_by_category(category: str):
    query = """
    MATCH (c:Customer)-[:BOUGHT]->(p:Product)-[:BELONGS_TO]->(cat:Category {name: $category})
    RETURN DISTINCT c.customerId AS customerId, c.age AS age, c.gender AS gender, c.location AS location,
           COUNT(p) AS productsBought
    ORDER BY productsBought DESC
    """
    return run_query(query, {"category": category})


@app.get("/read/payment-summary", summary="R4: Promedio de compra por método de pago")
def read_payment_summary():
    query = """
    MATCH (c:Customer)-[b:BOUGHT]->(p:Product)
    RETURN b.paymentMethod AS paymentMethod,
           COUNT(b) AS totalTransactions,
           AVG(b.amount) AS avgAmount,
           SUM(b.amount) AS totalAmount
    ORDER BY totalAmount DESC
    """
    return run_query(query)


@app.get("/read/premium-customers", summary="R5: Clientes premium")
def read_premium_customers():
    query = """
    MATCH (c:Customer)
    WHERE c.subscriptionStatus = 'Yes' AND c.previousPurchases > 20
    RETURN c.customerId AS customerId, c.age AS age, c.location AS location,
           c.previousPurchases AS previousPurchases, c.frequency AS frequency
    ORDER BY previousPurchases DESC
    """
    return run_query(query)


# ---------- UPDATE ----------
@app.patch("/update/customer-age/{customerId}", summary="U1: Actualizar edad de un cliente")
def update_customer_age(customerId: int, age: int = Query(..., gt=0, description="Nueva edad")):
    query = """
    MATCH (c:Customer {customerId: $customerId})
    SET c.age = $age
    RETURN c.customerId AS customerId, c.age AS age
    """
    result = run_query(query, {"customerId": customerId, "age": age})
    if not result:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return result[0]


@app.patch("/update/subscription-by-location", summary="U2: Cambiar suscripción por ubicación")
def update_subscription_by_location(location: str, status: str = "No"):
    query = """
    MATCH (c:Customer)
    WHERE c.location = $location
    SET c.subscriptionStatus = $status
    RETURN c.customerId AS customerId, c.location AS location, c.subscriptionStatus AS subscriptionStatus
    """
    return run_query(query, {"location": location, "status": status})


@app.post("/update/product-rating/{name}", summary="U3: Recalcular rating promedio de un producto")
def update_product_rating(name: str):
    query = """
    MATCH (p:Product {name: $name})<-[b:BOUGHT]-()
    WITH p, AVG(b.reviewRating) AS newAvgRating
    SET p.avgReviewRating = newAvgRating
    RETURN p.name AS name, p.avgReviewRating AS avgReviewRating
    """
    result = run_query(query, {"name": name})
    if not result:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return result[0]


@app.post("/update/increment-previous/{customerId}", summary="U4: Incrementar compras previas")
def increment_previous_purchases(customerId: int):
    query = """
    MATCH (c:Customer {customerId: $customerId})
    SET c.previousPurchases = c.previousPurchases + 1
    RETURN c.customerId AS customerId, c.previousPurchases AS previousPurchases
    """
    result = run_query(query, {"customerId": customerId})
    if not result:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return result[0]


@app.patch("/update/product/{name}", summary="U5: Actualizar propiedades de un producto")
def update_product(name: str, payload: ProductUpdate):
    sets = []
    params: Dict[str, Any] = {"name": name}
    for field, value in payload.model_dump(exclude_none=True).items():
        sets.append(f"p.{field} = ${field}")
        params[field] = value
    if not sets:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    set_clause = ", ".join(sets)
    query = f"""
    MATCH (p:Product {{name: $name}})
    SET {set_clause}
    RETURN p
    """
    result = run_query(query, params)
    if not result:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return result[0]


# ---------- DELETE ----------
@app.delete("/delete/customer/{customerId}", summary="D1: Eliminar un cliente y sus relaciones")
def delete_customer(customerId: int):
    query = """
    MATCH (c:Customer {customerId: $customerId})
    DETACH DELETE c
    """
    run_query(query, {"customerId": customerId})
    return {"deletedCustomerId": customerId}


@app.delete("/delete/purchases-low-rating", summary="D2: Eliminar compras con calificación baja")
def delete_low_rating_purchases(threshold: float = 2.0):
    query = """
    MATCH ()-[b:BOUGHT]->()
    WHERE b.reviewRating < $threshold
    DELETE b
    """
    run_query(query, {"threshold": threshold})
    return {"deletedBelow": threshold}


@app.delete("/delete/products-no-purchases", summary="D3: Eliminar productos nunca comprados")
def delete_products_no_purchases():
    query = """
    MATCH (p:Product)
    WHERE NOT (p)<-[:BOUGHT]-()
    DELETE p
    """
    run_query(query)
    return {"status": "ok"}


@app.delete("/delete/product-category/{name}", summary="D4: Eliminar relación producto-categoría")
def delete_product_category(name: str):
    query = """
    MATCH (p:Product {name: $name})-[r:BELONGS_TO]->()
    DELETE r
    """
    run_query(query, {"name": name})
    return {"product": name, "relationshipDeleted": "BELONGS_TO"}


@app.delete("/delete/inactive-customers", summary="D5: Eliminar clientes inactivos")
def delete_inactive_customers():
    query = """
    MATCH (c:Customer)
    WHERE c.subscriptionStatus = 'No' AND c.previousPurchases = 0
    DETACH DELETE c
    """
    run_query(query)
    return {"status": "ok"}


@app.get("/health", summary="Healthcheck")
def health():
    try:
        driver.verify_connectivity()
        run_query("RETURN 1 AS ok")
        return {
            "status": "ok",
            "neo4j_uri": NEO4J_URI.replace(NEO4J_PASSWORD, "***") if NEO4J_PASSWORD in NEO4J_URI else NEO4J_URI,
            "database": NEO4J_DATABASE
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Graph options ----------
@app.get("/graph/options", summary="Listado de valores disponibles por tipo")
def graph_options(
    type: str = Query("category", pattern="^(category|product|customer)$"),
    limit: int = Query(100, gt=1, le=300),
):
    if type == "category":
        q = "MATCH (c:Category) RETURN c.name AS value ORDER BY c.name LIMIT $limit"
    elif type == "product":
        q = "MATCH (p:Product) RETURN DISTINCT p.name AS value ORDER BY value LIMIT $limit"
    else:
        q = "MATCH (c:Customer) RETURN c.customerId AS value ORDER BY value LIMIT $limit"
    results = run_query(q, {"limit": limit})
    return {"type": type, "values": [r["value"] for r in results]}


# ---------- GRAPH SAMPLE ----------
@app.get("/graph/sample", summary="Subgrafo centrado en un nodo específico")
def graph_sample(
    centerType: str = Query("category", pattern="^(category|product|customer)$"),
    centerValue: str = Query("Clothing", description="Nombre o ID del nodo centro"),
    depth: int = Query(2, gt=0, le=4),
    limit: int = Query(50, gt=1, le=400),
):
    """
    Obtiene un subgrafo centrado en un nodo específico.
    Muestra el grafo tal como Neo4j lo devuelve, sin filtros adicionales.
    """
    # Construir query según el tipo de nodo central
    if centerType == "category":
        center_match = "MATCH (center:Category {name: $centerValue})"
    elif centerType == "product":
        center_match = "MATCH (center:Product {name: $centerValue})"
    else:  # customer
        center_match = "MATCH (center:Customer {customerId: toInteger($centerValue)})"
    
    # Query simple: obtener nodos vecinos y sus relaciones
    query = f"""
    {center_match}
    CALL {{
      WITH center
      MATCH path = (center)-[*1..{depth}]-(n)
      WITH DISTINCT n
      LIMIT $limit
      RETURN n
    }}
    WITH center, collect(n) AS neighbors
    WITH [center] + neighbors AS allNodes
    UNWIND allNodes AS fromNode
    MATCH (fromNode)-[r]-(toNode)
    WHERE toNode IN allNodes
    RETURN fromNode, r, toNode
    """
    
    with driver.session() as session:
        result = session.run(query, {"centerValue": centerValue, "limit": limit})
        
        nodes = {}
        links = {}  # Cambiar a dict para evitar duplicados
        found_data = False
        
        for record in result:
            found_data = True
            fromNode = record["fromNode"]
            toNode = record["toNode"]
            rel = record["r"]
            
            # Agregar nodos
            for node in [fromNode, toNode]:
                if node.id not in nodes:
                    label = list(node.labels)[0] if node.labels else "Node"
                    title = node.get("name") or str(node.get("customerId")) or label
                    nodes[node.id] = {
                        "id": str(node.id),
                        "group": label,
                        "label": title,
                        "properties": dict(node),
                    }
            
            # Agregar relación evitando duplicados
            rel_id = f"{rel.type}-{rel.id}"
            if rel_id not in links:
                links[rel_id] = {
                    "id": rel_id,
                    "from": str(fromNode.id),
                    "to": str(toNode.id),
                    "label": rel.type,
                }
        
        if not found_data:
            raise HTTPException(status_code=404, detail="Nodo centro no encontrado o sin resultados.")
        
        return {"nodes": list(nodes.values()), "links": list(links.values())}


@app.get("/graph/full", summary="Obtener el grafo completo")
def graph_full(limit: int = Query(500, gt=1, le=10000)):
    """
    Obtiene todo el grafo sin filtros.
    Útil para visualizar la estructura completa de datos.
    """
    query = """
    MATCH (n)
    WITH n
    LIMIT $limit
    MATCH (n)-[r]-(m)
    RETURN n, r, m
    """
    
    with driver.session() as session:
        result = session.run(query, {"limit": limit})
        
        nodes = {}
        links = {}  # Cambiar a dict para evitar duplicados
        
        for record in result:
            for node in [record["n"], record["m"]]:
                if node.id not in nodes:
                    label = list(node.labels)[0] if node.labels else "Node"
                    title = node.get("name") or str(node.get("customerId")) or label
                    nodes[node.id] = {
                        "id": str(node.id),
                        "group": label,
                        "label": title,
                        "properties": dict(node),
                    }
            
            rel = record["r"]
            rel_id = f"{rel.type}-{rel.id}"
            if rel_id not in links:
                links[rel_id] = {
                    "id": rel_id,
                    "from": str(record["n"].id),
                    "to": str(record["m"].id),
                    "label": rel.type,
                }
        
        return {"nodes": list(nodes.values()), "links": list(links.values())}

