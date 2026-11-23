# import flask class
from flask import Flask, render_template, url_for, request, abort, session, redirect, flash
import os
import hmac
import secrets
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename
from database import initialise_database, seed_products, load_products, place_order, load_order, list_orders, order_stats, update_product, seed_artists, load_artists, save_artist, create_product

# initialise flask application
app = Flask(__name__)
# Set SIDE_B_SECRET_KEY in production to keep carts valid across restarts.
app.secret_key = os.environ.get('SIDE_B_SECRET_KEY', 'side-b-local-development-only')


from seed_data import artists as sample_artists

@app.route("/")
# define route function that will handle reququests
def home():
    # sends a response back to the browser
    catalogue = load_artists()
    products = get_products()
    for artist in catalogue:
        artist["merch"] = [p for p in products if p["artist_id"] == artist["id"]]
    return render_template("index.html", artists=catalogue)


@app.route("/artists")
def artists_page():
    return render_template("artists.html", artists=load_artists())


@app.route("/artists/<slug>")
def artist_page(slug):

    # Find the artist matching the URL slug
    for artist in load_artists():
        if artist["slug"] == slug:
            artist["merch"] = [p for p in get_products() if p["artist_id"] == artist["id"]]
            return render_template("artist.html", artist=artist)

    return "Artist not found", 404


# Initialise and seed the SQLite catalogue on first startup only.
initialise_database()
seed_products(sample_artists)
seed_artists(sample_artists)


def get_products():
    products = load_products()
    artist_names = {artist["id"]: artist["name"] for artist in load_artists()}
    for product in products:
        product["artist"] = artist_names.get(product["artist_id"], "Unknown Artist")
    return products


# merch shop page
@app.route("/shop")
def merch_shop():
    products = get_products()
    categories = sorted(set(p["category"] for p in products))
    artist_names = sorted(set(p["artist"] for p in products))
    selected_category = request.args.get("category", "All")
    selected_artist = request.args.get("artist", "All")
    selected_sort = request.args.get("sort", "default")

    if selected_category not in categories:
        selected_category = "All"
    if selected_artist not in artist_names:
        selected_artist = "All"
    if selected_sort not in ("default", "price_asc", "price_desc", "name_asc"):
        selected_sort = "default"

    if selected_category != "All":
        products = [p for p in products if p["category"] == selected_category]
    if selected_artist != "All":
        products = [p for p in products if p["artist"] == selected_artist]

    if selected_sort == "price_asc":
        products.sort(key=lambda p: float(p["price"]))
    elif selected_sort == "price_desc":
        products.sort(key=lambda p: float(p["price"]), reverse=True)
    elif selected_sort == "name_asc":
        products.sort(key=lambda p: p["name"].casefold())

    return render_template("shop.html", products=products, categories=categories,
                           artist_names=artist_names, selected_category=selected_category,
                           selected_artist=selected_artist, selected_sort=selected_sort)

# individual product page
@app.route("/shop/<int:product_id>")
def product_detail(product_id):
    products = get_products()

    # find the product using its id
    product = next(
        (product for product in products if str(product.get("id")) == str(product_id)),
        None,
    )

    print("PRODUCT IDS:", [product.get("id") for product in products])

    if product is None:
        abort(404)

    # get other products from the same artist
    related_products = [
        item
        for item in products
        if item["artist"] == product["artist"]
        and str(item.get("id")) != str(product_id)
    ][:4]

    return render_template(
        "product.html",
        product=product,
        related_products=related_products
    )


# Cart stores only IDs and quantities; product details come from the catalogue.
def cart_details():
    catalogue = {str(p["id"]): p for p in get_products()}
    items = []
    subtotal = 0.0
    for entry in session.get("cart", []):
        product = catalogue.get(str(entry.get("product_id")))
        if not product:
            continue
        variant = next((v for v in product.get("variants", []) if str(v["id"]) == str(entry.get("variant_id"))), None)
        if product.get("variants") and variant is None:
            continue
        stock = int(variant["stock"] if variant else product.get("stock", 0))
        quantity = min(max(1, int(entry.get("quantity", 1))), stock)
        if stock <= 0:
            continue
        price = float(product["price"])
        subtotal += price * quantity
        label = " · ".join(str(variant[k]) for k in ("size", "colour", "edition", "fit", "finish", "option") if variant and variant.get(k))
        items.append({"product": product, "variant": variant, "variant_label": label,
                      "quantity": quantity, "stock": stock, "line_total": price * quantity,
                      "variant_id": entry.get("variant_id", "")})
    return items, round(subtotal, 2)


@app.route("/cart")
def view_cart():
    items, subtotal = cart_details()
    return render_template("cart.html", items=items, subtotal=subtotal)


