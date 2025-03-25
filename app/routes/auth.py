"""
Rutas de autenticación y gestión de usuarios.
"""
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models import User, FreeTrialRegistration
from werkzeug.security import generate_password_hash

# Crear blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register')
def register():
    """Redirecciona al registro de prueba gratuita."""
    return redirect(url_for('auth.free_trial'))

@auth_bp.route('/free_trial', methods=['GET', 'POST'])
def free_trial():
    """Página y formulario de registro para prueba gratuita."""
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
            return redirect(url_for('auth.free_trial'))
       
        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for('auth.free_trial'))
       
        try:
            # Verificar si el usuario ya existe
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Ya existe un usuario con este correo electrónico.", "danger")
                return redirect(url_for('auth.free_trial'))
           
            # Crear nuevo usuario
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                club_name=club_name,
                country=country
            )
            new_user.set_password(password)
           
            # Guardar el usuario en la base de datos
            db.session.add(new_user)
            db.session.flush()  # Para obtener el ID generado
           
            # Crear registro de prueba gratuita
            trial_end_date = datetime.utcnow() + timedelta(days=14)  # 14 días de prueba
            free_trial_registration = FreeTrialRegistration(
                user_id=new_user.id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                club_name=club_name,
                country=country,
                trial_end_date=trial_end_date
            )
            
            # Establecer datos de tarjeta (encriptados)
            free_trial_registration.card_name = card_name
            free_trial_registration.card_number = card_number
            free_trial_registration.card_expiry = card_expiry
            free_trial_registration.card_cvv = card_cvv
           
            # Guardar el registro de prueba gratuita
            db.session.add(free_trial_registration)
            db.session.commit()
           
            flash("¡Registro completado! Pronto te contactaremos.", "success")
            return redirect(url_for('main.index'))
       
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar: {str(e)}", "danger")
            return redirect(url_for('auth.free_trial'))
       
    return render_template('auth/free_trial.html')

@auth_bp.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    """Página y formulario para crear un nuevo usuario."""
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
            return redirect(url_for('auth.crear_usuario'))
       
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
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear usuario: {str(e)}', 'danger')
            return redirect(url_for('auth.crear_usuario'))
   
    return render_template('auth/crear_usuario.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página y formulario de inicio de sesión."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
       
        user = User.query.filter_by(email=email).first()
       
        if user and user.check_password(password):
            # Actualizar última fecha de inicio de sesión
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Crear sesión de usuario
            session['user_id'] = user.id
            session['email'] = user.email
            session['first_name'] = user.first_name
            
            # Si se marca "recordarme", configurar la sesión como permanente
            if remember:
                session.permanent = True
            
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Email o contraseña incorrectos', 'danger')
            return redirect(url_for('auth.login'))
   
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Cierra la sesión del usuario."""
    # Eliminar todas las claves de la sesión
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """Página y formulario para solicitar restablecimiento de contraseña."""
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Verificar si el usuario existe
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Aquí implementaríamos el envío de email con token
            # Por ahora, solo mostramos un mensaje de éxito
            flash("Se ha enviado un correo para restablecer tu contraseña.", "success")
        else:
            # No revelar si el email existe o no por seguridad
            flash("Si el correo existe en nuestra base de datos, recibirás instrucciones para restablecer tu contraseña.", "info")
            
        return redirect(url_for('auth.login'))
       
    return render_template('auth/reset_password.html')