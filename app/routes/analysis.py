"""
Rutas para funcionalidades de análisis de natación.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models import SwimTime, SwimLap, Swimmer  # Añadir Swimmer a las importaciones
from app.utils.auth import login_required

# Crear blueprint
analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/que_tal_si')
@login_required 
def que_tal_si():
    """Herramienta de simulación '¿Qué tal si?'"""
    # Datos de ejemplo para la demostración
    nadadores = [
        {'id': 1, 'nombre': 'Ana García'},
        {'id': 2, 'nombre': 'Carlos Rodríguez'},
        {'id': 3, 'nombre': 'María López'}
    ]
    return render_template('analysis/que_tal_si.html', nadadores=nadadores)

@analysis_bp.route('/tiempo_meta')
@login_required
def tiempo_meta():
    """Herramienta de cálculo de tiempo meta."""
    # Datos de ejemplo para la demostración
    nadadores = [
        {'id': 1, 'nombre': 'Ana García'},
        {'id': 2, 'nombre': 'Carlos Rodríguez'},
        {'id': 3, 'nombre': 'María López'}
    ]
    return render_template('analysis/tiempo_meta.html', nadadores=nadadores)

# En app/routes/analysis.py, modificar la ruta tiempos_competencia:

@analysis_bp.route('/tiempos_competencia')
@login_required
def tiempos_competencia():
    """Página de registro de tiempos de competencia."""
    # Obtener la lista de nadadores del usuario actual
    user_id = session['user_id']
    swimmers = Swimmer.query.filter_by(user_id=user_id).order_by(Swimmer.first_name).all()
    
    return render_template('analysis/tiempos_competencia.html', swimmers=swimmers)

# En app/routes/analysis.py, modificar la ruta guardar_tiempos:

@analysis_bp.route('/guardar_tiempos', methods=['POST'])
@login_required
def guardar_tiempos():
    """Procesa el formulario de registro de tiempos."""
    if 'user_id' not in session:
        flash("Debes iniciar sesión para guardar tiempos.", "danger")
        return redirect(url_for('auth.login'))
    
    try:
        # Obtener datos del formulario
        user_id = session['user_id']
        swimmer_id = request.form.get('swimmer_id')  # Ahora usamos el ID del nadador
        competition = request.form.get('competition')
        date = request.form.get('date')
        stroke = request.form.get('stroke')
        distance = int(request.form.get('distance'))
        pool_length = request.form.get('pool_length')
        time_total = request.form.get('time')
        level = request.form.get('level')
        
        # Buscar el nadador para obtener su nombre
        swimmer = Swimmer.query.filter_by(id=swimmer_id, user_id=user_id).first()
        if not swimmer:
            flash("Nadador no encontrado.", "danger")
            return redirect(url_for('analysis.tiempos_competencia'))
        
        # Crear nuevo registro de tiempo
        swim_time = SwimTime(
            user_id=user_id,
            swimmer_id=swimmer_id,
            swimmer_name=f"{swimmer.first_name} {swimmer.last_name}",  # Para compatibilidad
            competition=competition,
            date=date,
            gender=swimmer.gender,  # Ahora lo obtenemos del nadador
            stroke=stroke,
            distance=distance,
            pool_length=pool_length,
            time_total=time_total
        )
        
        # El resto del código sigue igual...
        
        db.session.add(swim_time)
        db.session.flush()  # Para obtener el ID generado
        
        # Calcular número de vueltas
        pool_length_value = int(pool_length.replace('m', '').replace('y', ''))
        laps = (distance + pool_length_value - 1) // pool_length_value  # Redondeado hacia arriba

        # Guardar tiempos por vuelta
        for i in range(1, laps + 1):
            lap_time_key = f"lap_time_{i}"
            lap_time = request.form.get(lap_time_key)
            
            # Si es nivel pro o elite, obtener datos adicionales
            stroke_rate = None
            stroke_length = None
            
            if level in ['pro', 'elite']:
                stroke_rate_key = f"stroke_rate_{i}"
                stroke_length_key = f"stroke_length_{i}"
                stroke_rate = request.form.get(stroke_rate_key)
                stroke_length = request.form.get(stroke_length_key)
            
            # Crear registro de vuelta
            if lap_time:
                lap = SwimLap(
                    swim_time_id=swim_time.id,
                    lap_number=i,
                    lap_time=lap_time,
                    stroke_rate=stroke_rate,
                    stroke_length=stroke_length
                )
                db.session.add(lap)
        
        db.session.commit()
        flash("Tiempos guardados correctamente.", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar tiempos: {str(e)}", "danger")
    
    return redirect(url_for('analysis.tiempos_competencia'))