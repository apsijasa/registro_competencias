"""
Rutas principales de la aplicación.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import ContactMessage, Newsletter

# Crear blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página de inicio."""
    return render_template('index.html')

@main_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """Página y formulario de contacto."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        privacy = request.form.get('privacy') == 'on'
       
        if not (name and email and message and privacy):
            flash("Por favor, completa los campos obligatorios y acepta la política de privacidad.", "danger")
            return redirect(url_for('main.contacto'))
       
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
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al enviar mensaje: {str(e)}", "danger")
            return redirect(url_for('main.contacto'))
       
    return render_template('contacto.html')

@main_bp.route('/newsletter', methods=['POST'])
def newsletter():
    """Suscripción al boletín."""
    email = request.form.get('email')
    if email:
        try:
            # Verificar si ya existe el email
            existing = Newsletter.query.filter_by(email=email).first()
            if existing:
                if existing.is_active:
                    flash("Ya estás suscrito a nuestro boletín.", "info")
                else:
                    # Reactivar la suscripción
                    existing.is_active = True
                    db.session.commit()
                    flash("¡Has reactivado tu suscripción a nuestro boletín!", "success")
            else:
                # Crear nueva suscripción
                newsletter_sub = Newsletter(email=email)
                db.session.add(newsletter_sub)
                db.session.commit()
                flash("¡Gracias por suscribirte a nuestro boletín!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al procesar tu suscripción: {str(e)}", "danger")
    return redirect(url_for('main.index'))