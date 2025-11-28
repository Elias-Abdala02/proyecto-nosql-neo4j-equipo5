# Neo4j con Docker (Equipo 5)

Estructura mínima para levantar Neo4j y cargar el dataset de compras sin subir datos al repositorio.

## Requisitos
- Docker y Docker Compose plugin instalados.

## Pasos rápidos
1. Copiar el CSV al directorio de importación del contenedor:
   ```bash
   cp ../data/shopping_behavior.csv neo4j-docker/import/
   ```
2. Levantar Neo4j en segundo plano:
   ```bash
   docker compose up -d
   ```
3. Crear constraints e importar datos (desde la raíz del repo):
   ```bash
   cat neo4j/constraints.cypher | docker compose exec -T neo4j cypher-shell -u neo4j -p test123
   cat neo4j/import_nodes.cypher | docker compose exec -T neo4j cypher-shell -u neo4j -p test123
   cat neo4j/import_relationships.cypher | docker compose exec -T neo4j cypher-shell -u neo4j -p test123
   ```
4. Probar CRUD/consultas (ejecutar en Neo4j Browser o con cypher-shell):
   ```bash
   cat neo4j/crud.cypher | docker compose exec -T neo4j cypher-shell -u neo4j -p test123
   ```

## Notas
- Las carpetas `data/`, `logs/`, `import/`, `plugins/` y `conf/` se mantienen vacías en Git; se llenan al ejecutar el contenedor.
- El password por defecto es `test123`; cámbialo si lo deseas y actualiza los comandos.
- El directorio `../neo4j` se monta en `/scripts` dentro del contenedor para ejecutar los archivos `.cypher` sin copiarlos.
