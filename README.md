# Proyecto Neo4j - Análisis de Comportamiento de Compras

## Descripción
Proyecto de base de datos NoSQL utilizando Neo4j para analizar patrones de comportamiento de compras.

## Estructura del Proyecto

```
proyecto-nosql-neo4j-equipo5/
├── data/
│   └── shopping_behaviour.csv      # Dataset de comportamiento de compras
├── neo4j/
│   ├── constraints.cypher          # Restricciones de la base de datos
│   ├── import_nodes.cypher         # Scripts para importar nodos
│   ├── import_relationships.cypher # Scripts para crear relaciones
│   └── crud.cypher                 # Operaciones CRUD
├── docs/
│   ├── diccionario_datos.md        # Diccionario de datos
│   ├── modelo_grafo.drawio         # Modelo de grafo (editable)
│   └── modelo_grafo.png            # Modelo de grafo (imagen)
└── README.md                        # Este archivo
```

## Requisitos

- Neo4j Desktop o Neo4j Community Edition
- Python 3.x (opcional, para procesamiento de datos)

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/Elias-Abdala02/proyecto-nosql-neo4j-equipo5.git
cd proyecto-nosql-neo4j-equipo5
```

2. Instala Neo4j Desktop desde [neo4j.com/download](https://neo4j.com/download/)

3. Crea una nueva base de datos en Neo4j Desktop

## Uso

### 1. Importar Datos

1. Copia el archivo `data/shopping_behaviour.csv` a la carpeta `import` de tu base de datos Neo4j
2. Ejecuta los scripts en el siguiente orden:
   ```cypher
   // 1. Crear restricciones
   :source neo4j/constraints.cypher
   
   // 2. Importar nodos
   :source neo4j/import_nodes.cypher
   
   // 3. Crear relaciones
   :source neo4j/import_relationships.cypher
   ```

### 2. Operaciones CRUD

Consulta el archivo `neo4j/crud.cypher` para ejemplos de operaciones Create, Read, Update y Delete.

## Documentación

- **Diccionario de Datos**: Ver `docs/diccionario_datos.md`
- **Modelo de Grafo**: Ver `docs/modelo_grafo.png`

## Equipo

- [Nombre del integrante 1]
- [Nombre del integrante 2]
- [Nombre del integrante 3]
- [Nombre del integrante 4]
- [Nombre del integrante 5]

## Licencia

Este proyecto es parte de un trabajo académico para la materia de Modelado de Datos.
