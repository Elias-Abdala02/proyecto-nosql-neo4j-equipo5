// CRUD Operations
// This file contains example CRUD (Create, Read, Update, Delete) operations

// ============================================
// CREATE - Examples
// ============================================

// Example: Create a new customer
// CREATE (:Customer {id: 'C001', name: 'John Doe', age: 30});

// ============================================
// READ - Examples
// ============================================

// Example: Find all customers
// MATCH (c:Customer) RETURN c;

// Example: Find customers by age
// MATCH (c:Customer) WHERE c.age > 25 RETURN c;

// ============================================
// UPDATE - Examples
// ============================================

// Example: Update customer information
// MATCH (c:Customer {id: 'C001'})
// SET c.age = 31
// RETURN c;

// ============================================
// DELETE - Examples
// ============================================

// Example: Delete a specific customer
// MATCH (c:Customer {id: 'C001'})
// DELETE c;

// Example: Delete all nodes and relationships (use with caution!)
// MATCH (n) DETACH DELETE n;
