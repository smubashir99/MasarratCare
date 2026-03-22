import sys
sys.path.insert(0, 'backend')

from models import create_product, get_all_products, delete_product

# These tests assume the Flask app is running on http://
def test_create_product():
    create_product("Test Lipstick", "lips", 999, "test")
    products = get_all_products()
    assert any(p['name'] == "Test Lipstick" for p in products)

# This test checks if the get_all_products function returns a list of products
def test_get_all_products():
    products = get_all_products()
    assert isinstance(products, list)
    assert len(products) > 0
    
# This test checks if a product can be deleted successfully
def test_delete_product():
    create_product("Delete Me", "test", 100, "temp")
    products = get_all_products()
    last_id = products[-1]['id']
    delete_product(last_id)
    after = get_all_products()
    assert all(p['id'] != last_id for p in after)