@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id", "")
    variant_id = request.form.get("variant", "")
    product = next((p for p in get_products() if str(p["id"]) == product_id), None)
    if not product:
        abort(404)
    variant = next((v for v in product.get("variants", []) if str(v["id"]) == variant_id), None)
    if product.get("variants") and variant is None:
        flash("Please select a valid option.")
        return redirect(url_for("product_detail", product_id=product["id"]))
    try:
        quantity = int(request.form.get("quantity", "1"))
    except ValueError:
        quantity = 0
    stock = int(variant["stock"] if variant else product.get("stock", 0))
    cart = list(session.get("cart", []))
    existing = next((item for item in cart if str(item["product_id"]) == product_id and str(item.get("variant_id", "")) == variant_id), None)
    current = int(existing["quantity"]) if existing else 0
    if quantity < 1 or current + quantity > stock:
        flash("Invalid quantity or not enough stock available.")
        return redirect(url_for("product_detail", product_id=product["id"]))
    if existing:
        existing["quantity"] += quantity
    else:
        cart.append({"product_id": product_id, "variant_id": variant_id, "quantity": quantity})
    session["cart"] = cart
    flash("Added to cart.")
    return redirect(url_for("view_cart"))


@app.route("/cart/update", methods=["POST"])
def update_cart():
    product_id = request.form.get("product_id", "")
    variant_id = request.form.get("variant_id", "")
    product = next((p for p in get_products() if str(p["id"]) == product_id), None)
    if not product:
        abort(404)
    variant = next((v for v in product.get("variants", []) if str(v["id"]) == variant_id), None)
    if product.get("variants") and variant is None:
        abort(400)
    try:
        quantity = int(request.form.get("quantity", "0"))
    except ValueError:
        quantity = -1
    stock = int(variant["stock"] if variant else product.get("stock", 0))
    cart = list(session.get("cart", []))
    matching = [item for item in cart if str(item["product_id"]) == product_id and str(item.get("variant_id", "")) == variant_id]
    if not matching:
        abort(404)
    if quantity == 0:
        cart = [item for item in cart if item not in matching]
    elif 1 <= quantity <= stock:
        matching[0]["quantity"] = quantity
    else:
        flash("Quantity must be between 1 and available stock.")
        return redirect(url_for("view_cart"))
    session["cart"] = cart
    return redirect(url_for("view_cart"))


# Simulated checkout: no payment details are collected.
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, subtotal = cart_details()
    if not session.get("cart") or not items:
        flash("Add something to your cart before checking out.")
        return redirect(url_for("view_cart"))
    if request.method == "POST":
        customer = {key: request.form.get(key, "").strip() for key in ("name", "email", "phone", "suburb")}
        if any(not value or len(value) > 200 for value in customer.values()) or "@" not in customer["email"]:
            flash("Please enter valid contact details.")
        else:
            try:
                order_id = place_order(customer, session["cart"])
            except ValueError as exc:
                flash(str(exc))
                return redirect(url_for("view_cart"))
            session.pop("cart", None)
            session["last_order_id"] = order_id
            return redirect(url_for("order_confirmation", order_id=order_id))
    return render_template("checkout.html", items=items, subtotal=subtotal)


@app.route("/order/<int:order_id>")
def order_confirmation(order_id):
    if session.get("last_order_id") != order_id:
        abort(404)
    order, items = load_order(order_id)
    if not order:
        abort(404)
    return render_template("order_confirmation.html", order=order, items=items)



# Admin access is disabled until SIDE_B_ADMIN_PASSWORD is configured.
def admin_authenticated():
    return bool(os.environ.get("SIDE_B_ADMIN_PASSWORD")) and session.get("admin_authenticated") is True


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if admin_authenticated():
        return redirect(url_for("admin_orders"))
    configured_password = os.environ.get("SIDE_B_ADMIN_PASSWORD", "")
    if request.method == "POST":
        supplied = request.form.get("password", "")
        if configured_password and hmac.compare_digest(supplied, configured_password):
            session.clear()
            session["admin_authenticated"] = True
            session["admin_csrf"] = secrets.token_urlsafe(32)
            return redirect(url_for("admin_orders"))
        flash("Incorrect password, or admin access has not been configured.")
    return render_template("admin_login.html", configured=bool(configured_password))


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    if not admin_authenticated():
        abort(403)
    if not hmac.compare_digest(request.form.get("csrf_token", ""), session.get("admin_csrf", "")):
        abort(403)
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin/orders")
def admin_orders():
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    return render_template("admin_orders.html", orders=list_orders(), stats=order_stats())


@app.route("/admin/orders/<int:order_id>")
def admin_order_detail(order_id):
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    order, items = load_order(order_id)
    if not order:
        abort(404)
    return render_template("admin_order_detail.html", order=order, items=items)



