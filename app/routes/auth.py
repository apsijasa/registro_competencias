"""
Rutas de autenticación y gestión de usuarios.
"""
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

# Crear blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página y formulario para crear un nuevo usuario."""
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        club_name = request.form.get('club_name', '')
        country = request.form.get('country', '')
       
        # Validaciones
        if not (first_name and last_name and email and password):
            flash("Por favor, completa los campos obligatorios.", "danger")
            return redirect(url_for('auth.register'))
       
        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for('auth.register'))
       
        try:
            # Verificar si el usuario ya existe
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Ya existe un usuario con este correo electrónico.", "danger")
                return redirect(url_for('auth.register'))
           
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
            db.session.commit()
           
            flash("¡Registro completado! Ya puedes iniciar sesión.", "success")
            return redirect(url_for('auth.login'))
       
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar: {str(e)}", "danger")
            return redirect(url_for('auth.register'))
       
    return render_template('auth/register.html')

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
            
            # Gestionar la redirección
            next_url = session.pop('next_url', None)
            return redirect(next_url or url_for('main.index'))
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