"""SIDE B. SQLite product catalogue. Run 'python3 database.py' to initialise."""
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "side_b.db"


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialise_database():
    with connect() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                artist_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL CHECK(price >= 0),
                colour TEXT,
                image TEXT,
                stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0)
            );
            CREATE TABLE IF NOT EXISTS variants (
                id TEXT PRIMARY KEY,
                product_id INTEGER NOT NULL REFERENCES products(id),
                size TEXT,
                edition TEXT,
                fit TEXT,
                finish TEXT,
                option TEXT,
                stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0)
            );
        """)


def seed_products(artists):
    """Import sample products once; never overwrite later DB edits."""
    initialise_database()
    with connect() as db:
        if db.execute("SELECT COUNT(*) FROM products").fetchone()[0]:
            return False
        for artist in artists:
            for product in artist.get("merch", []):
                variants = product.get("variants", [])
                colours = {v["colour"] for v in variants if v.get("colour")}
                # Only a shared colour can be represented by one product.
                colour = product.get("colour") or (next(iter(colours)) if len(colours) == 1 else None)
                db.execute(
                    """INSERT INTO products
                       (id, artist_id, name, category, description, price, colour, image, stock)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (product["id"], artist["id"], product["name"], product["category"],
                     product.get("description", ""), product["price"], colour,
                     product.get("image", ""), product.get("stock", 0))
                )
                for variant in variants:
                    db.execute(
                        """INSERT INTO variants
                           (id, product_id, size, edition, fit, finish, option, stock)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (variant["id"], product["id"], variant.get("size"),
                         variant.get("edition"), variant.get("fit"),
                         variant.get("finish"), variant.get("option"), variant.get("stock", 0))
                    )
    return True


def load_products():
    """Return dictionaries compatible with the existing Flask templates/cart."""
    with connect() as db:
        products = [dict(row) for row in db.execute("SELECT * FROM products ORDER BY id")]
        for product in products:
            product["variants"] = [
                {key: value for key, value in dict(row).items() if value is not None and key != "product_id"}
                for row in db.execute("SELECT * FROM variants WHERE product_id = ? ORDER BY id", (product["id"],))
            ]
    return products
