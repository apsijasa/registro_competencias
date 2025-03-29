# Crear un nuevo archivo app/routes/swimmers.py:

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models import Swimmer, SwimTime
from app.utils.auth import login_required
from datetime import datetime
from flask import jsonify

# Crear blueprint
swimmers_bp = Blueprint('swimmers', __name__)

@swimmers_bp.route('/nadadores')
@login_required
def list_swimmers():
    """Muestra la lista de nadadores del usuario."""
    user_id = session['user_id']
    swimmers = Swimmer.query.filter_by(user_id=user_id).order_by(Swimmer.first_name).all()
    return render_template('swimmers/index.html', swimmers=swimmers)

@swimmers_bp.route('/nadadores/nuevo', methods=['GET', 'POST'])
@login_required
def new_swimmer():
    """Página y formulario para crear un nuevo nadador."""
    if request.method == 'POST':
        user_id = session['user_id']
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        birth_date_str = request.form.get('birth_date')
        gender = request.form.get('gender')
        
        # Validaciones
        if not (first_name and last_name and birth_date_str and gender):
            flash("Por favor, completa los campos obligatorios.", "danger")
            return redirect(url_for('swimmers.new_swimmer'))

        # Validar fecha de nacimiento
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            
            # Verificar que la fecha no sea futura
            if birth_date > datetime.now().date():
                flash("La fecha de nacimiento no puede ser futura.", "danger")
                return redirect(url_for('swimmers.new_swimmer'))
                
        except ValueError:
            flash("El formato de la fecha de nacimiento es incorrecto.", "danger")
            return redirect(url_for('swimmers.new_swimmer'))
        try:
            # Convertir fecha
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            
            # Crear nuevo nadador
            new_swimmer = Swimmer(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                birth_date=birth_date,
                gender=gender
            )
            
            # Guardar en la base de datos
            db.session.add(new_swimmer)
            db.session.commit()
            
            flash("¡Nadador registrado correctamente!", "success")
            return redirect(url_for('swimmers.list_swimmers'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar nadador: {str(e)}", "danger")
            return redirect(url_for('swimmers.new_swimmer'))
    
    return render_template('swimmers/edit.html', swimmer=swimmer, SwimTime=SwimTime)

@swimmers_bp.route('/nadadores/json')
@login_required
def get_swimmers_json():
    """Devuelve la lista de nadadores en formato JSON."""
    user_id = session['user_id']
    swimmers = Swimmer.query.filter_by(user_id=user_id).order_by(Swimmer.first_name).all()
    
    # Convertir a formato JSON
    swimmers_list = [
        {
            'id': swimmer.id,
            'first_name': swimmer.first_name,
            'last_name': swimmer.last_name
        }
        for swimmer in swimmers
    ]
    
    return jsonify({'swimmers': swimmers_list})

@swimmers_bp.route('/nadadores/<int:swimmer_id>/editar', methods=['GET', 'POST'])
@login_required
def edit_swimmer(swimmer_id):
    """Página y formulario para editar un nadador existente."""
    user_id = session['user_id']
    swimmer = Swimmer.query.filter_by(id=swimmer_id, user_id=user_id).first_or_404()
    
    if request.method == 'POST':
        try:
            swimmer.first_name = request.form.get('first_name')
            swimmer.last_name = request.form.get('last_name')
            swimmer.email = request.form.get('email')
            birth_date_str = request.form.get('birth_date')
            swimmer.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            swimmer.gender = request.form.get('gender')
            
            db.session.commit()
            flash("Datos del nadador actualizados correctamente.", "success")
            return redirect(url_for('swimmers.list_swimmers'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar datos: {str(e)}", "danger")
    
    return render_template('swimmers/edit.html', swimmer=swimmer)

@swimmers_bp.route('/nadadores/<int:swimmer_id>/eliminar', methods=['POST'])
@login_required
def delete_swimmer(swimmer_id):
    """Elimina un nadador de la base de datos."""
    user_id = session['user_id']
    swimmer = Swimmer.query.filter_by(id=swimmer_id, user_id=user_id).first_or_404()
    
    try:
        db.session.delete(swimmer)
        db.session.commit()
        flash("Nadador eliminado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar nadador: {str(e)}", "danger")
    
    return redirect(url_for('swimmers.list_swimmers'))