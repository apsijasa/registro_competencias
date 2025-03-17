from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Importa los modelos (asegúrate de que models.py importe 'db' desde aquí)
from models import FreeTrialRegistration, ContactMessage

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
            flash("Por favor, complete los campos obligatorios.")
            return redirect(url_for('free_trial'))
        
        registration = FreeTrialRegistration(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,  # Aquí sería recomendable aplicar hashing
            club_name=club_name,
            country=country,
            card_name=card_name,
            card_number=card_number,
            card_expiry=card_expiry,
            card_cvv=card_cvv
        )
        db.session.add(registration)
        db.session.commit()
        flash("¡Registro completado! Pronto te contactaremos.")
        return redirect(url_for('index'))
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
            flash("Por favor, complete los campos obligatorios.")
            return redirect(url_for('contacto'))
        
        contact_message = ContactMessage(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        db.session.add(contact_message)
        db.session.commit()
        flash("¡Mensaje enviado! Nos pondremos en contacto contigo pronto.")
        return redirect(url_for('index'))
    return render_template('contacto.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea la base de datos y las tablas si no existen
    app.run(debug=True)
