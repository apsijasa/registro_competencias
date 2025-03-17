from __init__ import app

if __name__ == '__main__':
    with app.app_context():
        from __init__ import db
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)