from flask import Flask, jsonify, request
from flask_cors import CORS
from db import init_db

app = Flask(__name__)
CORS(app)
init_db()

#  PING (For Integration Testing)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

if __name__ == '__main__':
    app.run(debug=True)