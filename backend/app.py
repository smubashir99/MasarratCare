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

#  PING (For Integration Testing)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

if __name__ == '__main__':
    app.run(debug=True)