@app.route("/admin/products")
def admin_products():
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    products = get_products()
    for product in products:
        product["available_stock"] = sum(int(v["stock"]) for v in product["variants"]) if product["variants"] else int(product["stock"])
    query = request.args.get("q", "").strip()
    if query:
        products = [p for p in products if query.casefold() in p["name"].casefold() or query.casefold() in p["artist"].casefold()]
    return render_template("admin_products.html", products=products, query=query)


@app.route("/admin/products/<int:product_id>/edit", methods=["GET", "POST"])
def admin_edit_product(product_id):
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    product = next((p for p in get_products() if p["id"] == product_id), None)
    if product is None:
        abort(404)
    if request.method == "POST":
        if not hmac.compare_digest(request.form.get("csrf_token", ""), session.get("admin_csrf", "")):
            abort(403)
        fields = {key: request.form.get(key, "") for key in ("name", "colour", "price", "stock")}
        variant_stock = {str(v["id"]): request.form.get("stock_" + str(v["id"]), "") for v in product["variants"]}
        try:
            update_product(product_id, fields, variant_stock)
        except ValueError as exc:
            flash(str(exc))
        else:
            flash("Product updated successfully.")
            return redirect(url_for("admin_edit_product", product_id=product_id))
    return render_template("admin_edit_product.html", product=product)



# Images are saved as files, not database blobs. Only image types are accepted.
UPLOAD_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024


def store_image(upload, existing=""):
    if not upload or not upload.filename:
        return existing
    extension = Path(secure_filename(upload.filename)).suffix.lower()
    if extension not in UPLOAD_EXTENSIONS:
        raise ValueError("Upload a JPG, PNG, WebP or GIF image.")
    header = upload.stream.read(32)
    upload.stream.seek(0)
    valid = (header.startswith(bytes.fromhex("ffd8ff")) and extension in {".jpg", ".jpeg"}) or (
        header.startswith(bytes.fromhex("89504e470d0a1a0a")) and extension == ".png") or (
        header.startswith((b"GIF87a", b"GIF89a")) and extension == ".gif") or (
        header.startswith(b"RIFF") and header[8:12] == b"WEBP" and extension == ".webp")
    if not valid:
        raise ValueError("That file is not a recognised image.")
    folder = Path(app.static_folder) / "images" / "uploads"
    folder.mkdir(parents=True, exist_ok=True)
    filename = uuid4().hex + extension
    upload.save(folder / filename)
    return "images/uploads/" + filename


@app.route("/admin/artists")
def admin_artists():
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    return render_template("admin_artists.html", artists=load_artists())


@app.route("/admin/artists/new", methods=["GET", "POST"])
@app.route("/admin/artists/<int:artist_id>/edit", methods=["GET", "POST"])
def admin_artist_form(artist_id=None):
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    artist = next((a for a in load_artists() if a["id"] == artist_id), None)
    if artist_id is not None and artist is None:
        abort(404)
    if request.method == "POST":
        if not hmac.compare_digest(request.form.get("csrf_token", ""), session.get("admin_csrf", "")):
            abort(403)
        try:
            fields = {key: request.form.get(key, "") for key in
                      ("name", "slug", "genre", "description", "biography")}
            fields["image"] = store_image(request.files.get("image"), artist["image"] if artist else "")
            fields["portrait"] = store_image(request.files.get("portrait"), artist["portrait"] if artist else "")
            gallery = list(artist["gallery"]) if artist else []
            gallery.extend(store_image(upload) for upload in request.files.getlist("gallery") if upload.filename)
            fields["gallery"] = gallery
            saved_id = save_artist(fields, artist_id)
        except ValueError as exc:
            flash(str(exc))
        else:
            flash("Artist saved.")
            return redirect(url_for("admin_artist_form", artist_id=saved_id))
    return render_template("admin_artist_form.html", artist=artist)


@app.route("/admin/products/new", methods=["GET", "POST"])
def admin_new_product():
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        if not hmac.compare_digest(request.form.get("csrf_token", ""), session.get("admin_csrf", "")):
            abort(403)
        try:
            fields = {key: request.form.get(key, "") for key in
                      ("artist_id", "name", "category", "description", "price", "colour", "stock")}
            fields["image"] = store_image(request.files.get("image"))
            product_id = create_product(fields)
        except ValueError as exc:
            flash(str(exc))
        else:
            flash("Product created.")
            return redirect(url_for("admin_edit_product", product_id=product_id))
    return render_template("admin_new_product.html", artists=load_artists())


# runs when everything before it is correct
if __name__ == "__main__":
    # starts the server
    app.run(debug=True, port=5001)
