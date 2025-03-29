"""
Modelos de datos para la aplicación.
Define las clases de modelo para SQLAlchemy.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    """Modelo para usuarios registrados."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    club_name = db.Column(db.String(100))
    country = db.Column(db.String(50))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Genera el hash de la contraseña para almacenamiento seguro."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
# Modificar en app/models.py:

class SwimTime(db.Model):
    """Modelo para registrar tiempos de natación."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    swimmer_id = db.Column(db.Integer, db.ForeignKey('swimmer.id'), nullable=False)  # Nueva relación
    competition = db.Column(db.String(100))
    date = db.Column(db.Date, nullable=False)
    stroke = db.Column(db.String(10), nullable=False)  # 'free', 'back', 'breast', 'fly', 'im'
    distance = db.Column(db.Integer, nullable=False)   # en metros
    pool_length = db.Column(db.String(3), nullable=False)  # '25m', '50m', '25y'
    time_total = db.Column(db.String(10), nullable=False)  # formato 'mm:ss.cc'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Mantener el campo swimmer_name como opcional para compatibilidad con registros existentes
    swimmer_name = db.Column(db.String(100))
    
    # Relaciones
    laps = db.relationship('SwimLap', backref='swim_time', cascade='all, delete-orphan')
    user = db.relationship('User', backref='swim_times')
    
# En app/models.py, añadir:

class ContactMessage(db.Model):
    """Modelo para mensajes de contacto."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(150))
    message = db.Column(db.Text, nullable=False)
    sent_on = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<ContactMessage {self.email}: {self.subject}>'

# Modificar en app/models.py:

class SwimTime(db.Model):
    """Modelo para registrar tiempos de natación."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    swimmer_id = db.Column(db.Integer, db.ForeignKey('swimmer.id'), nullable=False)  # Nueva relación
    competition = db.Column(db.String(100))
    date = db.Column(db.Date, nullable=False)
    stroke = db.Column(db.String(10), nullable=False)  # 'free', 'back', 'breast', 'fly', 'im'
    distance = db.Column(db.Integer, nullable=False)   # en metros
    pool_length = db.Column(db.String(3), nullable=False)  # '25m', '50m', '25y'
    time_total = db.Column(db.String(10), nullable=False)  # formato 'mm:ss.cc'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Mantener el campo swimmer_name como opcional para compatibilidad con registros existentes
    swimmer_name = db.Column(db.String(100))
    
    # Relaciones
    laps = db.relationship('SwimLap', backref='swim_time', cascade='all, delete-orphan')
    user = db.relationship('User', backref='swim_times')
    
class SwimLap(db.Model):
    """Modelo para registrar tiempos por vuelta."""
    id = db.Column(db.Integer, primary_key=True)
    swim_time_id = db.Column(db.Integer, db.ForeignKey('swim_time.id'), nullable=False)
    lap_number = db.Column(db.Integer, nullable=False)
    lap_time = db.Column(db.String(10), nullable=False)  # formato 'mm:ss.cc'
    stroke_rate = db.Column(db.Float)  # ciclos por minuto
    stroke_length = db.Column(db.Float)  # distancia por ciclo en metros
    
    def __repr__(self):
        return f'<SwimLap {self.lap_number}: {self.lap_time}>'

class Newsletter(db.Model):
    """Modelo para suscriptores del boletín."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_on = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Newsletter {self.email}>'
    