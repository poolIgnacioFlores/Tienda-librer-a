from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True para ver cambios en caliente
    app.run(debug=True)
