"""
Decoradores de autenticación para la aplicación.
Este módulo proporciona decoradores para proteger rutas que requieren autenticación.
"""
from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(f):
    """
    Decorador que verifica si el usuario ha iniciado sesión.
    Redirige a la página de login si el usuario no está autenticado.
    
    Args:
        f: La función de vista que se va a decorar.
        
    Returns:
        La función decorada que verificará la autenticación.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Guardar la URL a la que intentó acceder para redirigir después del login
            session['next_url'] = request.url
            
            # Mostrar mensaje al usuario
            flash("Debes iniciar sesión para acceder a esta página.", "warning")
            
            # Redirigir a la página de login
            return redirect(url_for('auth.login'))
            
        return f(*args, **kwargs)
    return decorated_function

def is_authenticated():
    """
    Comprueba si el usuario actual está autenticado.
    
    Returns:
        bool: True si el usuario está autenticado, False en caso contrario.
    """
    return 'user_id' in session