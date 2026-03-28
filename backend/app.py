from flask import Flask, jsonify, request
from flask_cors import CORS
from db import init_db
from models import (
    create_product, get_all_products, update_product, delete_product,
    create_shade, get_shades_by_product, update_shade, delete_shade,
    create_batch, verify_batch
)

app = Flask(__name__)
CORS(app)
init_db()

#  PRODUCTS ROUTES

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(get_all_products())

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    create_product(
        data['name'],
        data['category'],
        data['price'],
        data['description']
    )
    return jsonify({'message': 'Product created'}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def edit_product(id):
    data = request.get_json()
    update_product(
        id,
        data['name'],
        data['category'],
        data['price'],
        data['description']
    )
    return jsonify({'message': 'Product updated'})

@app.route('/products/<int:id>', methods=['DELETE'])
def remove_product(id):
    delete_product(id)
    return jsonify({'message': 'Product deleted'})

#  SHADES ROUTES

@app.route('/shades/<int:product_id>', methods=['GET'])
def get_shades(product_id):
    return jsonify(get_shades_by_product(product_id))

@app.route('/shades', methods=['POST'])
def add_shade():
    data = request.get_json()
    create_shade(
        data['product_id'],
        data['shade_name'],
        data['hex_code']
    )
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


#  BATCH / AUTHENTICITY ROUTES

@app.route('/batch', methods=['POST'])
def add_batch():
    data = request.get_json()
    create_batch(
        data['product_id'],
        data['batch_code'],
        data.get('is_genuine', 1)
    )
    return jsonify({'message': 'Batch code added'}), 201

@app.route('/batch/verify/<string:code>', methods=['GET'])
def check_batch(code):
    result = verify_batch(code)
    if result:
        status = 'GENUINE ✅' if result['is_genuine'] else 'FAKE ❌'
        return jsonify({'status': status, 'data': result})
    return jsonify({'status': 'NOT FOUND ❓'}), 404

#  ADMIN ROUTES FOR BATCH MANAGEMENT
@app.route('/batch', methods=['GET'])
def get_all_batches():
    from models import get_all_batches
    return jsonify(get_all_batches())

#  Admin can edit batch details (e.g., mark as fake/genuine)
@app.route('/batch/<int:id>', methods=['PUT'])
def edit_batch(id):
    data = request.get_json()
    from models import update_batch
    update_batch(id, data['batch_code'], data['is_genuine'])
    return jsonify({'message': 'Batch updated'})

#  Admin can delete a batch if needed
@app.route('/batch/<int:id>', methods=['DELETE'])
def remove_batch(id):
    from models import delete_batch
    delete_batch(id)
    return jsonify({'message': 'Batch deleted'})

#  PING (For Integration Testing)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

#  REVIEWS ROUTES

from models import create_review, get_reviews_by_product, delete_review

# Reviews are linked to products, so we fetch them by product ID
@app.route('/reviews/<int:product_id>', methods=['GET'])
def get_reviews(product_id):
    return jsonify(get_reviews_by_product(product_id))

# Adding a review requires product ID, reviewer name, rating, and comment
@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    create_review(
        data['product_id'],
        data['reviewer'],
        data['rating'],
        data['comment']
    )
    return jsonify({'message': 'Review added'}), 201

# Deleting a review is done by review ID, which is unique for each review
@app.route('/reviews/<int:id>', methods=['DELETE'])
def remove_review(id):
    delete_review(id)
    return jsonify({'message': 'Review deleted'})

# Admin route to view all reviews across products (for moderation purposes)
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

if __name__ == '__main__':
    app.run(debug=True)