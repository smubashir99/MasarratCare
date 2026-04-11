from flask import Flask, jsonify, request
from flask_cors import CORS
from db import init_db, get_db
import os

# Frontend folder
frontend_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'frontend'
)

app = Flask(
    __name__,
    static_folder=frontend_folder,
    static_url_path=''
)
CORS(app)

#  AUTO SEED

def auto_seed():
    conn = get_db()
    existing = conn.execute(
        "SELECT COUNT(*) as count FROM products"
    ).fetchone()
    conn.close()

    if existing['count'] == 0:
        from models import (
            create_product, create_shade,
            create_batch, create_user
        )
        create_product("Masarrat Misbah Lip Gloss", "lips",  1800, "Long lasting glossy lip colour")
        create_product("MM Silk Foundation",         "face",  3500, "Lightweight silk finish foundation")
        create_product("MM Eye Shadow Palette",      "eyes",  2200, "12 shade eyeshadow palette")

        create_shade(1, "Rose Pink",   "#FF69B4")
        create_shade(1, "Coral Red",   "#FF4500")
        create_shade(1, "Nude Beige",  "#D4A574")
        create_shade(2, "Ivory Fair",  "#FFFFF0")
        create_shade(2, "Warm Sand",   "#C2956C")
        create_shade(2, "Deep Mocha",  "#8B4513")
        create_shade(3, "Smoky Brown", "#4A3728")
        create_shade(3, "Golden Nude", "#D4A843")
        create_shade(3, "Midnight",    "#191970")

        create_batch(1, "MM-LG-2024-001", 1)
        create_batch(1, "MM-LG-2024-002", 1)
        create_batch(1, "FAKE-001",        0)
        create_batch(2, "MM-SF-2024-001", 1)
        create_batch(2, "FAKE-002",        0)
        create_batch(3, "MM-ES-2024-001", 1)

        try:
            create_user('admin', 'admin123', 'admin')
            create_user('user1', 'user123',  'user')
        except:
            pass

        print("Auto seed done!")

init_db()
auto_seed()

#  INDEX ROUTE

@app.route('/')
def index():
    return app.send_static_file('index.html')

#  PRODUCTS ROUTES

from models import create_product, get_all_products, update_product, delete_product

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(get_all_products())

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    create_product(data['name'], data['category'], data['price'], data['description'])
    return jsonify({'message': 'Product created'}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def edit_product(id):
    data = request.get_json()
    update_product(id, data['name'], data['category'], data['price'], data['description'])
    return jsonify({'message': 'Product updated'})

@app.route('/products/<int:id>', methods=['DELETE'])
def remove_product(id):
    delete_product(id)
    return jsonify({'message': 'Product deleted'})


#  SHADES ROUTES

from models import create_shade, get_shades_by_product, update_shade, delete_shade

@app.route('/shades/<int:product_id>', methods=['GET'])
def get_shades(product_id):
    return jsonify(get_shades_by_product(product_id))

@app.route('/shades', methods=['POST'])
def add_shade():
    data = request.get_json()
    create_shade(data['product_id'], data['shade_name'], data['hex_code'])
    return jsonify({'message': 'Shade created'}), 201

@app.route('/shades/<int:id>', methods=['PUT'])
def edit_shade(id):
    data = request.get_json()
    update_shade(id, data['shade_name'], data['hex_code'])
    return jsonify({'message': 'Shade updated'})

@app.route('/shades/<int:id>', methods=['DELETE'])
def remove_shade(id):
    delete_shade(id)
    return jsonify({'message': 'Shade deleted'})


#  BATCH ROUTES

from models import create_batch, verify_batch, get_all_batches, update_batch, delete_batch

@app.route('/batch', methods=['POST'])
def add_batch():
    data = request.get_json()
    create_batch(data['product_id'], data['batch_code'], data.get('is_genuine', 1))
    return jsonify({'message': 'Batch code added'}), 201

@app.route('/batch/verify/<string:code>', methods=['GET'])
def check_batch(code):
    result = verify_batch(code)
    if result:
        status = 'GENUINE ✅' if result['is_genuine'] else 'FAKE ❌'
        return jsonify({'status': status, 'data': result})
    return jsonify({'status': 'NOT FOUND ❓'}), 404

@app.route('/batch', methods=['GET'])
def get_batches():
    return jsonify(get_all_batches())

@app.route('/batch/<int:id>', methods=['PUT'])
def edit_batch(id):
    data = request.get_json()
    update_batch(id, data['batch_code'], data['is_genuine'])
    return jsonify({'message': 'Batch updated'})

@app.route('/batch/<int:id>', methods=['DELETE'])
def remove_batch(id):
    delete_batch(id)
    return jsonify({'message': 'Batch deleted'})

#  REVIEWS ROUTES

from models import create_review, get_reviews_by_product, delete_review

@app.route('/reviews', methods=['GET'])
def get_all_reviews():
    from db import get_db
    conn = get_db()
    rows = conn.execute("""
        SELECT reviews.*, products.name as product_name
        FROM reviews
        LEFT JOIN products ON reviews.product_id = products.id
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/reviews/<int:product_id>', methods=['GET'])
def get_reviews(product_id):
    return jsonify(get_reviews_by_product(product_id))

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    create_review(data['product_id'], data['reviewer'], data['rating'], data['comment'])
    return jsonify({'message': 'Review added'}), 201

@app.route('/reviews/<int:id>', methods=['DELETE'])
def remove_review(id):
    delete_review(id)
    return jsonify({'message': 'Review deleted'})

#  WISHLIST ROUTES

from models import add_to_wishlist, get_wishlist, remove_from_wishlist

@app.route('/wishlist', methods=['GET'])
def get_all_wishlists():
    from db import get_db
    conn = get_db()
    rows = conn.execute("""
        SELECT wishlist.*, products.name as product_name
        FROM wishlist
        LEFT JOIN products ON wishlist.product_id = products.id
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/wishlist', methods=['POST'])
def add_wishlist():
    data = request.get_json()
    add_to_wishlist(data['product_id'], data['user_name'])
    return jsonify({'message': 'Added to wishlist'}), 201

@app.route('/wishlist/<int:id>', methods=['DELETE'])
def delete_wishlist(id):
    remove_from_wishlist(id)
    return jsonify({'message': 'Removed from wishlist'})

#  AUTH ROUTES

from models import create_user, get_user

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing = get_user(data['username'])
    if existing:
        return jsonify({'message': 'User already exists'}), 400
    create_user(data['username'], data['password'], data.get('role', 'user'))
    return jsonify({'message': 'User registered'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = get_user(data['username'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if user['password'] != data['password']:
        return jsonify({'message': 'Wrong password'}), 401
    return jsonify({'message': 'Login successful', 'username': user['username'], 'role': user['role']}), 200

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)