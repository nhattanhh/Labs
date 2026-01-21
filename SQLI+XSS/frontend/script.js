// CodeShop - Frontend JavaScript
// Flat design, consistent colors

const API_BASE = '/api';

const productsGrid = document.getElementById('productsGrid');
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
const searchResultsGrid = document.getElementById('searchResultsGrid');
const searchMessage = document.getElementById('searchMessage');
const loginBtn = document.getElementById('loginBtn');
const loginModal = document.getElementById('loginModal');
const loginForm = document.getElementById('loginForm');
const loginMessage = document.getElementById('loginMessage');
const userBanner = document.getElementById('userBanner');
const welcomeMessage = document.getElementById('welcomeMessage');
const logoutBtn = document.getElementById('logoutBtn');
const reviewForm = document.getElementById('reviewForm');
const reviewsContainer = document.getElementById('reviewsContainer');
const productSelect = document.getElementById('productSelect');
const filterTabs = document.querySelectorAll('.filter-tab');
const ratingBtns = document.querySelectorAll('.rating-btn');

let currentUser = null;
let currentRating = 5;
let allProducts = [];

document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    loadReviews();
    setupEventListeners();
});

function setupEventListeners() {
    document.querySelector('.search-btn')?.addEventListener('click', handleSearch);
    searchInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });

    loginBtn?.addEventListener('click', openLoginModal);
    loginModal?.querySelector('.modal-overlay')?.addEventListener('click', closeLoginModal);
    loginModal?.querySelector('.modal-close')?.addEventListener('click', closeLoginModal);
    loginForm?.addEventListener('submit', handleLogin);
    logoutBtn?.addEventListener('click', handleLogout);

    reviewForm?.addEventListener('submit', handleReviewSubmit);
    ratingBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentRating = parseInt(btn.dataset.rating);
            updateRatingDisplay();
        });
    });

    filterTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            filterTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            filterProducts(tab.dataset.category);
        });
    });
}

// Parse image format: "colors|text" or URL
function parseImageUrl(imageUrl) {
    if (!imageUrl) return { type: 'text', text: '?' };

    if (imageUrl.includes('|')) {
        const parts = imageUrl.split('|');
        return { type: 'text', text: parts[1] || '?' };
    }

    if (imageUrl.startsWith('http') || imageUrl.startsWith('/')) {
        return { type: 'image', url: imageUrl };
    }

    return { type: 'text', text: imageUrl.substring(0, 2).toUpperCase() };
}

