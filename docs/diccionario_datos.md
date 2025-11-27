# Diccionario de Datos

## Descripción General

Este documento describe la estructura de datos del proyecto Neo4j basado en el dataset **Shopping Behaviour and Product Ranking Dataset** obtenido de Kaggle.

## Fuente de Datos

- **Archivo**: `shopping_behavior.csv`
- **Ubicación**: `/data/shopping_behavior.csv`
- **Número de registros**: 3,900 transacciones
- **Formato**: CSV con encabezados

## Entidades (Nodos) y Atributos

### Customer (Cliente)

Representa a los clientes que realizan compras en la tienda.

| Campo | Tipo Neo4j | Tipo Original | Descripción | Restricciones |
|-------|-----------|---------------|-------------|---------------|
| customerId | Integer | INT | Identificador único del cliente | Clave primaria, UNIQUE |
| age | Integer | INT | Edad del cliente | No nulo, rango típico: 18-70 |
| gender | String | STRING | Género del cliente | Valores: 'Male', 'Female' |
| location | String | STRING | Estado de residencia | Estados de EE.UU. |
| subscriptionStatus | String | STRING | Estado de suscripción | Valores: 'Yes', 'No' |
| previousPurchases | Integer | INT | Número de compras previas | No negativo |
| frequency | String | STRING | Frecuencia de compra | Valores: 'Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Annually' |

### Product (Producto)

Representa los productos disponibles en la tienda.

| Campo | Tipo Neo4j | Tipo Original | Descripción | Restricciones |
|-------|-----------|---------------|-------------|---------------|
| productId | String | Compuesto | Identificador único (name_color_size_season) | Clave primaria, UNIQUE |
| name | String | STRING | Nombre del producto | No nulo |
| size | String | STRING | Talla del producto | Valores: 'S', 'M', 'L', 'XL' |
| color | String | STRING | Color del producto | Variedad de colores |
| season | String | STRING | Temporada del producto | Valores: 'Spring', 'Summer', 'Fall', 'Winter' |
| avgReviewRating | Float | FLOAT | Calificación promedio | Rango: 1.0-5.0 |

### Category (Categoría)

Representa las categorías de productos.

| Campo | Tipo Neo4j | Tipo Original | Descripción | Restricciones |
|-------|-----------|---------------|-------------|---------------|
| name | String | STRING | Nombre de la categoría | Clave primaria, UNIQUE |

**Categorías existentes**: Clothing, Footwear, Outerwear, Accessories

## Relaciones (Edges)

### BOUGHT (Compra)

Relación entre un Cliente y un Producto que representa una transacción de compra.

- **Nodos origen**: Customer
- **Nodos destino**: Product
- **Cardinalidad**: Muchos a muchos (un cliente puede comprar múltiples productos, un producto puede ser comprado por múltiples clientes)

**Propiedades de la relación:**

| Propiedad | Tipo | Descripción | Restricciones |
|-----------|------|-------------|---------------|
| amount | Float | Monto de la compra en USD | No negativo |
| discountApplied | String | Indica si se aplicó descuento | Valores: 'Yes', 'No' |
| reviewRating | Float | Calificación del cliente | Rango: 1.0-5.0 |
| paymentMethod | String | Método de pago utilizado | Valores: 'Cash', 'Credit Card', 'PayPal', 'Venmo', 'Debit Card' |
| purchaseDate | DateTime | Fecha de la transacción | Generada al importar |

### BELONGS_TO (Pertenece a)

Relación entre un Producto y su Categoría.

- **Nodos origen**: Product
- **Nodos destino**: Category
- **Cardinalidad**: Muchos a uno (cada producto pertenece a una categoría, una categoría tiene múltiples productos)

**Propiedades de la relación:** Ninguna

## Modelo de Grafo

```text
(Customer)-[:BOUGHT]->(Product)-[:BELONGS_TO]->(Category)
```

### Ejemplo de instancia

```cypher
(:Customer {customerId: 1, age: 55, gender: 'Male', location: 'Kentucky'})
  -[:BOUGHT {amount: 53.0, reviewRating: 3.1, paymentMethod: 'Venmo'}]->
(:Product {name: 'Blouse', color: 'Gray', size: 'L', season: 'Winter'})
  -[:BELONGS_TO]->
(:Category {name: 'Clothing'})
```

## Transformaciones de Datos

### Campos compuestos

- **productId**: Se genera concatenando `name + '_' + color + '_' + size + '_' + season` para garantizar unicidad de productos.

### Conversiones de tipo

- `Customer ID` → `customerId` (String a Integer)
- `Age` → `age` (String a Integer)
- `Purchase Amount (USD)` → `amount` (String a Float)
- `Review Rating` → `reviewRating` (String a Float)
- `Previous Purchases` → `previousPurchases` (String a Integer)

## Estadísticas del Dataset

- **Total de clientes únicos**: ~3,900
- **Total de productos únicos**: Varía según combinación color/talla/temporada
- **Total de categorías**: 4
- **Total de transacciones**: 3,900
- **Rango de precios**: $20 - $100 USD
- **Rango de edad de clientes**: 18-70 años

## Notas Adicionales

1. El dataset fue diseñado para análisis de comportamiento de compra y permite estudiar patrones de consumo por demografía, temporada y categoría.

2. Las relaciones `BOUGHT` contienen propiedades ricas que permiten análisis de preferencias de pago, satisfacción del cliente (review rating) y efectividad de descuentos.

3. El modelo permite consultas complejas como:
   - Productos más vendidos por temporada
   - Clientes de alto valor
   - Análisis de retención (subscription status)
   - Patrones de compra por ubicación geográfica
