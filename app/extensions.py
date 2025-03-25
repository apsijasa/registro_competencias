"""
Extensiones de Flask utilizadas en la aplicación.
Este módulo inicializa las extensiones de Flask para su uso en toda la aplicación.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

# Inicializar extensiones
db = SQLAlchemy()
csrf = CSRFProtect()
mail = Mail()