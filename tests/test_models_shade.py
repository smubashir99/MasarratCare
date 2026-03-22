import sys
sys.path.insert(0, 'backend')

from models import create_shade, get_shades_by_product, delete_shade

# These tests assume the Flask app is running on http://
def test_create_shade():
    create_shade(1, "Test Shade", "#123456")
    shades = get_shades_by_product(1)
    assert any(s['shade_name'] == "Test Shade" for s in shades)

# This test checks if the get_shades_by_product function returns a list of shades for a given product
def test_get_shades_by_product():
    shades = get_shades_by_product(1)
    assert isinstance(shades, list)

# This test checks if a shade can be deleted successfully
def test_delete_shade():
    create_shade(1, "Temp Shade", "#FFFFFF")
    shades = get_shades_by_product(1)
    last_id = shades[-1]['id']
    delete_shade(last_id)
    after = get_shades_by_product(1)
    assert all(s['id'] != last_id for s in after)