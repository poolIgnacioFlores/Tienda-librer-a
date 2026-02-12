from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..models import Book, Category
from .. import db

admin_bp = Blueprint("admin", __name__)

def admin_required():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)

@admin_bp.get("/")
@login_required
def dashboard():
    admin_required()
    books_count = Book.query.count()
    categories_count = Category.query.count()
    return render_template("admin/dashboard.html", books_count=books_count, categories_count=categories_count)

@admin_bp.get("/books")
@login_required
def books():
    admin_required()
    books = Book.query.order_by(Book.id.desc()).all()
    return render_template("admin/books_list.html", books=books)

@admin_bp.route("/books/new", methods=["GET", "POST"])
@login_required
def books_new():
    admin_required()
    categories = Category.query.order_by(Category.name.asc()).all()

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        author = (request.form.get("author") or "").strip()
        price = float(request.form.get("price") or 0)
        stock = int(request.form.get("stock") or 0)
        description = (request.form.get("description") or "").strip()
        cover_url = (request.form.get("cover_url") or "").strip()
        category_id = int(request.form.get("category_id") or 0)

        if not title or not author or price <= 0 or category_id <= 0:
            flash("Completa título, autor, precio y categoría.", "danger")
            return redirect(url_for("admin.books_new"))

        book = Book(
            title=title, author=author, price=price, stock=stock,
            description=description, cover_url=cover_url, category_id=category_id
        )
        db.session.add(book)
        db.session.commit()

        flash("Libro creado.", "success")
        return redirect(url_for("admin.books"))

    return render_template("admin/books_form.html", mode="new", categories=categories, book=None)

@admin_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def books_edit(book_id):
    admin_required()
    book = Book.query.get_or_404(book_id)
    categories = Category.query.order_by(Category.name.asc()).all()

    if request.method == "POST":
        book.title = (request.form.get("title") or "").strip()
        book.author = (request.form.get("author") or "").strip()
        book.price = float(request.form.get("price") or 0)
        book.stock = int(request.form.get("stock") or 0)
        book.description = (request.form.get("description") or "").strip()
        book.cover_url = (request.form.get("cover_url") or "").strip()
        book.category_id = int(request.form.get("category_id") or book.category_id)

        if not book.title or not book.author or book.price <= 0:
            flash("Título, autor y precio son obligatorios.", "danger")
            return redirect(url_for("admin.books_edit", book_id=book_id))

        db.session.commit()
        flash("Libro actualizado.", "success")
        return redirect(url_for("admin.books"))

    return render_template("admin/books_form.html", mode="edit", categories=categories, book=book)

@admin_bp.post("/books/<int:book_id>/delete")
@login_required
def books_delete(book_id):
    admin_required()
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Libro eliminado.", "info")
    return redirect(url_for("admin.books"))
