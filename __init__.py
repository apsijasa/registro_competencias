from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import User, FreeTrialRegistration, ContactMessage

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Importar rutas después de crear la instancia db para evitar importaciones circulares
from routes import *

# Importar modelos
from models import User, FreeTrialRegistration, ContactMessage