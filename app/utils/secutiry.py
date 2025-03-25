"""
Utilidades de seguridad para la aplicación.

Este módulo proporciona funciones para mejorar la seguridad de la aplicación,
incluyendo encriptación, desencriptación y configuración de encabezados de seguridad.
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask import current_app

def get_encryption_key():
    """
    Obtiene o genera una clave de encriptación basada en la clave secreta de la aplicación.
    
    Returns:
        bytes: Clave de encriptación en formato bytes
    """
    # Obtener la clave de encriptación de la configuración
    key = current_app.config.get('ENCRYPTION_KEY', current_app.config['SECRET_KEY'])
    
    # Convertir a bytes si es una cadena
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # Usar PBKDF2 para derivar una clave adecuada para Fernet
    salt = b'swim_analysis_salt'  # En producción, esto debería ser un valor único y secreto
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    # Derivar la clave y convertirla a formato base64 para Fernet
    derived_key = base64.urlsafe_b64encode(kdf.derive(key))
    return derived_key

def encrypt_data(data):
    """
    Encripta datos sensibles utilizando Fernet (encriptación simétrica).
    
    Args:
        data (str): Datos a encriptar
        
    Returns:
        bytes: Datos encriptados
    """
    if not data:
        return None
    
    # Convertir a bytes si es necesario
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Crear instancia de Fernet con la clave de encriptación
    fernet = Fernet(get_encryption_key())
    
    # Encriptar los datos
    return fernet.encrypt(data)

def decrypt_data(encrypted_data):
    """
    Desencripta datos encriptados con Fernet.
    
    Args:
        encrypted_data (bytes): Datos encriptados
        
    Returns:
        str: Datos desencriptados como cadena
    """
    if not encrypted_data:
        return None
    
    # Crear instancia de Fernet con la clave de encriptación
    fernet = Fernet(get_encryption_key())
    
    try:
        # Desencriptar los datos y convertir a cadena
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        # Registrar el error, pero no exponer detalles específicos
        current_app.logger.error(f"Error desencriptando datos: {type(e).__name__}")
        return None

def init_security_headers(app):
    """
    Configura encabezados de seguridad HTTP para la aplicación.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    @app.after_request
    def add_security_headers(response):
        # Encabezados básicos de seguridad
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Política de seguridad de contenido (CSP)
        # Esta es una política básica, ajustar según las necesidades de la aplicación
        csp = "default-src 'self'; "
        csp += "script-src 'self' https://cdn.jsdelivr.net cdnjs.cloudflare.com; "
        csp += "style-src 'self' https://cdn.jsdelivr.net https://fonts.googleapis.com 'unsafe-inline'; "
        csp += "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        csp += "img-src 'self' data:; "
        csp += "connect-src 'self';"
        
        response.headers['Content-Security-Policy'] = csp
        
        # Prevenir el almacenamiento en caché de datos sensibles
        if app.config.get('ENV') == 'production':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response