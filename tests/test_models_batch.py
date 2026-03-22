import sys
sys.path.insert(0, 'backend')

from models import create_batch, verify_batch

# These tests assume the Flask app is running on http://
def test_create_batch():
    create_batch(1, "TEST-BATCH-999", 1)
    result = verify_batch("TEST-BATCH-999")
    assert result is not None

# This test checks if a genuine batch is verified correctly
def test_verify_genuine_batch():
    create_batch(1, "TEST-GENUINE-001", 1)
    result = verify_batch("TEST-GENUINE-001")
    assert result['is_genuine'] == 1

# This test checks if a fake batch is verified correctly
def test_verify_fake_batch():
    create_batch(1, "TEST-FAKE-001", 0)
    result = verify_batch("TEST-FAKE-001")
    assert result['is_genuine'] == 0

# This test checks if a non-existent batch is verified correctly
def test_verify_notfound_batch():
    result = verify_batch("NOTEXIST-999")
    assert result is None