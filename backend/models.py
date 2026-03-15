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