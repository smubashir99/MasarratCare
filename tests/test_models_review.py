import sys
sys.path.insert(0, 'backend')

from models import create_review, get_reviews_by_product, delete_review

# These tests assume the Flask app is running on http://
def test_create_review():
    create_review(1, "Ayesha", 5, "Amazing product!")
    reviews = get_reviews_by_product(1)
    assert any(r['reviewer'] == "Ayesha" for r in reviews)

# This test checks if the get_reviews_by_product function returns a list of reviews
def test_get_reviews():
    reviews = get_reviews_by_product(1)
    assert isinstance(reviews, list)

# This test checks if a review can be deleted successfully
def test_delete_review():
    create_review(1, "Temp User", 3, "okay")
    reviews = get_reviews_by_product(1)
    last_id = reviews[-1]['id']
    delete_review(last_id)
    after = get_reviews_by_product(1)
    assert all(r['id'] != last_id for r in after)