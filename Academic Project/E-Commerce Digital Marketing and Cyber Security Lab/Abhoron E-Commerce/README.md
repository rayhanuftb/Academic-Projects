# আভরণ (Abhoron): E-Commerce Website for Clothing and Textiles

**Course:** E-Commerce, Digital Marketing and Cyber Security Lab (ICT 4364)  
**Academic Program:** B.Sc. in Educational Technology and Engineering  
**Institution:** University of Frontier Technology, Bangladesh  
**Author:** Rayhanul Islam

---

## 📌 Project Overview

**আভরণ (Abhoron)** is a responsive, boutique e-commerce web platform celebrating Bangladeshi handloom textiles, pure silk, and artisanal heritage apparel. It features full catalog browsing, category filtering, real-time search, interactive shopping cart management, demonstration checkout processing, SEO digital marketing metadata, and transactional order persistence.

---

## 🎯 Key Features

1. **Artisanal Product Catalog**: Categorized collections for Jamdani Sarees, Rajshahi Silk, Hand-spun Khadi Panjabis, Kurtis, and Indigenous Shawls.
2. **Dynamic Filtering & Search**: Client-side filtering by category slug and real-time keyword search.
3. **Cart & Local Persistence**: Responsive shopping bag with dynamic quantity calculation and `localStorage` state persistence.
4. **Demonstration Checkout**: Validates customer shipping and contact details and creates database order records with unique order tracking codes (`ABH-XXXXXX`).
5. **SEO & Digital Marketing**: OpenGraph social media sharing metadata, semantic schema markup, and responsive typography.

---

## 🏗️ Project Structure

```
Abhoron E-Commerce/
├── backend/
│   └── server.js           # REST API server (Node.js)
├── database/
│   ├── db.js               # SQLite connection manager
│   ├── schema.sql          # Relational SQL schema
│   ├── seed.js             # Sample product catalog seed script
│   └── ecommerce.db        # Persistent SQLite database
├── frontend/
│   ├── index.html          # Responsive e-commerce storefront UI
│   ├── styles.css          # Boutique heritage styling
│   └── app.js              # Client-side shopping cart & checkout logic
├── tests/
│   └── ecommerce.test.js   # Automated integration test suite
├── package.json
└── README.md
```

---

## 🚀 Execution Instructions

### 1. Seed Product Catalog
```bash
node database/seed.js
```

### 2. Start Application Server
```bash
node backend/server.js
```
Navigate to: `http://localhost:4200`

### 3. Run Automated Tests
```bash
npm test
```
*(or `node --test tests/ecommerce.test.js`)*
