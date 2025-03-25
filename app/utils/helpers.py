"""
Funciones auxiliares para la aplicación.
"""
from datetime import datetime

def time_to_seconds(time_str):
    """
    Convierte una cadena de tiempo en formato 'mm:ss.cc' a segundos.
    
    Args:
        time_str (str): Tiempo en formato 'mm:ss.cc' o 'ss.cc'
        
    Returns:
        float: Tiempo en segundos
    """
    if not time_str or time_str == '-':
        return 0
    
    minutes = 0
    seconds = 0
    centiseconds = 0
    
    if ':' in time_str:
        # Formato 'mm:ss.cc'
        parts = time_str.split(':')
        minutes = int(parts[0])
        sec_parts = parts[1].split('.')
        seconds = int(sec_parts[0])
        centiseconds = int(sec_parts[1]) if len(sec_parts) > 1 else 0
    else:
        # Formato 'ss.cc'
        sec_parts = time_str.split('.')
        seconds = int(sec_parts[0])
        centiseconds = int(sec_parts[1]) if len(sec_parts) > 1 else 0
    
    return minutes * 60 + seconds + centiseconds / 100

def seconds_to_time(seconds):
    """
    Convierte segundos a una cadena de tiempo en formato 'mm:ss.cc'.
    
    Args:
        seconds (float): Tiempo en segundos
        
    Returns:
        str: Tiempo formateado como 'mm:ss.cc'
    """
    if seconds is None or seconds < 0:
        return '00:00.00'
    
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    centiseconds = int((remaining_seconds - int(remaining_seconds)) * 100)
    
    return f"{minutes:02d}:{int(remaining_seconds):02d}.{centiseconds:02d}"

def format_date(date_obj, format_str='%d/%m/%Y'):
    """
    Formatea un objeto fecha a una cadena.
    
    Args:
        date_obj: Objeto datetime o date
        format_str: Formato de salida (por defecto '%d/%m/%Y')
        
    Returns:
        str: Fecha formateada
    """
    if not date_obj:
        return ''
    
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
        except ValueError:
            return date_obj
    
    return date_obj.strftime(format_str)

def calculate_swim_metrics(distance, time_seconds, stroke_rate=None, stroke_length=None):
    """
    Calcula métricas de natación basadas en distancia y tiempo.
    
    Args:
        distance (float): Distancia en metros
        time_seconds (float): Tiempo en segundos
        stroke_rate (float, optional): Frecuencia de brazada (ciclos por minuto)
        stroke_length (float, optional): Distancia por ciclo en metros
        
    Returns:
        dict: Diccionario con métricas calculadas
    """
    metrics = {}
    
    # Calcular velocidad (m/s)
    if time_seconds > 0:
        metrics['speed'] = distance / time_seconds
    else:
        metrics['speed'] = 0
    
    # Si se proporcionan datos adicionales
    if stroke_rate and stroke_length:
        # Convertir frecuencia de brazada a ciclos por segundo
        stroke_rate_per_second = stroke_rate / 60
        
        # Calcular eficiencia
        calculated_speed = stroke_rate_per_second * stroke_length
        metrics['efficiency'] = (metrics['speed'] / calculated_speed) if calculated_speed > 0 else 0
        
        # Calcular índice de nado
        metrics['swim_index'] = stroke_length * metrics['speed']
    
    return metrics