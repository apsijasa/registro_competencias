"""
Configuración de la aplicación Flask.
Este módulo define las clases de configuración para diferentes entornos.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Directorio base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    """Configuración base para todos los entornos."""
    
    # Clave secreta para sesiones y tokens CSRF (cargar desde variable de entorno)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambiar-esta-clave-en-produccion'
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(BASE_DIR, "swim_analysis.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de seguridad
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de correo electrónico
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'False').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Opciones de seguridad para encriptación
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or SECRET_KEY

class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Configuración para entorno de producción."""
    DEBUG = False
    # En producción, asegúrate de establecer SESSION_COOKIE_SECURE=True si usas HTTPS
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    
    # Opciones adicionales de seguridad para producción
    # Asegúrate de que SECRET_KEY y ENCRYPTION_KEY estén configurados a través de variables de entorno

class TestingConfig(Config):
    """Configuración para pruebas."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False