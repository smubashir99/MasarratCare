from db import init_db, get_db
from models import create_product, create_shade

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

    #  SHADES

    create_shade(1, "Rose Pink",   "#FF69B4")
    create_shade(1, "Coral Red",   "#FF4500")
    create_shade(1, "Nude Beige",  "#D4A574")

    create_shade(2, "Ivory Fair",  "#FFFFF0")
    create_shade(2, "Warm Sand",   "#C2956C")
    create_shade(2, "Deep Mocha",  "#8B4513")

    create_shade(3, "Smoky Brown", "#4A3728")
    create_shade(3, "Golden Nude", "#D4A843")
    create_shade(3, "Midnight",    "#191970")

    print("shades seeded!")

if __name__ == '__main__':
    seed()