from __init__ import create_app
from extensions import db

# Crea la aplicación
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas definidas en los modelos
    app.run(debug=True)