"""
Modelos de datos para la aplicación.
Define las clases de modelo para SQLAlchemy.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.utils.security import encrypt_data, decrypt_data

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
    
    # Relaciones
    free_trial = db.relationship('FreeTrialRegistration', backref='user', uselist=False)
    
    def set_password(self, password):
        """Genera el hash de la contraseña para almacenamiento seguro."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class FreeTrialRegistration(db.Model):
    """Modelo para registros de prueba gratuita."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    club_name = db.Column(db.String(100))
    country = db.Column(db.String(50))
    
    # Campos encriptados para información de tarjeta de crédito
    _card_name = db.Column('card_name', db.LargeBinary)
    _card_number = db.Column('card_number', db.LargeBinary)
    _card_expiry = db.Column('card_expiry', db.LargeBinary)
    _card_cvv = db.Column('card_cvv', db.LargeBinary)
    
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    trial_end_date = db.Column(db.DateTime)
    
    @property
    def card_name(self):
        """Obtiene el nombre de la tarjeta desencriptado."""
        if self._card_name:
            return decrypt_data(self._card_name)
        return None
    
    @card_name.setter
    def card_name(self, value):
        """Establece el nombre de la tarjeta encriptándolo."""
        if value:
            self._card_name = encrypt_data(value)
        else:
            self._card_name = None
    
    @property
    def card_number(self):
        """Obtiene el número de tarjeta desencriptado."""
        if self._card_number:
            return decrypt_data(self._card_number)
        return None
    
    @card_number.setter
    def card_number(self, value):
        """Establece el número de tarjeta encriptándolo."""
        if value:
            self._card_number = encrypt_data(value)
        else:
            self._card_number = None
    
    @property
    def card_expiry(self):
        """Obtiene la fecha de expiración desencriptada."""
        if self._card_expiry:
            return decrypt_data(self._card_expiry)
        return None
    
    @card_expiry.setter
    def card_expiry(self, value):
        """Establece la fecha de expiración encriptándola."""
        if value:
            self._card_expiry = encrypt_data(value)
        else:
            self._card_expiry = None
    
    @property
    def card_cvv(self):
        """Obtiene el CVV desencriptado."""
        if self._card_cvv:
            return decrypt_data(self._card_cvv)
        return None
    
    @card_cvv.setter
    def card_cvv(self, value):
        """Establece el CVV encriptándolo."""
        if value:
            self._card_cvv = encrypt_data(value)
        else:
            self._card_cvv = None
    
    def __repr__(self):
        return f'<FreeTrialRegistration {self.email}>'

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

class SwimTime(db.Model):
    """Modelo para registrar tiempos de natación."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    swimmer_name = db.Column(db.String(100), nullable=False)
    competition = db.Column(db.String(100))
    date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(1), nullable=False)  # 'M' o 'F'
    stroke = db.Column(db.String(10), nullable=False)  # 'free', 'back', 'breast', 'fly', 'im'
    distance = db.Column(db.Integer, nullable=False)   # en metros
    pool_length = db.Column(db.String(3), nullable=False)  # '25m', '50m', '25y'
    time_total = db.Column(db.String(10), nullable=False)  # formato 'mm:ss.cc'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con las vueltas
    laps = db.relationship('SwimLap', backref='swim_time', cascade='all, delete-orphan')
    
    # Relación con el usuario
    user = db.relationship('User', backref='swim_times')
    
    def __repr__(self):
        return f'<SwimTime {self.swimmer_name}: {self.distance}m {self.stroke} - {self.time_total}>'

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