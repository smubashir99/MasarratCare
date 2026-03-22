import requests

# These tests assume the Flask app is running on http://
def test_ping():
    res = requests.get('http://127.0.0.1:5000/ping')
    assert res.status_code == 200
    assert res.json()['message'] == 'pong'

# This test checks if the /products endpoint returns a list of products
def test_get_products():
    res = requests.get('http://127.0.0.1:5000/products')
    assert res.status_code == 200
    assert isinstance(res.json(), list)