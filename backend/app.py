from flask import Flask, jsonify, request
from flask_cors import CORS
from db import init_db
from models import (
    create_product, get_all_products, update_product, delete_product
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

#  PING (For Integration Testing)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

if __name__ == '__main__':
    app.run(debug=True)