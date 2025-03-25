"""
Inicialización y registro de rutas de la aplicación.
"""
from flask import Blueprint

# Importar todos los módulos de rutas
from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.analysis import analysis_bp
from app.routes.api import api_bp

def init_routes(app):
    """
    Registra todos los blueprints de rutas en la aplicación.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(analysis_bp, url_prefix='/analysis')
    app.register_blueprint(api_bp, url_prefix='/api')