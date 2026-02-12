from app import create_app, db
from app.models import Category, Book, User

def upsert_category(slug, name):
    c = Category.query.filter_by(slug=slug).first()
    if not c:
        c = Category(slug=slug, name=name)
        db.session.add(c)
    else:
        c.name = name
    return c

def upsert_admin():
    email = "admin@pool.local"
    u = User.query.filter_by(email=email).first()
    if not u:
        u = User(email=email, name="Admin Pool", is_admin=True)
        u.set_password("admin123")
        db.session.add(u)
    else:
        u.is_admin = True
        u.name = "Admin Pool"
    return u

def add_book(title, author, price, stock, description, cover_url, category):
    exists = Book.query.filter_by(title=title, author=author).first()
    if exists:
        return
    b = Book(
        title=title,
        author=author,
        price=price,
        stock=stock,
        description=description,
        cover_url=cover_url,
        category_id=category.id
    )
    db.session.add(b)

def main():
    app = create_app()
    with app.app_context():
        db.create_all()

        shonen = upsert_category("shonen", "Shonen")
        seinen = upsert_category("seinen", "Seinen")
        shojo = upsert_category("shojo", "Shojo")
        artbook = upsert_category("artbook", "Artbooks")

        upsert_admin()

        # Covers: URLs de ejemplo (puedes cambiarlas)
        add_book(
            "Naruto Vol. 1",
            "Masashi Kishimoto",
            29.90,
            20,
            "El inicio de la historia de Naruto Uzumaki.",
            "https://images-na.ssl-images-amazon.com/images/I/81tA5XWzqzL.jpg",
            shonen
        )
        add_book(
            "One Piece Vol. 1",
            "Eiichiro Oda",
            32.90,
            15,
            "Luffy comienza su aventura para ser Rey de los Piratas.",
            "https://images-na.ssl-images-amazon.com/images/I/81gJ1x7DkVL.jpg",
            shonen
        )
        add_book(
            "Attack on Titan Vol. 1",
            "Hajime Isayama",
            34.90,
            12,
            "Una humanidad encerrada tras muros gigantes.",
            "https://images-na.ssl-images-amazon.com/images/I/91M9VaZWxOL.jpg",
            seinen
        )
        add_book(
            "Death Note Vol. 1",
            "Tsugumi Ohba",
            33.50,
            10,
            "Un cuaderno con el poder de matar con solo escribir un nombre.",
            "https://images-na.ssl-images-amazon.com/images/I/81OthjkJBuL.jpg",
            seinen
        )
        add_book(
            "Sailor Moon Vol. 1",
            "Naoko Takeuchi",
            30.00,
            9,
            "Magia, amistad y batallas épicas.",
            "https://images-na.ssl-images-amazon.com/images/I/81i2Uu7K6bL.jpg",
            shojo
        )
        add_book(
            "Studio Ghibli Artbook (Demo)",
            "Varios",
            59.90,
            6,
            "Un artbook de ejemplo para la tienda (demo).",
            "https://images-na.ssl-images-amazon.com/images/I/71z2KX7P3qL.jpg",
            artbook
        )

        db.session.commit()
        print("✅ BD lista y datos cargados (seed).")

if __name__ == "__main__":
    main()
