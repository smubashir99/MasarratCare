import sqlite3

def get_db():
    conn = sqlite3.connect("backend/medora.db")
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

    conn.commit()
    conn.close()