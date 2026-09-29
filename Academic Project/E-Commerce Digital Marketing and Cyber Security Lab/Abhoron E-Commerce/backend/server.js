const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { getEcommerceDb } = require('../database/db');

const PORT = process.env.PORT || 4200;
const FRONTEND_DIR = path.join(__dirname, '..', 'frontend');

function parseBody(req) {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            if (!body) return resolve({});
            try { resolve(JSON.parse(body)); } catch (e) { reject(new Error('Invalid JSON')); }
        });
        req.on('error', reject);
    });
}

function sendJson(res, statusCode, data) {
    res.writeHead(statusCode, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    });
    res.end(JSON.stringify(data));
}

function createEcommerceServer(dbInstance) {
    const db = dbInstance || getEcommerceDb();

    return http.createServer(async (req, res) => {
        if (req.method === 'OPTIONS') {
            res.writeHead(204, {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            });
            return res.end();
        }

        const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
        const pathname = url.pathname;

        try {
            // Categories
            if (pathname === '/api/categories' && req.method === 'GET') {
                const categories = db.query(`SELECT * FROM categories ORDER BY name ASC`);
                return sendJson(res, 200, { categories });
            }

            // Products
            if (pathname === '/api/products' && req.method === 'GET') {
                const catSlug = url.searchParams.get('category');
                let query = `
                    SELECT p.*, c.name as category_name, c.slug as category_slug
                    FROM products p
                    JOIN categories c ON p.category_id = c.id
                `;
                const params = [];
                if (catSlug) {
                    query += ` WHERE c.slug = ?`;
                    params.push(catSlug);
                }
                query += ` ORDER BY p.is_featured DESC, p.created_at DESC`;
                const products = db.query(query, params);
                return sendJson(res, 200, { products });
            }

            // Single Product
            const prodMatch = pathname.match(/^\/api\/products\/(\d+)$/);
            if (prodMatch && req.method === 'GET') {
                const id = parseInt(prodMatch[1]);
                const product = db.get(`
                    SELECT p.*, c.name as category_name
                    FROM products p
                    JOIN categories c ON p.category_id = c.id
                    WHERE p.id = ?
                `, [id]);
                if (!product) return sendJson(res, 404, { error: 'Product not found' });
                return sendJson(res, 200, { product });
            }

            // Checkout / Create Order
            if (pathname === '/api/orders' && req.method === 'POST') {
                const { customer_name, customer_email, shipping_address, phone, payment_method, items } = await parseBody(req);
                if (!customer_name || !customer_email || !shipping_address || !phone || !items || !Array.isArray(items) || items.length === 0) {
                    return sendJson(res, 400, { error: 'Customer details and valid shopping cart items are required.' });
                }

                let totalAmount = 0;
                const orderItemsToInsert = [];

                for (const item of items) {
                    const prod = db.get(`SELECT id, price, stock_quantity FROM products WHERE id = ?`, [item.product_id]);
                    if (!prod) return sendJson(res, 400, { error: `Product ID ${item.product_id} not found.` });
                    const qty = item.quantity || 1;
                    totalAmount += prod.price * qty;
                    orderItemsToInsert.push({ product_id: prod.id, quantity: qty, unit_price: prod.price });
                }

                const orderCode = 'ABH-' + Math.floor(100000 + Math.random() * 900000);
                const orderRes = db.run(
                    `INSERT INTO orders (order_code, customer_name, customer_email, shipping_address, phone, total_amount, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?)`,
                    [orderCode, customer_name.trim(), customer_email.trim(), shipping_address.trim(), phone.trim(), totalAmount, payment_method || 'Demo Cash on Delivery']
                );
                const orderId = orderRes.lastInsertRowid;

                for (const oi of orderItemsToInsert) {
                    db.run(
                        `INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)`,
                        [orderId, oi.product_id, oi.quantity, oi.unit_price]
                    );
                }

                return sendJson(res, 201, {
                    message: 'Order placed successfully (Demonstration Mode)',
                    order_code: orderCode,
                    total_amount: totalAmount
                });
            }

            // Admin: List Orders
            if (pathname === '/api/orders' && req.method === 'GET') {
                const orders = db.query(`SELECT * FROM orders ORDER BY created_at DESC`);
                return sendJson(res, 200, { orders });
            }

            // Static Web Serving
            let filePath = path.join(FRONTEND_DIR, pathname === '/' ? 'index.html' : pathname);
            if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
                const ext = path.extname(filePath).toLowerCase();
                const mime = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json' };
                res.writeHead(200, { 'Content-Type': mime[ext] || 'text/plain' });
                return fs.createReadStream(filePath).pipe(res);
            }

            return sendJson(res, 404, { error: 'Not found' });
        } catch (err) {
            console.error('Ecommerce Server Error:', err);
            return sendJson(res, 500, { error: err.message });
        }
    });
}

if (require.main === module) {
    const server = createEcommerceServer();
    server.listen(PORT, () => {
        console.log(`[+] Abhoron E-Commerce Server running at http://localhost:${PORT}`);
    });
}

module.exports = { createEcommerceServer };
