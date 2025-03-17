from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from config import Config

# Inicializar Flask y extensiones
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Definir modelos
class FreeTrialRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
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

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/free_trial', methods=['GET', 'POST'])
def free_trial():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        club_name = request.form.get('club_name')
        country = request.form.get('country')
        card_name = request.form.get('card_name')
        card_number = request.form.get('card_number')
        card_expiry = request.form.get('card_expiry')
        card_cvv = request.form.get('card_cvv')
        
        if not (first_name and last_name and email and password):
            flash("Por favor, complete los campos obligatorios.", "danger")
            return redirect(url_for('free_trial'))
        
        try:
            registration = FreeTrialRegistration(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                club_name=club_name,
                country=country,
                card_name=card_name,
                card_number=card_number,
                card_expiry=card_expiry,
                card_cvv=card_cvv
            )
            db.session.add(registration)
            db.session.commit()
            flash("¡Registro completado! Pronto te contactaremos.", "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar: {str(e)}", "danger")
            return redirect(url_for('free_trial'))
            
    return render_template('free_trial.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not (name and email and message):
            flash("Por favor, complete los campos obligatorios.", "danger")
            return redirect(url_for('contacto'))
        
        try:
            contact_message = ContactMessage(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            db.session.add(contact_message)
            db.session.commit()
            flash("¡Mensaje enviado! Nos pondremos en contacto contigo pronto.", "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al enviar mensaje: {str(e)}", "danger")
            return redirect(url_for('contacto'))
            
    return render_template('contacto.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de login aquí
        flash("Funcionalidad de inicio de sesión no implementada aún.", "info")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/que_tal_si')
def que_tal_si():
    # Simulamos obtener nadadores desde la base de datos
    nadadores = [
        {'id': 1, 'nombre': 'Ana García'},
        {'id': 2, 'nombre': 'Carlos Rodríguez'},
        {'id': 3, 'nombre': 'María López'}
    ]
    return render_template('que_tal_si.html', nadadores=nadadores)

@app.route('/tiempo_meta')
def tiempo_meta():
    # Simulamos obtener nadadores desde la base de datos
    nadadores = [
        {'id': 1, 'nombre': 'Ana García'},
        {'id': 2, 'nombre': 'Carlos Rodríguez'},
        {'id': 3, 'nombre': 'María López'}
    ]
    return render_template('tiempo_meta.html', nadadores=nadadores)

@app.route('/tiempos_competencia')
def tiempos_competencia():
    return render_template('tiempos_competencia.html')

@app.route('/newsletter', methods=['POST'])
def newsletter():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            flash("¡Gracias por suscribirte a nuestro boletín!", "success")
        return redirect(url_for('index'))
