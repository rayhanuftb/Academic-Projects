const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs');
const { EcommerceDatabaseManager } = require('../database/db');
const { createEcommerceServer } = require('../backend/server');
const { seedEcommerceDatabase } = require('../database/seed');

const TEST_DB = path.join(__dirname, 'test_ecommerce.db');

test('Abhoron E-Commerce Test Suite', async (t) => {
    if (fs.existsSync(TEST_DB)) {
        try { fs.unlinkSync(TEST_DB); } catch (_) {}
    }
    const db = new EcommerceDatabaseManager(TEST_DB);
    seedEcommerceDatabase(TEST_DB);

    const server = createEcommerceServer(db);
    await new Promise(res => server.listen(0, res));
    const port = server.address().port;
    const base = `http://localhost:${port}/api`;

    t.after(() => {
        try { server.close(); } catch (_) {}
        try { db.close(); } catch (_) {}
        try { if (fs.existsSync(TEST_DB)) fs.unlinkSync(TEST_DB); } catch (_) {}
    });

    await t.test('1. Should fetch product categories', async () => {
        const res = await fetch(`${base}/categories`);
        const data = await res.json();
        assert.strictEqual(res.status, 200);
        assert.ok(data.categories.length >= 4);
    });

    await t.test('2. Should list products and filter by category', async () => {
        const resAll = await fetch(`${base}/products`);
        const allData = await resAll.json();
        assert.strictEqual(resAll.status, 200);
        assert.ok(allData.products.length >= 5);

        const resCat = await fetch(`${base}/products?category=sarees`);
        const catData = await resCat.json();
        assert.strictEqual(resCat.status, 200);
        assert.ok(catData.products.length >= 2);
    });

    await t.test('3. Should process order checkout successfully', async () => {
        const res = await fetch(`${base}/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                customer_name: 'Rayhanul Islam',
                customer_email: 'rayhanul@example.com',
                phone: '+8801700000001',
                shipping_address: 'Mirpur, Dhaka, Bangladesh',
                payment_method: 'Demo bKash / Nagad',
                items: [{ product_id: 1, quantity: 2 }]
            })
        });
        const data = await res.json();
        assert.strictEqual(res.status, 201);
        assert.ok(data.order_code);
        assert.strictEqual(data.total_amount, 17000); // 8500 * 2
    });
});
