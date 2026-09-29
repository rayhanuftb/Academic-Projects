const { getEcommerceDb } = require('./db');

function seedEcommerceDatabase(dbPath) {
    const db = getEcommerceDb(dbPath);

    console.log('[+] Seeding Abhoron E-Commerce Database...');

    db.exec(`
        DELETE FROM order_items;
        DELETE FROM orders;
        DELETE FROM products;
        DELETE FROM categories;
    `);

    // 1. Categories
    db.run(`INSERT INTO categories (name, slug, description) VALUES (?, ?, ?)`, ['Traditional Sarees', 'sarees', 'Handloom Jamdani, Silk, and Muslin artisanal sarees.']);
    const cat1 = db.get(`SELECT id FROM categories WHERE slug = 'sarees'`).id;

    db.run(`INSERT INTO categories (name, slug, description) VALUES (?, ?, ?)`, ['Men\'s Panjabi', 'panjabis', 'Handcrafted cotton, silk, and embroidered panjabis.']);
    const cat2 = db.get(`SELECT id FROM categories WHERE slug = 'panjabis'`).id;

    db.run(`INSERT INTO categories (name, slug, description) VALUES (?, ?, ?)`, ['Kurtis & Tunics', 'kurtis', 'Contemporary ethnic kurtis for festive and casual wear.']);
    const cat3 = db.get(`SELECT id FROM categories WHERE slug = 'kurtis'`).id;

    db.run(`INSERT INTO categories (name, slug, description) VALUES (?, ?, ?)`, ['Textiles & Shawls', 'fabrics', 'Handwoven indigenous shawls and organic textile yardages.']);
    const cat4 = db.get(`SELECT id FROM categories WHERE slug = 'fabrics'`).id;

    // 2. Products
    db.run(`INSERT INTO products (category_id, title, slug, description, price, fabric_type, stock_quantity, image_url, is_featured) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [cat1, 'Royal Dhakai Jamdani Saree', 'royal-dhakai-jamdani', 'Authentic geometric floral motif handwoven on wooden pit looms with fine cotton yarn.', 8500.00, 'Pure Cotton Jamdani', 12, 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600&q=80', 1]
    );

    db.run(`INSERT INTO products (category_id, title, slug, description, price, fabric_type, stock_quantity, image_url, is_featured) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [cat1, 'Rajshahi Mulberry Silk Saree', 'rajshahi-mulberry-silk', 'Exquisite natural Mulberry silk featuring traditional block-printed borders.', 12500.00, 'Mulberry Silk', 8, 'https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=600&q=80', 1]
    );

    db.run(`INSERT INTO products (category_id, title, slug, description, price, fabric_type, stock_quantity, image_url, is_featured) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [cat2, 'Heritage Khadi Embroidered Panjabi', 'heritage-khadi-panjabi', 'Eco-friendly hand-spun Khadi cotton panjabi with delicate kantha-stitch neck embroidery.', 3200.00, 'Handspun Khadi Cotton', 20, 'https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=600&q=80', 1]
    );

    db.run(`INSERT INTO products (category_id, title, slug, description, price, fabric_type, stock_quantity, image_url, is_featured) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [cat3, 'Indigo Floral Printed Kurti', 'indigo-floral-kurti', 'Breathable organic cotton kurti dyed with natural vegetable indigo extracts.', 1850.00, 'Organic Cotton', 25, 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&q=80', 0]
    );

    db.run(`INSERT INTO products (category_id, title, slug, description, price, fabric_type, stock_quantity, image_url, is_featured) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [cat4, 'Handloom Kashmiri Pattern Shawl', 'handloom-kashmiri-shawl', 'Finely brushed soft wool shawl featuring classic paisley needlework.', 4500.00, 'Pure Wool', 15, 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600&q=80', 0]
    );

    console.log('[+] Abhoron E-Commerce database seeded successfully.');
}

if (require.main === module) {
    seedEcommerceDatabase();
}

module.exports = { seedEcommerceDatabase };
