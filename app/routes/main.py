from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from ..models import Book, Category, Order, OrderItem
from .. import db

main_bp = Blueprint("main", __name__)

def _cart():
    # cart en session: {book_id: qty}
    return session.setdefault("cart", {})

@main_bp.get("/")
def home():
    featured = Book.query.limit(6).all()
    categories = Category.query.all()
    return render_template("home.html", featured=featured, categories=categories)

@main_bp.get("/catalog")
def catalog():
    books = Book.query.order_by(Book.id.desc()).all()
    categories = Category.query.all()
    return render_template("catalog.html", books=books, categories=categories, active_category=None)

@main_bp.get("/category/<slug>")
def by_category(slug):
    cat = Category.query.filter_by(slug=slug).first_or_404()
    books = Book.query.filter_by(category_id=cat.id).all()
    categories = Category.query.all()
    return render_template("catalog.html", books=books, categories=categories, active_category=cat)

@main_bp.get("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book_detail.html", book=book)

@main_bp.get("/search")
def search():
    q = (request.args.get("q") or "").strip()
    if not q:
        flash("Escribe algo para buscar 😊", "warning")
        return redirect(url_for("main.catalog"))
    books = Book.query.filter(Book.title.ilike(f"%{q}%")).all()
    return render_template("search.html", q=q, books=books)

@main_bp.get("/about")
def about():
    return render_template("about.html")

@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        message = (request.form.get("message") or "").strip()
        if not name or not message:
            flash("Completa tu nombre y el mensaje.", "danger")
            return redirect(url_for("main.contact"))
        # No enviamos email de verdad (es demo). Solo confirmamos.
        flash("Mensaje enviado (demo). ¡Gracias!", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html")

# --- CART ---
@main_bp.get("/cart")
def cart_view():
    cart = _cart()
    book_ids = [int(k) for k in cart.keys()]
    books = Book.query.filter(Book.id.in_(book_ids)).all() if book_ids else []
    items = []
    total = 0.0
    book_map = {b.id: b for b in books}
    for book_id_str, qty in cart.items():
        book_id = int(book_id_str)
        book = book_map.get(book_id)
        if not book:
            continue
        line = book.price * int(qty)
        total += line
        items.append({"book": book, "qty": int(qty), "line": line})
    return render_template("cart.html", items=items, total=total)

@main_bp.post("/cart/add/<int:book_id>")
def cart_add(book_id):
    book = Book.query.get_or_404(book_id)
    cart = _cart()
    current = int(cart.get(str(book_id), 0))
    cart[str(book_id)] = current + 1
    session.modified = True
    flash(f"Agregado: {book.title}", "success")
    return redirect(request.referrer or url_for("main.catalog"))

@main_bp.post("/cart/remove/<int:book_id>")
def cart_remove(book_id):
    cart = _cart()
    cart.pop(str(book_id), None)
    session.modified = True
    flash("Producto removido del carrito.", "info")
    return redirect(url_for("main.cart_view"))

@main_bp.post("/cart/clear")
def cart_clear():
    session["cart"] = {}
    session.modified = True
    flash("Carrito limpiado.", "info")
    return redirect(url_for("main.cart_view"))

# --- CHECKOUT (fake) ---
@main_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = _cart()
    if not cart:
        flash("Tu carrito está vacío.", "warning")
        return redirect(url_for("main.catalog"))

    book_ids = [int(k) for k in cart.keys()]
    books = Book.query.filter(Book.id.in_(book_ids)).all()

    items = []
    total = 0.0
    book_map = {b.id: b for b in books}
    for book_id_str, qty in cart.items():
        book_id = int(book_id_str)
        book = book_map.get(book_id)
        if not book:
            continue
        qty_int = int(qty)
        line = book.price * qty_int
        total += line
        items.append((book, qty_int, line))

    if request.method == "POST":
        full_name = (request.form.get("full_name") or "").strip()
        address = (request.form.get("address") or "").strip()
        if not full_name or not address:
            flash("Completa tu nombre y dirección.", "danger")
            return redirect(url_for("main.checkout"))

        order = Order(full_name=full_name, address=address, total=total, user_id=current_user.id)
        db.session.add(order)
        db.session.flush()  # para tener order.id

        for book, qty_int, _line in items:
            order_item = OrderItem(
                book_title=book.title,
                unit_price=book.price,
                quantity=qty_int,
                order_id=order.id
            )
            db.session.add(order_item)

        db.session.commit()

        session["cart"] = {}
        session.modified = True

        flash(f"Compra registrada (demo). Pedido #{order.id}", "success")
        return redirect(url_for("main.order_detail", order_id=order.id))

    return render_template("checkout.html", items=items, total=total)

@main_bp.get("/orders")
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    return render_template("orders.html", orders=orders)

@main_bp.get("/orders/<int:order_id>")
@login_required
def order_detail(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template("order_detail.html", order=order)
