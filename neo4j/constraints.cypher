// ============================================
// CONSTRAINTS - Shopping Behaviour Dataset
// ============================================
// Este archivo define las restricciones de integridad para garantizar
// la unicidad de identificadores y propiedades clave.

// Restricción de unicidad para el ID de clientes
CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
FOR (c:Customer) REQUIRE c.customerId IS UNIQUE;

// Restricción de unicidad para el nombre de categorías
CREATE CONSTRAINT category_name_unique IF NOT EXISTS
FOR (cat:Category) REQUIRE cat.name IS UNIQUE;

// Restricción de unicidad para productos (combinación de nombre, color y talla)
// Nota: Neo4j no soporta constraints compuestos nativamente en versiones community
// Se puede lograr con un identificador compuesto
CREATE CONSTRAINT product_composite_unique IF NOT EXISTS
FOR (p:Product) REQUIRE p.productId IS UNIQUE;

// Índices para mejorar el rendimiento de las consultas
CREATE INDEX customer_age_index IF NOT EXISTS
FOR (c:Customer) ON (c.age);

CREATE INDEX customer_location_index IF NOT EXISTS
FOR (c:Customer) ON (c.location);

CREATE INDEX product_name_index IF NOT EXISTS
FOR (p:Product) ON (p.name);

// Verificar las restricciones creadas
SHOW CONSTRAINTS;

// Verificar los índices creados
SHOW INDEXES;
