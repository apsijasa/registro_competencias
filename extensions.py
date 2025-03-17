from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Crea las extensiones globalmente
db = SQLAlchemy()
csrf = CSRFProtect()