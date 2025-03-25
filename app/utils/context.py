"""
Utilidades de contexto para plantillas.
Este módulo proporciona funciones para añadir variables y utilidades al contexto de las plantillas.
"""
from flask import session

def init_template_context(app):
    """
    Inicializa el contexto para todas las plantillas.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    @app.context_processor
    def utility_processor():
        """
        Añade funciones de utilidad y variables al contexto de la plantilla.
        
        Returns:
            dict: Diccionario con funciones y variables disponibles en las plantillas
        """
        return {
            'is_authenticated': 'user_id' in session,
            'current_user': {
                'id': session.get('user_id'),
                'email': session.get('email'),
                'first_name': session.get('first_name'),
            } if 'user_id' in session else None
        }