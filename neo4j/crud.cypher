// ============================================
// OPERACIONES CRUD - Shopping Behaviour Dataset
// ============================================
// Proyecto Neo4J - Análisis de Comportamiento de Compras
// Este archivo contiene 5 ejemplos de cada operación CRUD

// ============================================
// CREATE - Crear nuevos nodos y relaciones (5 ejemplos)
// ============================================

// C1. Crear (o asegurar) un nuevo cliente
MERGE (c:Customer {customerId: 9999})
SET c.age = 28,
    c.gender = 'Female',
    c.location = 'California',
    c.subscriptionStatus = 'Yes',
    c.previousPurchases = 5,
    c.frequency = 'Monthly';

// C2. Crear (o asegurar) una nueva categoría de producto
MERGE (:Category {name: 'Electronics'});

// C3. Crear (o asegurar) un nuevo producto
MERGE (p:Product {productId: 'Smart Watch_Black_M_All Season'})
SET p.name = 'Smart Watch',
    p.size = 'M',
    p.color = 'Black',
    p.season = 'All Season',
    p.avgReviewRating = 4.5;

// C4. Crear una relación de compra entre un cliente existente y un producto
MATCH (c:Customer {customerId: 1})
MATCH (p:Product {name: 'Blouse'})
MERGE (c)-[b:BOUGHT {
    amount: 53.0,
    discountApplied: 'Yes',
    reviewRating: 3.1,
    paymentMethod: 'Venmo'
}]->(p)
RETURN c.customerId, p.name, b;

// C5. Crear un producto y su relación con una categoría en una sola operación
MERGE (cat:Category {name: 'Footwear'})
MERGE (p:Product {productId: 'Running Shoes_Blue_L_Summer'})
SET p.name = 'Running Shoes',
    p.size = 'L',
    p.color = 'Blue',
    p.season = 'Summer',
    p.avgReviewRating = 4.2
MERGE (p)-[:BELONGS_TO]->(cat);

// ============================================
// READ - Consultar datos (5 ejemplos)
// ============================================

// R1. Obtener todos los clientes mayores de 50 años
MATCH (c:Customer)
WHERE c.age > 50
RETURN c.customerId, c.age, c.gender, c.location
ORDER BY c.age DESC;

// R2. Encontrar los 10 productos más comprados
MATCH (c:Customer)-[b:BOUGHT]->(p:Product)
RETURN p.name, COUNT(b) AS totalPurchases, AVG(b.amount) AS avgPrice
ORDER BY totalPurchases DESC
LIMIT 10;

// R3. Buscar clientes que compraron en una categoría específica
MATCH (c:Customer)-[:BOUGHT]->(p:Product)-[:BELONGS_TO]->(cat:Category {name: 'Clothing'})
WITH c, COUNT(DISTINCT p) AS productsBought
RETURN c.customerId AS customerId,
       c.age       AS age,
       c.gender    AS gender,
       c.location  AS location,
       productsBought
ORDER BY productsBought DESC;

// R4. Obtener el promedio de compra por método de pago
MATCH (c:Customer)-[b:BOUGHT]->(p:Product)
RETURN b.paymentMethod, 
       COUNT(b) AS totalTransactions,
       AVG(b.amount) AS avgAmount,
       SUM(b.amount) AS totalAmount
ORDER BY totalAmount DESC;

// R5. Encontrar clientes con suscripción activa que hayan hecho más de 20 compras previas
MATCH (c:Customer)
WHERE c.subscriptionStatus = 'Yes' AND c.previousPurchases > 20
RETURN c.customerId, c.age, c.location, c.previousPurchases, c.frequency
ORDER BY c.previousPurchases DESC;

// ============================================
// UPDATE - Actualizar datos existentes (5 ejemplos)
// ============================================

// U1. Actualizar la edad de un cliente específico
MATCH (c:Customer {customerId: 1})
SET c.age = 56
RETURN c.customerId, c.age;

// U2. Cambiar el estado de suscripción de clientes de una ubicación específica
MATCH (c:Customer)
WHERE c.location = 'Kentucky'
SET c.subscriptionStatus = 'No'
RETURN c.customerId, c.location, c.subscriptionStatus;

// U3. Actualizar el rating promedio de un producto basado en las compras
MATCH (p:Product {name: 'Blouse'})<-[b:BOUGHT]-()
WITH p, AVG(b.reviewRating) AS newAvgRating
SET p.avgReviewRating = newAvgRating
RETURN p.name, p.avgReviewRating;

// U4. Incrementar el contador de compras previas de un cliente después de una nueva compra
MATCH (c:Customer {customerId: 2})
SET c.previousPurchases = c.previousPurchases + 1
RETURN c.customerId, c.previousPurchases;

// U5. Actualizar múltiples propiedades de un producto
MATCH (p:Product {name: 'Smart Watch'})
SET p.color = 'Silver',
    p.avgReviewRating = 4.7,
    p.season = 'Winter'
RETURN p;

// ============================================
// DELETE - Eliminar datos (5 ejemplos)
// ============================================

// D1. Eliminar un cliente específico y todas sus relaciones
MATCH (c:Customer {customerId: 9999})
DETACH DELETE c;

// D2. Eliminar todas las relaciones de compra con calificación menor a 2.0
MATCH ()-[b:BOUGHT]->()
WHERE b.reviewRating < 2.0
DELETE b;

// D3. Eliminar productos que nunca han sido comprados
MATCH (p:Product)
WHERE NOT (p)<-[:BOUGHT]-()
DELETE p;

// D4. Eliminar la relación entre un producto y su categoría
MATCH (p:Product {name: 'Running Shoes'})-[r:BELONGS_TO]->()
DELETE r;

// D5. Eliminar clientes sin suscripción y sin compras previas
MATCH (c:Customer)
WHERE c.subscriptionStatus = 'No' AND c.previousPurchases = 0
DETACH DELETE c;

// ============================================
// CONSULTAS ADICIONALES ÚTILES
// ============================================

// Contar el total de nodos por tipo
MATCH (n)
RETURN labels(n) AS nodeType, COUNT(n) AS count;

// Ver el esquema de la base de datos
CALL db.schema.visualization();

// Eliminar TODA la base de datos (¡USAR CON PRECAUCIÓN!)
// MATCH (n) DETACH DELETE n;