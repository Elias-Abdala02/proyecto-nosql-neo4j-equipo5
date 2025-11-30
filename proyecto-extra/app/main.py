import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase, basic_auth
from pydantic import BaseModel, Field


NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test123")


def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD))


driver = get_driver()

app = FastAPI(
    title="Proyecto Extra - Neo4J CRUD",
    description="API FastAPI que expone las operaciones CRUD definidas para el proyecto Neo4J.",
    version="1.0.0",
)


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
    with driver.session() as session:
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

        # Importar nodos
        run_query(
            """
            LOAD CSV WITH HEADERS FROM 'file:///shopping_behavior.csv' AS row
            MERGE (:Category {name: row.Category});
            """
        )
        run_query(
            """
            LOAD CSV WITH HEADERS FROM 'file:///shopping_behavior.csv' AS row
            MERGE (c:Customer {customerId: toInteger(row.`Customer ID`)})
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
            """
            LOAD CSV WITH HEADERS FROM 'file:///shopping_behavior.csv' AS row
            WITH row,
                 row.`Item Purchased` + '_' + row.Color + '_' + row.Size + '_' + row.Season AS productId
            MERGE (p:Product {productId: productId})
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
            """
            LOAD CSV WITH HEADERS FROM 'file:///shopping_behavior.csv' AS row
            WITH row,
                 row.`Item Purchased` + '_' + row.Color + '_' + row.Size + '_' + row.Season AS productId
            MATCH (p:Product {productId: productId})
            MATCH (cat:Category {name: row.Category})
            MERGE (p)-[:BELONGS_TO]->(cat);
            """
        )
        run_query(
            """
            LOAD CSV WITH HEADERS FROM 'file:///shopping_behavior.csv' AS row
            WITH row,
                 row.`Item Purchased` + '_' + row.Color + '_' + row.Size + '_' + row.Season AS productId
            MATCH (c:Customer {customerId: toInteger(row.`Customer ID`)})
            MATCH (p:Product {productId: productId})
            MERGE (c)-[:BOUGHT {
                amount: toFloat(row.`Purchase Amount (USD)`),
                discountApplied: row.`Discount Applied`,
                reviewRating: toFloat(row.`Review Rating`),
                paymentMethod: row.`Payment Method`,
                purchaseDate: datetime()
            }]->(p);
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
def update_customer_age(customerId: int, age: int = Field(..., gt=0)):
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
        run_query("RETURN 1 AS ok")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
