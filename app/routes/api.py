"""
Rutas para la API de la aplicación.
Estas rutas devuelven datos en formato JSON para ser consumidos por el frontend.
"""
from flask import Blueprint, jsonify, request

# Crear blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/get_time')
def get_time():
    """
    Obtiene el tiempo para un nadador, estilo, distancia y piscina específicos.
    
    Esta API es utilizada por la página de simulación '¿Qué tal si?' y la de tiempo meta.
    """
    name = request.args.get('name')
    stroke = request.args.get('stroke')
    distance = request.args.get('distance')
    pool = request.args.get('pool')
    
    # En una implementación real, aquí consultaríamos la base de datos
    # Por ahora, devolvemos un tiempo de ejemplo
    # Simular diferentes tiempos según los parámetros
    times = {
        '1': {'free': '1:03.45', 'back': '1:10.22', 'breast': '1:15.40', 'fly': '1:05.33', 'im': '1:18.75'},
        '2': {'free': '0:59.85', 'back': '1:05.50', 'breast': '1:10.15', 'fly': '1:02.45', 'im': '1:12.33'},
        '3': {'free': '1:05.75', 'back': '1:12.80', 'breast': '1:18.95', 'fly': '1:07.65', 'im': '1:20.50'}
    }
    
    # Obtener tiempo según el nadador y estilo
    time = times.get(name, {}).get(stroke, '1:00.00')
    
    return jsonify({'time': time})

@api_bp.route('/get_swimmer_history/<int:swimmer_id>')
def get_swimmer_history(swimmer_id):
    """
    Obtiene el historial de tiempos para un nadador específico.
    
    Args:
        swimmer_id: ID del nadador
        
    Returns:
        JSON con el historial de tiempos del nadador
    """
    # En una implementación real, consultaríamos la base de datos
    # Por ahora, devolvemos datos simulados
    
    # Datos simulados: fechas y tiempos de los últimos 12 meses
    history = []
    
    for i in range(12):
        month = (i + 1) % 12 + 1  # Meses del 1 al 12
        year = 2024 if month >= 3 else 2023  # Año actual o anterior
        
        # Tiempo simulado (mejorando gradualmente)
        base_time = 70.0  # Segundos
        improvement = i * 0.5  # Mejora gradual
        random_variation = (hash(f"{swimmer_id}-{month}-{year}") % 10 - 5) / 10.0  # Variación aleatoria pero consistente
        
        time = base_time - improvement + random_variation
        
        history.append({
            'date': f"{year}-{month:02d}",
            'time': time,
            'formatted_time': format_time(time)
        })
    
    return jsonify(history)

def format_time(seconds):
    """
    Formatea segundos a formato 'mm:ss.cc'.
    
    Args:
        seconds: Tiempo en segundos
        
    Returns:
        Cadena formateada en formato 'mm:ss.cc'
    """
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    centiseconds = int((remaining_seconds - int(remaining_seconds)) * 100)
    
    return f"{minutes:01d}:{int(remaining_seconds):02d}.{centiseconds:02d}"