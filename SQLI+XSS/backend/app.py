from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
import time

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootpassword'),
    'database': os.getenv('DB_NAME', 'healthyfood'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """Get database connection with retry logic"""
    max_retries = 30
    for i in range(max_retries):
        try:
            connection = pymysql.connect(**DB_CONFIG)
            return connection
        except pymysql.Error as e:
            if i < max_retries - 1:
                time.sleep(2)
            else:
                raise e

# ==========================================
# VULNERABLE ENDPOINTS - FOR SECURITY TESTING
# ==========================================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
        conn.close()
        return jsonify({'success': True, 'products': products})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_products():
    """
    VULNERABLE TO SQL INJECTION
    The query parameter is directly concatenated into the SQL query
    """
    query = request.args.get('q', '')
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # VULNERABLE: String concatenation in SQL query
            sql = f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
            cursor.execute(sql)
            products = cursor.fetchall()
        conn.close()
        
        # VULNERABLE TO XSS: Reflecting user input without sanitization
        return jsonify({
            'success': True, 
            'products': products,
            'search_term': query,  # Reflected XSS point
            'message': f'Found {len(products)} results for: {query}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """
    VULNERABLE TO SQL INJECTION
    Username and password are directly concatenated into the SQL query
    """
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # VULNERABLE: String concatenation allows authentication bypass
            sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            cursor.execute(sql)
            user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                'success': True,
                'message': f'Welcome back, {user["username"]}!',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    """Get reviews for a product - vulnerable to stored XSS"""
    product_id = request.args.get('product_id', 1)
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Using parameterized query here, but stored data may contain XSS
            cursor.execute("SELECT * FROM reviews WHERE product_id = %s ORDER BY created_at DESC", (product_id,))
            reviews = cursor.fetchall()
        conn.close()
        
        # Convert datetime to string for JSON serialization
        for review in reviews:
            if review.get('created_at'):
                review['created_at'] = review['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({'success': True, 'reviews': reviews})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/review', methods=['POST'])
def add_review():
    """
    VULNERABLE TO STORED XSS
    Review content is stored without sanitization and rendered on the frontend
    """
    data = request.get_json()
    product_id = data.get('product_id', 1)
    reviewer_name = data.get('name', 'Anonymous')
    review_text = data.get('review', '')
    rating = data.get('rating', 5)
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # VULNERABLE: Storing user input without sanitization
            # When this is rendered on the frontend, XSS will execute
            sql = "INSERT INTO reviews (product_id, reviewer_name, review_text, rating) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (product_id, reviewer_name, review_text, rating))
            conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Review added successfully!',
            'review': {
                'product_id': product_id,
                'name': reviewer_name,
                'review': review_text,  # Stored XSS payload
                'rating': rating
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    VULNERABLE TO SQL INJECTION
    User ID is directly concatenated into the query
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # VULNERABLE: Direct concatenation of user_id
            sql = f"SELECT id, username, email, role FROM users WHERE id = {user_id}"
            cursor.execute(sql)
            user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({'success': True, 'user': user})
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'ToyBox API is running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
