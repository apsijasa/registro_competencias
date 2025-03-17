from __init__ import db
from datetime import datetime

class FreeTrialRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Recomendable usar hashing
    club_name = db.Column(db.String(100))
    country = db.Column(db.String(50))
    card_name = db.Column(db.String(100))
    card_number = db.Column(db.String(20))
    card_expiry = db.Column(db.String(10))
    card_cvv = db.Column(db.String(10))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(150))
    message = db.Column(db.Text, nullable=False)
    sent_on = db.Column(db.DateTime, default=datetime.utcnow)