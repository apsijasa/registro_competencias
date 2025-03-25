"""
Punto de entrada para ejecutar la aplicación Flask.
"""
import os
from dotenv import load_dotenv
from app import create_app
from app.config import DevelopmentConfig, ProductionConfig

# Cargar variables de entorno
load_dotenv()

# Determinar la configuración según el entorno
config = ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else DevelopmentConfig

# Crear la aplicación con la configuración adecuada
app = create_app(config)

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("¡Iniciando servidor Flask!")
    print(f"Modo de depuración: {'Activado' if debug else 'Desactivado'}")
    print("Servidor iniciado. Visita http://localhost:5000 en tu navegador.")
    
    app.run(debug=debug, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))