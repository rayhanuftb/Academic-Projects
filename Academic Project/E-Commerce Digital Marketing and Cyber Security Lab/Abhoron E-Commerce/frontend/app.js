const API = '/api';
let allProducts = [];
let cart = JSON.parse(localStorage.getItem('abhoron_cart') || '[]');
let activeCat = null;

document.addEventListener('DOMContentLoaded', () => {
    loadCategories();
    loadProducts();
    updateCartUI();
});

function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.remove('hidden');
    setTimeout(() => t.classList.add('hidden'), 3000);
}

async function loadCategories() {
    try {
        const res = await fetch(`${API}/categories`);
        const data = await res.json();
        const cont = document.getElementById('category-filter-container');
        cont.innerHTML = `
            <button class="cat-pill ${!activeCat ? 'active' : ''}" onclick="filterCategory(null)">All Collections</button>
            ${(data.categories || []).map(c => `
                <button class="cat-pill ${activeCat === c.slug ? 'active' : ''}" onclick="filterCategory('${c.slug}')">${c.name}</button>
            `).join('')}
        `;
    } catch (_) {}
}

async function loadProducts() {
    try {
        const url = activeCat ? `${API}/products?category=${activeCat}` : `${API}/products`;
        const res = await fetch(url);
        const data = await res.json();
        allProducts = data.products || [];
        renderProducts(allProducts);
    } catch (_) {}
}

function renderProducts(prods) {
    const grid = document.getElementById('product-grid-container');
    if (prods.length === 0) {
        grid.innerHTML = '<p>No products found in this category.</p>';
        return;
    }
    grid.innerHTML = prods.map(p => `
        <div class="prod-card">
            <img src="${p.image_url}" alt="${p.title}" class="prod-img">
            <div class="prod-body">
                <span class="prod-cat">${p.category_name}</span>
                <h3 class="prod-title">${p.title}</h3>
                <p class="prod-fabric">Fabric: ${p.fabric_type}</p>
                <div class="prod-price">৳${p.price.toLocaleString()}</div>
                <button class="btn btn-primary btn-block" onclick="addToCart(${p.id})">Add to Bag</button>
            </div>
        </div>
    `).join('');
}

function filterCategory(slug) {
    activeCat = slug;
    loadCategories();
    loadProducts();
}

function handleSearch() {
    const query = document.getElementById('search-input').value.toLowerCase();
    const filtered = allProducts.filter(p => p.title.toLowerCase().includes(query) || p.fabric_type.toLowerCase().includes(query));
    renderProducts(filtered);
}

function addToCart(prodId) {
    const prod = allProducts.find(p => p.id === prodId);
    if (!prod) return;

    const existing = cart.find(item => item.id === prodId);
    if (existing) {
        existing.quantity++;
    } else {
        cart.push({ id: prod.id, title: prod.title, price: prod.price, quantity: 1 });
    }
    localStorage.setItem('abhoron_cart', JSON.stringify(cart));
    updateCartUI();
    showToast(`Added "${prod.title}" to bag!`);
}

function updateCartUI() {
    const count = cart.reduce((sum, i) => sum + i.quantity, 0);
    const total = cart.reduce((sum, i) => sum + (i.price * i.quantity), 0);
    document.getElementById('cart-count').textContent = count;

    const cont = document.getElementById('cart-items-container');
    if (cart.length === 0) {
        cont.innerHTML = '<p style="text-align: center; color: var(--muted);">Your shopping bag is empty.</p>';
        document.getElementById('cart-total-amount').textContent = '0';
        return;
    }

    cont.innerHTML = cart.map((item, idx) => `
        <div class="cart-item">
            <div>
                <strong>${item.title}</strong><br>
                <small>৳${item.price.toLocaleString()} × ${item.quantity}</small>
            </div>
            <div>
                <button onclick="removeFromCart(${idx})" style="background:none; border:none; color:var(--primary); cursor:pointer; font-weight:700;">✕</button>
            </div>
        </div>
    `).join('');

    document.getElementById('cart-total-amount').textContent = total.toLocaleString();
}

function removeFromCart(idx) {
    cart.splice(idx, 1);
    localStorage.setItem('abhoron_cart', JSON.stringify(cart));
    updateCartUI();
}

function toggleCartModal() {
    document.getElementById('cart-modal').classList.toggle('hidden');
}

function openCheckoutModal() {
    if (cart.length === 0) return showToast('Your bag is empty!');
    document.getElementById('cart-modal').classList.add('hidden');
    document.getElementById('checkout-modal').classList.remove('hidden');
}

function closeCheckoutModal() {
    document.getElementById('checkout-modal').classList.add('hidden');
}

async function handleCheckout(e) {
    e.preventDefault();
    const orderPayload = {
        customer_name: document.getElementById('chk-name').value,
        customer_email: document.getElementById('chk-email').value,
        phone: document.getElementById('chk-phone').value,
        shipping_address: document.getElementById('chk-address').value,
        payment_method: document.getElementById('chk-payment').value,
        items: cart.map(i => ({ product_id: i.id, quantity: i.quantity }))
    };

    try {
        const res = await fetch(`${API}/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderPayload)
        });
        const data = await res.json();
        if (res.ok) {
            cart = [];
            localStorage.removeItem('abhoron_cart');
            updateCartUI();
            closeCheckoutModal();
            alert(`🎉 Order Confirmed!\n\nOrder Code: ${data.order_code}\nTotal: ৳${data.total_amount.toLocaleString()}\n\nThank you for exploring Abhoron E-Commerce.`);
        } else {
            alert(`Checkout Error: ${data.error}`);
        }
    } catch (err) {
        alert(`Checkout Failed: ${err.message}`);
    }
}
