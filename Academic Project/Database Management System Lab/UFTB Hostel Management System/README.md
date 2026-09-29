# UFTB Hostel Management System

**Course:** Database Management System Lab (ICT 4254)  
**Academic Program:** B.Sc. in Educational Technology and Engineering  
**Institution:** University of Frontier Technology, Bangladesh  
**Author:** Rayhanul Islam

---

## 📌 Project Overview

The **UFTB Hostel Management System** is a full-stack database application engineered to manage university residential operations. It implements relational database normalization, CRUD operations, room allocation tracking, fee payment invoicing, and maintenance ticket logging.

---

## 🎯 Key Database Entities & Relationships

- **`blocks`**: Hostel buildings, gender eligibility, and floor infrastructure.
- **`rooms`**: Block foreign-key relation, room numbers, bed capacities, and rental rates.
- **`students`**: Student academic identifiers, departments, and contact information.
- **`allocations`**: Many-to-many relationship linking students to allocated beds with occupancy tracking and uniqueness constraints.
- **`fee_payments`**: Monthly residential fee tracking, billing history, and payment status.
- **`maintenance_requests`**: Facility issue tickets linked to specific rooms with priority and resolution workflows.

---

## 🏗️ Project Structure

```
UFTB Hostel Management System/
├── backend/
│   └── server.js           # REST API server (Node.js)
├── database/
│   ├── db.js               # SQLite connection manager
│   ├── schema.sql          # Relational SQL schema
│   ├── seed.js             # Sample data generator
│   └── hostel.db           # Persistent SQLite database
├── frontend/
│   ├── index.html          # Responsive management dashboard UI
│   ├── styles.css          # Modern CSS styling
│   └── app.js              # Frontend client application logic
├── tests/
│   └── hostel.test.js      # Automated CRUD & integration test suite
├── package.json
└── README.md
```

---

## 🚀 Execution Instructions

### 1. Seed Database
```bash
node database/seed.js
```

### 2. Start Application Server
```bash
node backend/server.js
```
Navigate to: `http://localhost:4100`

### 3. Run Automated Tests
```bash
npm test
```
*(or `node --test tests/hostel.test.js`)*
