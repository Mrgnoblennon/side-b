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
            CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                genre TEXT NOT NULL DEFAULT '',
                description TEXT NOT NULL DEFAULT '',
                biography TEXT NOT NULL DEFAULT '',
                image TEXT NOT NULL DEFAULT '',
                portrait TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS artist_gallery (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist_id INTEGER NOT NULL REFERENCES artists(id),
                image TEXT NOT NULL
            );
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
        artist_columns = {row["name"] for row in db.execute("PRAGMA table_info(artists)")}
        if "featured" not in artist_columns:
            db.execute("ALTER TABLE artists ADD COLUMN featured INTEGER NOT NULL DEFAULT 0")
            db.execute("UPDATE artists SET featured=1 WHERE id IN (SELECT id FROM artists ORDER BY id LIMIT 4)")
        for table in ("artists", "products"):
            columns = {row["name"] for row in db.execute(f"PRAGMA table_info({table})")}
            if "archived" not in columns:
                db.execute(f"ALTER TABLE {table} ADD COLUMN archived INTEGER NOT NULL DEFAULT 0")


def set_archived(kind, record_id, archived):
    if kind not in ("artists", "products"):
        raise ValueError("Invalid catalogue type.")
    with connect() as db:
        result = db.execute(f"UPDATE {kind} SET archived=? WHERE id=?", (int(bool(archived)), record_id))
        if result.rowcount != 1:
            raise LookupError("Catalogue entry not found.")


def list_categories():
    with connect() as db:
        return [row[0] for row in db.execute("SELECT DISTINCT category FROM products WHERE TRIM(category) != '' ORDER BY category COLLATE NOCASE")]


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
            product = db.execute("SELECT * FROM products WHERE id = ? AND archived=0 AND artist_id IN (SELECT id FROM artists WHERE archived=0)", (product_id,)).fetchone()
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


def load_products(include_archived=False):
    """Return dictionaries compatible with the existing Flask templates/cart."""
    with connect() as db:
        products = [dict(row) for row in db.execute("SELECT * FROM products ORDER BY id" if include_archived else "SELECT * FROM products WHERE archived=0 AND artist_id IN (SELECT id FROM artists WHERE archived=0) ORDER BY id")]
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


def update_product(product_id, fields, variant_stock):
    """Persist editable product fields and stock in a single transaction."""
    from decimal import Decimal, InvalidOperation
    try:
        name = fields["name"].strip()
        colour = fields["colour"].strip()
        image = fields.get("image", "").strip()
        price = Decimal(fields["price"])
        stock = int(fields["stock"])
        if not name or len(name) > 200 or len(colour) > 100 or not price.is_finite() or price < 0 or price > 999999 or price.as_tuple().exponent < -2 or stock < 0:
            raise ValueError
        parsed_variants = {str(key): int(value) for key, value in variant_stock.items()}
        if any(value < 0 for value in parsed_variants.values()):
            raise ValueError
    except (KeyError, ValueError, TypeError, InvalidOperation):
        raise ValueError("Enter a valid name, price (up to two decimals), and non-negative stock quantities.")
    with connect() as db:
        product = db.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
        if not product:
            raise LookupError("Product not found.")
        existing = {row["id"] for row in db.execute("SELECT id FROM variants WHERE product_id = ?", (product_id,))}
        if existing != set(parsed_variants):
            raise ValueError("Product options have changed. Refresh the page and try again.")
        db.execute("UPDATE products SET name = ?, colour = ?, price = ?, stock = ?, image = ? WHERE id = ?",
                   (name, colour, float(price), stock, image, product_id))
        for variant_id, quantity in parsed_variants.items():
            db.execute("UPDATE variants SET stock = ? WHERE id = ? AND product_id = ?",
                       (quantity, variant_id, product_id))