async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE}/products`);
        const data = await response.json();
        if (data.success) {
            allProducts = data.products;
            renderProducts(allProducts);
            populateProductSelect(allProducts);
        }
    } catch (error) {
        console.error('Error:', error);
        if (productsGrid) productsGrid.innerHTML = '<p>Unable to load courses.</p>';
    }
}

function renderProducts(products) {
    if (!products || products.length === 0) {
        productsGrid.innerHTML = '<p>No courses found.</p>';
        return;
    }
    productsGrid.innerHTML = products.map(p => createProductCard(p)).join('');
}

function createProductCard(product) {
    const img = parseImageUrl(product.image_url);
    const imageContent = img.type === 'image'
        ? `<img src="${img.url}" alt="${product.name}" style="width:100%;height:100%;object-fit:cover;">`
        : `<div class="product-icon">${img.text}</div>`;

    return `
        <div class="product-card">
            <div class="product-image">
                ${imageContent}
                <span class="product-badge">${product.category}</span>
            </div>
            <div class="product-content">
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description}</p>
                <div class="product-meta">
                    <span class="product-price">$${product.price}</span>
                    <span class="product-level">${product.age_range || 'All'}</span>
                </div>
            </div>
        </div>
    `;
}

function filterProducts(category) {
    if (category === 'all') {
        renderProducts(allProducts);
    } else {
        renderProducts(allProducts.filter(p => p.category === category));
    }
}

function populateProductSelect(products) {
    if (!productSelect) return;
    productSelect.innerHTML = '<option value="">Select course...</option>' +
        products.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
}

// VULNERABLE TO SQL INJECTION
async function handleSearch() {
    const query = searchInput?.value.trim();
    if (!query) return;
    try {
        const response = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        showSearchResults(data);
    } catch (error) {
        console.error('Search error:', error);
    }
}

function showSearchResults(data) {
    searchResults.classList.remove('hidden');
    // XSS VULNERABLE
    searchMessage.innerHTML = data.message;
    if (data.products && data.products.length > 0) {
        searchResultsGrid.innerHTML = data.products.map(p => createProductCard(p)).join('');
    } else {
        searchResultsGrid.innerHTML = `<p>No results for "${data.search_term}"</p>`;
    }
    searchResults.scrollIntoView({ behavior: 'smooth' });
}

function openLoginModal() {
    loginModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeLoginModal() {
    loginModal.classList.add('hidden');
    document.body.style.overflow = '';
    if (loginMessage) {
        loginMessage.textContent = '';
        loginMessage.className = '';
    }
    loginForm?.reset();
}

// VULNERABLE TO SQL INJECTION
async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();

        if (data.success) {
            currentUser = data.user;
            loginMessage.textContent = data.message;
            loginMessage.className = 'success';
            setTimeout(() => {
                closeLoginModal();
                showUserBanner(data.user);
            }, 1000);
        } else {
            loginMessage.textContent = data.message || 'Login failed';
            loginMessage.className = 'error';
        }
    } catch (error) {
        loginMessage.textContent = 'Network error';
        loginMessage.className = 'error';
    }
}

function showUserBanner(user) {
    userBanner.classList.remove('hidden');
    // XSS VULNERABLE
    welcomeMessage.innerHTML = `Welcome, <strong>${user.username}</strong> (${user.role})`;
    loginBtn.textContent = user.username;
}

function handleLogout() {
    currentUser = null;
    userBanner.classList.add('hidden');
    loginBtn.textContent = 'Sign In';
}

// VULNERABLE TO STORED XSS
async function loadReviews() {
    try {
        const response = await fetch(`${API_BASE}/reviews?product_id=1`);
        const data = await response.json();
        if (data.success) renderReviews(data.reviews);
    } catch (error) {
        console.error('Error:', error);
    }
}

function renderReviews(reviews) {
    if (!reviews || reviews.length === 0) {
        reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
        return;
    }
    // XSS VULNERABLE
    reviewsContainer.innerHTML = reviews.map(r => `
        <div class="review-card">
            <div class="review-header">
                <span class="reviewer-name">${r.reviewer_name}</span>
                <span class="review-rating">${'*'.repeat(r.rating)}</span>
            </div>
            <p class="review-text">${r.review_text}</p>
            <span class="review-date">${r.created_at}</span>
        </div>
    `).join('');
}

function updateRatingDisplay() {
    ratingBtns.forEach((btn, i) => {
        btn.classList.toggle('active', i < currentRating);
    });
}

async function handleReviewSubmit(e) {
    e.preventDefault();
    const productId = productSelect.value;
    const name = document.getElementById('reviewerName').value;
    const review = document.getElementById('reviewText').value;

    if (!productId) return alert('Please select a course');

    try {
        const response = await fetch(`${API_BASE}/review`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                product_id: parseInt(productId),
                name, review, rating: currentRating
            })
        });
        const data = await response.json();

        if (data.success) {
            // XSS VULNERABLE
            reviewsContainer.insertAdjacentHTML('afterbegin', `
                <div class="review-card">
                    <div class="review-header">
                        <span class="reviewer-name">${data.review.name}</span>
                        <span class="review-rating">${'*'.repeat(data.review.rating)}</span>
                    </div>
                    <p class="review-text">${data.review.review}</p>
                    <span class="review-date">Just now</span>
                </div>
            `);
            reviewForm.reset();
            currentRating = 5;
            updateRatingDisplay();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
