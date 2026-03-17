from db import init_db, get_db
from models import create_product

# This script is used to seed the database with initial data for testing and development purposes.

def seed():
    init_db()
    conn = get_db()

    # First remove old data to avoid duplicates when running seed multiple times

    conn.execute("DELETE FROM batch_codes")
    conn.execute("DELETE FROM shades")
    conn.execute("DELETE FROM products")
    conn.commit()
    conn.close()

    #  PRODUCTS

    create_product(
        "Masarrat Misbah Lip Gloss",
        "lips",
        1800,
        "Long lasting glossy lip colour"
    )
    create_product(
        "MM Silk Foundation",
        "face",
        3500,
        "Lightweight silk finish foundation"
    )
    create_product(
        "MM Eye Shadow Palette",
        "eyes",
        2200,
        "12 shade eyeshadow palette"
    )

    print("products seeded!")

if __name__ == '__main__':
    seed()