def seed_artists(catalogue):
    """One-time, non-destructive migration of existing artist dictionaries."""
    initialise_database()
    with connect() as db:
        for artist in catalogue:
            inserted = db.execute("""INSERT OR IGNORE INTO artists
                (id, name, slug, genre, description, biography, image, portrait)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (artist["id"], artist["name"], artist["slug"], artist.get("genre", ""),
                 artist.get("description", ""), artist.get("biography", ""),
                 artist.get("image", ""), artist.get("portrait", "")))
            if inserted.rowcount == 1 and artist["id"] in [item["id"] for item in catalogue[:4]]:
                db.execute("UPDATE artists SET featured=1 WHERE id=?", (artist["id"],))
            if inserted.rowcount == 1:
                db.executemany("INSERT INTO artist_gallery (artist_id, image) VALUES (?, ?)",
                               [(artist["id"], path) for path in artist.get("gallery", [])])


def load_artists(include_archived=False):
    with connect() as db:
        artists = [dict(row) for row in db.execute("SELECT * FROM artists ORDER BY id" if include_archived else "SELECT * FROM artists WHERE archived=0 ORDER BY id")]
        for artist in artists:
            artist["gallery"] = [row["image"] for row in db.execute(
                "SELECT image FROM artist_gallery WHERE artist_id = ? ORDER BY id", (artist["id"],))]
    return artists


def save_artist(fields, artist_id=None):
    name = fields.get("name", "").strip()
    slug = fields.get("slug", "").strip().lower()
    if not name or len(name) > 200 or not slug or len(slug) > 100 or not __import__("re").fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("Enter an artist name and a lowercase URL slug (letters, numbers and hyphens).")
    fields = dict(fields)
    fields["slug"] = slug
    for key in ("genre", "description", "biography"):
        if len(fields.get(key, "")) > 10000:
            raise ValueError("Artist text is too long.")
    featured = 1 if fields.get("featured") else 0
    with connect() as db:
        try:
            if artist_id is None:
                cursor = db.execute("""INSERT INTO artists
                    (name, slug, genre, description, biography, image, portrait, featured)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    tuple(fields.get(key, "").strip() for key in
                          ("name", "slug", "genre", "description", "biography", "image", "portrait")) + (featured,))
                artist_id = cursor.lastrowid
            else:
                if not db.execute("SELECT 1 FROM artists WHERE id = ?", (artist_id,)).fetchone():
                    raise LookupError("Artist not found.")
                db.execute("""UPDATE artists SET name=?, slug=?, genre=?, description=?,
                    biography=?, image=?, portrait=?, featured=? WHERE id=?""",
                    tuple(fields.get(key, "").strip() for key in
                          ("name", "slug", "genre", "description", "biography", "image", "portrait")) + (featured, artist_id))
            db.execute("DELETE FROM artist_gallery WHERE artist_id = ?", (artist_id,))
            db.executemany("INSERT INTO artist_gallery (artist_id, image) VALUES (?, ?)",
                           [(artist_id, path) for path in fields.get("gallery", [])])
        except sqlite3.IntegrityError:
            raise ValueError("That artist URL slug is already in use.")
    return artist_id


def create_product(fields):
    from decimal import Decimal, InvalidOperation
    try:
        artist_id = int(fields.get("artist_id", ""))
        name = fields.get("name", "").strip()
        category = fields.get("category", "").strip()
        price = Decimal(fields.get("price", ""))
        stock = int(fields.get("stock", ""))
        if not name or not category or len(name) > 200 or len(category) > 100 or len(fields.get("colour", "")) > 100 or len(fields.get("description", "")) > 10000 or not price.is_finite() or price < 0 or price > 999999 or price.as_tuple().exponent < -2 or stock < 0:
            raise ValueError
    except (ValueError, TypeError, InvalidOperation):
        raise ValueError("Enter a valid artist, name, category, price and non-negative stock.")
    with connect() as db:
        if not db.execute("SELECT 1 FROM artists WHERE id=?", (artist_id,)).fetchone():
            raise ValueError("Select a valid artist.")
        cursor = db.execute("""INSERT INTO products
            (artist_id, name, category, description, price, colour, image, stock)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (artist_id, name, category, fields.get("description", "").strip(),
             float(price), fields.get("colour", "").strip(), fields.get("image", ""), stock))
        return cursor.lastrowid


def add_product_variant(product_id, fields):
    """Add a stock-tracked option; retain existing variants for order history."""
    from uuid import uuid4
    try:
        stock = int(fields.get("stock", ""))
        if stock < 0:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError("Variant stock must be a non-negative whole number.")
    values = {key: fields.get(key, "").strip() for key in ("size", "edition", "fit", "finish", "option")}
    if not any(values.values()):
        raise ValueError("Enter at least one option, such as a size or edition.")
    if any(len(value) > 100 for value in values.values()):
        raise ValueError("Option values must be 100 characters or fewer.")
    with connect() as db:
        if not db.execute("SELECT 1 FROM products WHERE id=?", (product_id,)).fetchone():
            raise LookupError("Product not found.")
        existing = db.execute("SELECT size, edition, fit, finish, option FROM variants WHERE product_id=?", (product_id,)).fetchall()
        if any(all((row[key] or "") == values[key] for key in values) for row in existing):
            raise ValueError("This product option already exists.")
        variant_id = uuid4().hex
        db.execute("""INSERT INTO variants (id, product_id, size, edition, fit, finish, option, stock)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                   (variant_id, product_id, *(values[key] for key in values), stock))
        if not existing:
            db.execute("UPDATE products SET stock=0 WHERE id=?", (product_id,))
    return variant_id
