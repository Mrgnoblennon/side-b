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
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                suburb TEXT NOT NULL,
                total_cents INTEGER NOT NULL CHECK(total_cents >= 0),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL REFERENCES orders(id),
                product_id INTEGER NOT NULL REFERENCES products(id),
                variant_id TEXT REFERENCES variants(id),
                product_name TEXT NOT NULL,
                variant_label TEXT,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_price_cents INTEGER NOT NULL CHECK(unit_price_cents >= 0)
            );
        """)


def place_order(customer, cart):
    """Validate stock and write an order atomically. Returns its new ID."""
    from decimal import Decimal
    if not cart:
        raise ValueError("Your cart is empty.")
    with connect() as db:
        db.execute("BEGIN IMMEDIATE")
        lines = []
        for entry in cart:
            try:
                product_id = int(entry["product_id"])
                quantity = int(entry["quantity"])
            except (ValueError, TypeError, KeyError):
                raise ValueError("Invalid cart item.")
            product = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if not product or quantity < 1:
                raise ValueError("An item in your cart is unavailable.")
            variant_id = entry.get("variant_id") or None
            variant = db.execute("SELECT * FROM variants WHERE id = ? AND product_id = ?",
                                 (variant_id, product_id)).fetchone() if variant_id else None
            has_variants = db.execute("SELECT 1 FROM variants WHERE product_id = ? LIMIT 1", (product_id,)).fetchone()
            if has_variants and not variant:
                raise ValueError("Please choose a valid product option.")
            stock = variant["stock"] if variant else product["stock"]
            if quantity > stock:
                raise ValueError(f"Not enough stock for {product['name']}.")
            label = " · ".join(str(variant[k]) for k in ("size", "edition", "fit", "finish", "option") if variant and variant[k])
            cents = int(Decimal(str(product["price"])) * 100)
            lines.append((product, variant_id, label, quantity, cents))
        # Aggregate quantities for duplicate cart entries before stock changes.
        counts = {}
        for product, variant_id, _, quantity, _ in lines:
            key = (product["id"], variant_id)
            counts[key] = counts.get(key, 0) + quantity
        for (product_id, variant_id), quantity in counts.items():
            if variant_id:
                result = db.execute("UPDATE variants SET stock = stock - ? WHERE id = ? AND product_id = ? AND stock >= ?",
                                    (quantity, variant_id, product_id, quantity))
            else:
                result = db.execute("UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?",
                                    (quantity, product_id, quantity))
            if result.rowcount != 1:
                raise ValueError("Stock changed. Please review your cart.")
        total = sum(quantity * cents for _, _, _, quantity, cents in lines)
        cursor = db.execute("INSERT INTO orders (customer_name, email, phone, suburb, total_cents) VALUES (?, ?, ?, ?, ?)",
                            (customer["name"], customer["email"], customer["phone"], customer["suburb"], total))
        order_id = cursor.lastrowid
        for product, variant_id, label, quantity, cents in lines:
            db.execute("""INSERT INTO order_items
                (order_id, product_id, variant_id, product_name, variant_label, quantity, unit_price_cents)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (order_id, product["id"], variant_id, product["name"], label, quantity, cents))
    return order_id


def load_order(order_id):
    with connect() as db:
        order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if not order:
            return None, []
        items = [dict(row) for row in db.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))]
    return dict(order), items


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


def list_orders():
    """Newest orders first, with a count of purchased items."""
    with connect() as db:
        return [dict(row) for row in db.execute("""
            SELECT o.*, COALESCE(SUM(oi.quantity), 0) AS item_count
            FROM orders AS o
            LEFT JOIN order_items AS oi ON oi.order_id = o.id
            GROUP BY o.id
            ORDER BY o.id DESC
        """)]


def order_stats():
    with connect() as db:
        row = db.execute("""
            SELECT COUNT(*) AS order_count,
                   COALESCE(SUM(total_cents), 0) AS revenue_cents
            FROM orders
        """).fetchone()
        return dict(row)
