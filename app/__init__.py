"""
Inicialización de la aplicación Flask.
Este módulo configura la aplicación Flask y sus extensiones.
"""
import os
from flask import Flask
from app.config import Config
from app.extensions import db, csrf, mail
from app.utils.security import init_security_headers
from flask import Flask, render_template
from app.utils.context import init_template_context

def create_app(config_class=Config):
    """
    Factory function para crear la instancia de la aplicación Flask.
    """
    # Crea la aplicación Flask
    app = Flask(__name__)
    
    # Carga la configuración
    app.config.from_object(config_class)
    
    # Inicializa las extensiones
    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    
    # Inicializa encabezados de seguridad
    init_security_headers(app)
    
    # Añade esta línea para inicializar el contexto de plantillas
    init_template_context(app)
    
    # Registra los blueprints
    from app.routes import init_routes
    init_routes(app)
    
    # Registra los manejadores de errores
    register_error_handlers(app)
    
    # Crear las tablas de la base de datos si no existen
    with app.app_context():
        db.create_all()
    
    return app

def register_error_handlers(app):
    """
    Registra los manejadores para páginas de error.
    """
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Añade estos dos manejadores
    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('errors/401.html'), 401
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

def register_error_handlers(app):
    """
    Registra los manejadores para páginas de error.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
        
    from flask import render_template