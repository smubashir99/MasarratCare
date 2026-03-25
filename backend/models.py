from db import get_db

#  PRODUCTS

def create_product(name, category, price, description):
    conn = get_db()
    conn.execute(
        "INSERT INTO products (name, category, price, description) VALUES (?,?,?,?)",
        [name, category, price, description]
    )
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_db()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_product(id, name, category, price, description):
    conn = get_db()
    conn.execute(
        "UPDATE products SET name=?, category=?, price=?, description=? WHERE id=?",
        [name, category, price, description, id]
    )
    conn.commit()
    conn.close()

def delete_product(id):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id=?", [id])
    conn.commit()
    conn.close()

#  SHADES

def create_shade(product_id, shade_name, hex_code):
    conn = get_db()
    conn.execute(
        "INSERT INTO shades (product_id, shade_name, hex_code) VALUES (?,?,?)",
        [product_id, shade_name, hex_code]
    )
    conn.commit()
    conn.close()

def get_shades_by_product(product_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM shades WHERE product_id=?", [product_id]
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_shade(id, shade_name, hex_code):
    conn = get_db()
    conn.execute(
        "UPDATE shades SET shade_name=?, hex_code=? WHERE id=?",
        [shade_name, hex_code, id]
    )
    conn.commit()
    conn.close()

def delete_shade(id):
    conn = get_db()
    conn.execute("DELETE FROM shades WHERE id=?", [id])
    conn.commit()
    conn.close()

#  BATCH CODES (Authenticity)

def create_batch(product_id, batch_code, is_genuine=1):
    conn = get_db()
    conn.execute(
        "INSERT INTO batch_codes (product_id, batch_code, is_genuine) VALUES (?,?,?)",
        [product_id, batch_code, is_genuine]
    )
    conn.commit()
    conn.close()

def verify_batch(batch_code):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM batch_codes WHERE batch_code=?", [batch_code]
    ).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

#  For admin dashboard - list all batch codes
def get_all_batches():
    conn = get_db()
    rows = conn.execute("SELECT * FROM batch_codes").fetchall()
    conn.close()
    return [dict(r) for r in rows]

#  For admin dashboard - update batch code info
def update_batch(id, batch_code, is_genuine):
    conn = get_db()
    conn.execute(
        "UPDATE batch_codes SET batch_code=?, is_genuine=? WHERE id=?",
        [batch_code, is_genuine, id]
    )
    conn.commit()
    conn.close()
    
#  For admin dashboard - delete batch code
def delete_batch(id):
    conn = get_db()
    conn.execute("DELETE FROM batch_codes WHERE id=?", [id])
    conn.commit()
    conn.close()

#  REVIEWS

def create_review(product_id, reviewer, rating, comment):
    conn = get_db()
    conn.execute(
        "INSERT INTO reviews (product_id, reviewer, rating, comment) VALUES (?,?,?,?)",
        [product_id, reviewer, rating, comment]
    )
    conn.commit()
    conn.close()

def get_reviews_by_product(product_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM reviews WHERE product_id=?", [product_id]
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_review(id):
    conn = get_db()
    conn.execute("DELETE FROM reviews WHERE id=?", [id])
    conn.commit()
    conn.close()

#  WISHLIST

def add_to_wishlist(product_id, user_name):
    conn = get_db()
    conn.execute(
        "INSERT INTO wishlist (product_id, user_name) VALUES (?,?)",
        [product_id, user_name]
    )
    conn.commit()
    conn.close()

def get_wishlist(user_name):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM wishlist WHERE user_name=?", [user_name]
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def remove_from_wishlist(id):
    conn = get_db()
    conn.execute("DELETE FROM wishlist WHERE id=?", [id])
    conn.commit()
    conn.close()