// ============================================
// IMPORT RELATIONSHIPS - Shopping Behaviour Dataset
// ============================================
// Este archivo crea las relaciones entre nodos ya existentes

// PREREQUISITO: Asegúrate de haber ejecutado primero:
// 1. constraints.cypher
// 2. import_nodes.cypher

// ============================================
// 1. CREAR RELACIONES PRODUCTO -> CATEGORÍA
// ============================================
LOAD CSV WITH HEADERS FROM 'file:///shopping_behavior.csv' AS row
WITH row,
     row.`Item Purchased` + '_' + row.Color + '_' + row.Size + '_' + row.Season AS productId
MATCH (p:Product {productId: productId})
MATCH (cat:Category {name: row.Category})
MERGE (p)-[:BELONGS_TO]->(cat);

// Verificar relaciones BELONGS_TO creadas
MATCH ()-[r:BELONGS_TO]->()
RETURN COUNT(r) AS totalBelongsToRelationships;

// ============================================
// 2. CREAR RELACIONES CLIENTE -> PRODUCTO (COMPRAS)
// ============================================
LOAD CSV WITH HEADERS FROM 'file:///shopping_behavior.csv' AS row
WITH row,
     row.`Item Purchased` + '_' + row.Color + '_' + row.Size + '_' + row.Season AS productId
MATCH (c:Customer {customerId: toInteger(row.`Customer ID`)})
MATCH (p:Product {productId: productId})
CREATE (c)-[:BOUGHT {
    amount: toFloat(row.`Purchase Amount (USD)`),
    discountApplied: row.`Discount Applied`,
    reviewRating: toFloat(row.`Review Rating`),
    paymentMethod: row.`Payment Method`,
    purchaseDate: datetime()  // Fecha de importación como referencia
}]->(p);

// Verificar relaciones BOUGHT creadas
MATCH ()-[r:BOUGHT]->()
RETURN COUNT(r) AS totalPurchases;

// ============================================
// RESUMEN DE RELACIONES IMPORTADAS
// ============================================
MATCH ()-[r]->()
RETURN type(r) AS relationshipType, COUNT(r) AS count
ORDER BY relationshipType;

// ============================================
// VERIFICACIÓN FINAL - Ver ejemplo del grafo
// ============================================
// Mostrar un ejemplo de cliente con sus compras y categorías
MATCH path = (c:Customer)-[:BOUGHT]->(p:Product)-[:BELONGS_TO]->(cat:Category)
RETURN path
LIMIT 5;
