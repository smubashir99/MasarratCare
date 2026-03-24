import sys
sys.path.insert(0, 'backend')

from models import add_to_wishlist, get_wishlist, remove_from_wishlist

# These tests assume the Flask app is running on http://
def test_add_wishlist():
    add_to_wishlist(1, "Fatima")
    wishlist = get_wishlist("Fatima")
    assert any(w['user_name'] == "Fatima" for w in wishlist)

# This test checks if the get_wishlist function returns a list of wishlist items
def test_get_wishlist():
    wishlist = get_wishlist("Fatima")
    assert isinstance(wishlist, list)

# This test checks if a wishlist item can be removed successfully
def test_remove_wishlist():
    add_to_wishlist(1, "TempUser")
    wishlist = get_wishlist("TempUser")
    last_id = wishlist[-1]['id']
    remove_from_wishlist(last_id)
    after = get_wishlist("TempUser")
    assert all(w['id'] != last_id for w in after)