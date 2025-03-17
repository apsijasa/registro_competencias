from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from extensions import db
from .models import User, FreeTrialRegistration, ContactMessage  # Use relative import

def init_routes(app):
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
            confirm_password = request.form.get('confirm_password')
            club_name = request.form.get('club_name')
            country = request.form.get('country')
            card_name = request.form.get('card_name')
            card_number = request.form.get('card_number')
            card_expiry = request.form.get('card_expiry')
            card_cvv = request.form.get('card_cvv')
           
            # Validaciones
            if not (first_name and last_name and email and password):
                flash("Por favor, completa los campos obligatorios.", "danger")
                return redirect(url_for('free_trial'))
           
            if password != confirm_password:
                flash("Las contraseñas no coinciden.", "danger")
                return redirect(url_for('free_trial'))
           
            try:
                # Verificar si el usuario ya existe
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    flash("Ya existe un usuario con este correo electrónico.", "danger")
                    return redirect(url_for('free_trial'))
               
                # Crear nuevo usuario
                new_user = User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    club_name=club_name,
                    country=country
                )
                new_user.set_password(password)
               
                # Crear registro de prueba gratuita
                free_trial_registration = FreeTrialRegistration(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=generate_password_hash(password),
                    club_name=club_name,
                    country=country,
                    card_name=card_name,
                    card_number=card_number,
                    card_expiry=card_expiry,
                    card_cvv=card_cvv
                )
               
                # Guardar en la base de datos
                db.session.add(new_user)
                db.session.add(free_trial_registration)
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
            privacy = request.form.get('privacy') == 'on'
           
            if not (name and email and message and privacy):
                flash("Por favor, completa los campos obligatorios y acepta la política de privacidad.", "danger")
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

    @app.route('/crear_usuario', methods=['GET', 'POST'])
    def crear_usuario():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            club_name = request.form.get('club_name')
            
            # Verificar si el usuario ya existe
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Ya existe un usuario con este correo electrónico.', 'danger')
                return redirect(url_for('crear_usuario'))
            
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                club_name=club_name
            )
            new_user.set_password(password)
            
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Usuario creado exitosamente.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear usuario: {str(e)}', 'danger')
                return redirect(url_for('crear_usuario'))
        
        return render_template('crear_usuario.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
           
            user = User.query.filter_by(email=email).first()
           
            if user and user.check_password(password):
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('index'))
            else:
                flash('Email o contraseña incorrectos', 'danger')
                return redirect(url_for('login'))
       
        return render_template('login.html')

    @app.route('/reset_password', methods=['GET', 'POST'])
    def reset_password():
        if request.method == 'POST':
            email = request.form.get('email')
            flash("Se ha enviado un correo para restablecer tu contraseña.", "success")
            return redirect(url_for('login'))
           
        return render_template('reset_password.html')

    @app.route('/que_tal_si')
    def que_tal_si():
        nadadores = [
            {'id': 1, 'nombre': 'Ana García'},
            {'id': 2, 'nombre': 'Carlos Rodríguez'},
            {'id': 3, 'nombre': 'María López'}
        ]
        return render_template('que_tal_si.html', nadadores=nadadores)

    @app.route('/tiempo_meta')
    def tiempo_meta():
        nadadores = [
            {'id': 1, 'nombre': 'Ana García'},
            {'id': 2, 'nombre': 'Carlos Rodríguez'},
            {'id': 3, 'nombre': 'María López'}
        ]
        return render_template('tiempo_meta.html', nadadores=nadadores)

    @app.route('/tiempos_competencia')
    def tiempos_competencia():
        return render_template('tiempos_competencia.html')

    @app.route('/guardar_tiempos', methods=['POST'])
    def guardar_tiempos():
        flash("Tiempos guardados correctamente.", "success")
        return redirect(url_for('tiempos_competencia'))

    @app.route('/api/get_time')
    def get_time():
        name = request.args.get('name')
        stroke = request.args.get('stroke')
        distance = request.args.get('distance')
        pool = request.args.get('pool')
        return {'time': '1:03.45'}

    @app.route('/register')
    def register():
        return redirect(url_for('free_trial'))

    @app.route('/newsletter', methods=['POST'])
    def newsletter():
        email = request.form.get('email')
        if email:
            flash("¡Gracias por suscribirte a nuestro boletín!", "success")
        return redirect(url_for('index'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500