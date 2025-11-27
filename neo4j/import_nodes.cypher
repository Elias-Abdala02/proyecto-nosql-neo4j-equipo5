// ============================================
// IMPORT NODES - Shopping Behaviour Dataset
// ============================================
// Este archivo carga los nodos desde el archivo CSV

// IMPORTANTE: Asegúrate de copiar shopping_behavior.csv al directorio 'import' de Neo4j
// Ubicación típica: <neo4j-home>/import/shopping_behavior.csv

// ============================================
// 1. CREAR NODOS DE CATEGORÍAS (únicas)
// ============================================
LOAD CSV WITH HEADERS FROM 'file:///shopping_behavior.csv' AS row
MERGE (:Category {name: row.Category});

// Verificar categorías creadas
MATCH (cat:Category)
RETURN cat.name, COUNT(*) AS count
ORDER BY cat.name;

// ============================================
// 2. CREAR NODOS DE CLIENTES
// ============================================
LOAD CSV WITH HEADERS FROM 'file:///shopping_behavior.csv' AS row
MERGE (c:Customer {customerId: toInteger(row.`Customer ID`)})
ON CREATE SET
    c.age = toInteger(row.Age),
    c.gender = row.Gender,
    c.location = row.Location,
    c.subscriptionStatus = row.`Subscription Status`,
    c.previousPurchases = toInteger(row.`Previous Purchases`),
    c.frequency = row.`Frequency of Purchases`;

// Verificar clientes creados
MATCH (c:Customer)
RETURN COUNT(c) AS totalCustomers;

// ============================================
// 3. CREAR NODOS DE PRODUCTOS
// ============================================
// Creamos productos únicos basados en nombre, color, talla y temporada
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

// Verificar productos creados
MATCH (p:Product)
RETURN COUNT(p) AS totalProducts;

// ============================================
// RESUMEN DE NODOS IMPORTADOS
// ============================================
MATCH (n)
RETURN labels(n)[0] AS nodeType, COUNT(n) AS count
ORDER BY nodeType;
