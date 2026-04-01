import sqlite3

def get_db():
    conn = sqlite3.connect("medora.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            category    TEXT,
            price       REAL,
            description TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS shades (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            shade_name TEXT NOT NULL,
            hex_code   TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    # Create batch_codes table to store unique batch codes for each product

    conn.execute("""
        CREATE TABLE IF NOT EXISTS batch_codes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            batch_code TEXT UNIQUE NOT NULL,
            is_genuine INTEGER DEFAULT 1,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    # Create reviews table to store user reviews for each product

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            reviewer   TEXT,
            rating     INTEGER,
            comment    TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # Create wishlist table to store user wishlists for products

    conn.execute("""
        CREATE TABLE IF NOT EXISTS wishlist (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            user_name  TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    # Create users table to store user credentials and roles
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role     TEXT DEFAULT 'user'
        )
    """)

    conn.commit()
    conn.close()