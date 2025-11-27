# Guía Rápida de Uso - Proyecto Neo4j

## 📋 Pasos para Ejecutar el Proyecto

### 1️⃣ Preparar Neo4j

1. **Instalar Neo4j Desktop**
   - Descargar desde: <https://neo4j.com/download/>
   - Crear una nueva base de datos
   - Iniciar la base de datos

2. **Copiar el archivo CSV**

   ```bash
   # Ubicar la carpeta 'import' de tu base de datos Neo4j
   # Típicamente en: <neo4j-home>/import/
   # Copiar shopping_behavior.csv a esa carpeta
   ```

### 2️⃣ Ejecutar Scripts en Orden

Abrir Neo4j Browser y ejecutar los scripts en este orden:

#### Paso 1: Crear Restricciones

```cypher
// Copiar y ejecutar todo el contenido de:
:source neo4j/constraints.cypher
```

#### Paso 2: Importar Nodos

```cypher
// Copiar y ejecutar todo el contenido de:
:source neo4j/import_nodes.cypher
```

#### Paso 3: Crear Relaciones

```cypher
// Copiar y ejecutar todo el contenido de:
:source neo4j/import_relationships.cypher
```

### 3️⃣ Verificar Importación

```cypher
// Contar nodos por tipo
MATCH (n)
RETURN labels(n)[0] AS tipo, COUNT(n) AS cantidad;

// Ver el esquema completo
CALL db.schema.visualization();

// Ver un ejemplo del grafo
MATCH path = (c:Customer)-[:BOUGHT]->(p:Product)-[:BELONGS_TO]->(cat:Category)
RETURN path
LIMIT 10;
```

### 4️⃣ Probar Operaciones CRUD

Ejecutar las sentencias del archivo `neo4j/crud.cypher` una por una para probar:

- ✅ **CREATE**: 5 operaciones de creación
- 📖 **READ**: 5 consultas de lectura
- ♻️ **UPDATE**: 5 operaciones de actualización
- 🗑️ **DELETE**: 5 operaciones de eliminación

## 🔍 Consultas Útiles

### Análisis por Categoría

```cypher
MATCH (c:Customer)-[b:BOUGHT]->(p:Product)-[:BELONGS_TO]->(cat:Category)
RETURN cat.name AS categoria, 
       COUNT(b) AS totalVentas,
       SUM(b.amount) AS montoTotal,
       AVG(b.reviewRating) AS ratingPromedio
ORDER BY totalVentas DESC;
```

### Top 10 Clientes

```cypher
MATCH (c:Customer)-[b:BOUGHT]->()
RETURN c.customerId, c.age, c.location,
       COUNT(b) AS totalCompras,
       SUM(b.amount) AS montoTotal
ORDER BY montoTotal DESC
LIMIT 10;
```

### Productos por Temporada

```cypher
MATCH (p:Product)<-[b:BOUGHT]-()
WHERE p.season = 'Winter'
RETURN p.name, p.color, p.size,
       COUNT(b) AS ventas,
       AVG(b.reviewRating) AS rating
ORDER BY ventas DESC
LIMIT 10;
```

## 🚨 Solución de Problemas

### Error: "file not found"

- Asegúrate de que `shopping_behavior.csv` está en la carpeta `import` de Neo4j
- Verifica el nombre exacto del archivo (case-sensitive)

### Error: "constraint already exists"

- Las restricciones ya están creadas
- Puedes saltar ese paso o ejecutar: `DROP CONSTRAINT nombre_constraint`

### Error: "Node already exists"

- Usa `MERGE` en lugar de `CREATE` para evitar duplicados
- O ejecuta primero: `MATCH (n) DETACH DELETE n` (⚠️ borra todo)

## 📚 Recursos Adicionales

- **Neo4j Browser Guide**: Ejecutar `:guide` en Neo4j Browser
- **Cypher Refcard**: <https://neo4j.com/docs/cypher-refcard/current/>
- **Documentación del Proyecto**: Ver `README.md`
- **Diccionario de Datos**: Ver `docs/diccionario_datos.md`
