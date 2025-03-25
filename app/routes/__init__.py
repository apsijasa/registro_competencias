from flask import Flask
from config import Config
from extensions import db, csrf

def create_app(config_class=Config):
    # Crea la aplicación Flask
    app = Flask(__name__)
    
    # Carga la configuración
    app.config.from_object(config_class)
    
    # Inicializa las extensiones
    db.init_app(app)
    csrf.init_app(app)
    
    # Importa rutas DENTRO de la función para evitar importaciones circulares
    from routes import init_routes
    
    # Inicializa las rutas
    init_routes(app)
    
    return app