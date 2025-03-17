from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from config import Config

# Inicializar Flask y extensiones
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Definir modelos
class FreeTrialRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    club_name = db.Column(db.String(100))
    country = db.Column(db.String(50))
    card_name = db.Column(db.String(100))
    card_number = db.Column(db.String(20))
    card_expiry = db.Column(db.String(10))
    card_cvv = db.Column(db.String(10))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(150))
    message = db.Column(db.Text, nullable=False)
    sent_on = db.Column(db.DateTime, default=datetime.utcnow)

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/free_trial', methods=['GET', 'POST'])
def free_trial():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        club_name = request.form.get('club_name')
        country = request.form.get('country')
        card_name = request.form.get('card_name')
        card_number = request.form.get('card_number')
        card_expiry = request.form.get('card_expiry')
        card_cvv = request.form.get('card_cvv')
        
        if not (first_name and last_name and email and password):
            flash("Por favor, complete los campos obligatorios.", "danger")
            return redirect(url_for('free_trial'))
        
        try:
            registration = FreeTrialRegistration(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                club_name=club_name,
                country=country,
                card_name=card_name,
                card_number=card_number,
                card_expiry=card_expiry,
                card_cvv=card_cvv
            )
            db.session.add(registration)
            db.session.commit()
            flash("¡Registro completado! Pronto te contactaremos.", "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar: {str(e)}", "danger")
            return redirect(url_for('free_trial'))
            
    return render_template('free_trial.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not (name and email and message):
            flash("Por favor, complete los campos obligatorios.", "danger")
            return redirect(url_for('contacto'))
        
        try:
            contact_message = ContactMessage(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            db.session.add(contact_message)
            db.session.commit()
            flash("¡Mensaje enviado! Nos pondremos en contacto contigo pronto.", "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al enviar mensaje: {str(e)}", "danger")
            return redirect(url_for('contacto'))
            
    return render_template('contacto.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de login aquí
        flash("Funcionalidad de inicio de sesión no implementada aún.", "info")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/que_tal_si')
def que_tal_si():
    # Simulamos obtener nadadores desde la base de datos
    nadadores = [
        {'id': 1, 'nombre': 'Ana García'},
        {'id': 2, 'nombre': 'Carlos Rodríguez'},
        {'id': 3, 'nombre': 'María López'}
    ]
    return render_template('que_tal_si.html', nadadores=nadadores)

@app.route('/tiempo_meta')
def tiempo_meta():
    # Simulamos obtener nadadores desde la base de datos
    nadadores = [
        {'id': 1, 'nombre': 'Ana García'},
        {'id': 2, 'nombre': 'Carlos Rodríguez'},
        {'id': 3, 'nombre': 'María López'}
    ]
    return render_template('tiempo_meta.html', nadadores=nadadores)

@app.route('/tiempos_competencia')
def tiempos_competencia():
    return render_template('tiempos_competencia.html')

@app.route('/newsletter', methods=['POST'])
def newsletter():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            flash("¡Gracias por suscribirte a nuestro boletín!", "success")
        return redirect(url_for('index'))
    
// Código JavaScript para la página de Tiempos de Competencia

document.addEventListener('DOMContentLoaded', function () {
  // Referencias a los elementos del DOM
  const levelSection = document.querySelector('.level-selection-section');
  const formSection = document.getElementById('registration-form-section');
  const basicTimeContainer = document.getElementById('basic-time-container');
  const advancedTimeContainer = document.getElementById('advanced-time-container');
  const eliteAnalysisContainer = document.getElementById('elite-analysis-container');
  const proLevelMessage = document.getElementById('pro-level-message');
  const formActions = document.getElementById('form-actions');
  const levelBadge = document.getElementById('selected-level-badge');
  const levelInput = document.getElementById('level_input');
  const premiumLevelSpan = document.getElementById('premium-level');

  // Botones
  const cancelBtn = document.getElementById('cancel-btn');
  const backToBasicBtn = document.getElementById('back-to-basic-btn');

  // Configurar botones de selección de nivel
  document.querySelectorAll('.select-level-btn').forEach(button => {
    button.addEventListener('click', function () {
      const level = this.getAttribute('data-level');
      selectLevel(level);
    });
  });

  // Función para seleccionar nivel
  function selectLevel(level) {
    // Ocultar sección de selección de nivel
    levelSection.style.display = 'none';

    // Actualizar el badge de nivel seleccionado y el input hidden
    levelBadge.textContent = level.charAt(0).toUpperCase() + level.slice(1);
    if (levelInput) levelInput.value = level;

    // Lógica según el nivel
    if (level === 'basic') {
      // Mostrar formulario para nivel básico
      formSection.style.display = 'block';
      basicTimeContainer.style.display = 'block';
      advancedTimeContainer.style.display = 'none';
      eliteAnalysisContainer.style.display = 'none';
      proLevelMessage.style.display = 'none';

      // Generar campos para tiempos por vuelta
      generateLapTimeFields();
    } else {
      // Para niveles Pro y Elite, mostrar mensaje de suscripción
      formSection.style.display = 'none';
      proLevelMessage.style.display = 'block';
      premiumLevelSpan.textContent = level.charAt(0).toUpperCase() + level.slice(1);
    }
  }

  // Generar campos de tiempo por vuelta según la distancia y longitud de piscina
  function generateLapTimeFields() {
    const distance = parseInt(document.getElementById('distance').value);
    const poolLength = parseInt(document.getElementById('pool_length').value);
    const lapTimes = document.getElementById('lap-times');
    
    // Limpiar contenido previo
    lapTimes.innerHTML = '';
    
    // Calcular número de vueltas
    const laps = Math.ceil(distance / poolLength);
    
    // Crear cuadrícula de campos
    const grid = document.createElement('div');
    grid.className = 'form-grid';
    
    for (let i = 1; i <= laps; i++) {
      const fieldContainer = document.createElement('div');
      fieldContainer.className = 'form-field';
      
      const label = document.createElement('label');
      label.innerHTML = `<i class="fas fa-flag-checkered"></i> Vuelta ${i}:`;
      label.setAttribute('for', `lap_time_${i}`);
      
      const input = document.createElement('input');
      input.type = 'text';
      input.id = `lap_time_${i}`;
      input.name = `lap_time_${i}`;
      input.placeholder = 'mm:ss.00';
      input.pattern = '^([0-5]?[0-9]:)?[0-5][0-9].[0-9]{2}$';
      
      fieldContainer.appendChild(label);
      fieldContainer.appendChild(input);
      grid.appendChild(fieldContainer);
    }
    
    lapTimes.appendChild(grid);
  }

  // Generar campos de análisis avanzado para Pro y Elite
  function generateAdvancedFields() {
    const distance = parseInt(document.getElementById('distance').value);
    const poolLength = parseInt(document.getElementById('pool_length').value);
    const advancedLapTimes = document.getElementById('advanced-lap-times');
    
    // Limpiar contenido previo
    advancedLapTimes.innerHTML = '';
    
    // Calcular número de vueltas
    const laps = Math.ceil(distance / poolLength);
    
    // Crear tabla para métricas avanzadas
    const table = document.createElement('table');
    table.className = 'data-table';
    
    // Encabezado
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    const headers = ['Vuelta', 'Tiempo', 'FR (c/min)', 'DPC (m)', 'Velocidad (m/s)'];
    headers.forEach(text => {
      const th = document.createElement('th');
      th.textContent = text;
      headerRow.appendChild(th);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Cuerpo de la tabla
    const tbody = document.createElement('tbody');
    
    for (let i = 1; i <= laps; i++) {
      const row = document.createElement('tr');
      
      // Celda de vuelta
      const lapCell = document.createElement('td');
      lapCell.textContent = i;
      row.appendChild(lapCell);
      
      // Celda de tiempo
      const timeCell = document.createElement('td');
      const timeInput = document.createElement('input');
      timeInput.type = 'text';
      timeInput.name = `adv_lap_time_${i}`;
      timeInput.placeholder = 'mm:ss.00';
      timeInput.pattern = '^([0-5]?[0-9]:)?[0-5][0-9].[0-9]{2}$';
      timeCell.appendChild(timeInput);
      row.appendChild(timeCell);
      
      // Celda de frecuencia de brazada
      const frCell = document.createElement('td');
      const frInput = document.createElement('input');
      frInput.type = 'number';
      frInput.name = `stroke_rate_${i}`;
      frInput.min = '20';
      frInput.max = '100';
      frCell.appendChild(frInput);
      row.appendChild(frCell);
      
      // Celda de distancia por ciclo
      const dpcCell = document.createElement('td');
      const dpcInput = document.createElement('input');
      dpcInput.type = 'number';
      dpcInput.name = `stroke_length_${i}`;
      dpcInput.step = '0.01';
      dpcInput.min = '1';
      dpcInput.max = '3';
      dpcCell.appendChild(dpcInput);
      row.appendChild(dpcCell);
      
      // Celda de velocidad
      const speedCell = document.createElement('td');
      const speedSpan = document.createElement('span');
      speedSpan.id = `speed_${i}`;
      speedSpan.textContent = '-';
      speedCell.appendChild(speedSpan);
      row.appendChild(speedCell);
      
      tbody.appendChild(row);
    }
    
    table.appendChild(tbody);
    advancedLapTimes.appendChild(table);
    
    // Configurar cálculos en tiempo real
    setupAdvancedCalculations();
  }

  // Configurar cálculos para campos avanzados
  function setupAdvancedCalculations() {
    const timeInputs = document.querySelectorAll('[name^="adv_lap_time_"]');
    const frInputs = document.querySelectorAll('[name^="stroke_rate_"]');
    const dpcInputs = document.querySelectorAll('[name^="stroke_length_"]');
    
    // Función para calcular velocidad
    const calculateSpeed = (index) => {
      const timeInput = document.querySelector(`[name="adv_lap_time_${index + 1}"]`);
      const frInput = document.querySelector(`[name="stroke_rate_${index + 1}"]`);
      const dpcInput = document.querySelector(`[name="stroke_length_${index + 1}"]`);
      const speedSpan = document.getElementById(`speed_${index + 1}`);
      
      if (timeInput && timeInput.value && dpcInput && dpcInput.value && frInput && frInput.value) {
        // Convertir tiempo a segundos
        const timeParts = timeInput.value.split(':');
        let seconds = 0;
        
        if (timeParts.length === 2) {
          seconds = parseFloat(timeParts[0]) * 60 + parseFloat(timeParts[1]);
        } else {
          seconds = parseFloat(timeParts[0]);
        }
        
        if (seconds > 0) {
          // Cálculo simplificado: velocidad = FR (ciclos/min) * DPC (m/ciclo) / 60
          const fr = parseFloat(frInput.value);
          const dpc = parseFloat(dpcInput.value);
          const speed = (fr * dpc / 60).toFixed(2);
          
          speedSpan.textContent = speed;
        }
      }
    };
    
    // Configurar event listeners para actualizar velocidad en tiempo real
    const updateAllSpeeds = () => {
      for (let i = 0; i < timeInputs.length; i++) {
        calculateSpeed(i);
      }
    };
    
    timeInputs.forEach((input, index) => {
      input.addEventListener('input', () => calculateSpeed(index));
    });
    
    frInputs.forEach((input, index) => {
      input.addEventListener('input', () => calculateSpeed(index));
    });
    
    dpcInputs.forEach((input, index) => {
      input.addEventListener('input', () => calculateSpeed(index));
    });
  }

  // Event listeners para actualizaciones en tiempo real
  document.getElementById('distance').addEventListener('change', function() {
    generateLapTimeFields();
    if (advancedTimeContainer.style.display !== 'none') {
      generateAdvancedFields();
    }
  });
  
  document.getElementById('pool_length').addEventListener('change', function() {
    generateLapTimeFields();
    if (advancedTimeContainer.style.display !== 'none') {
      generateAdvancedFields();
    }
  });

  // Event listeners para botones
  if (cancelBtn) {
    cancelBtn.addEventListener('click', function() {
      // Volver a mostrar la selección de nivel
      formSection.style.display = 'none';
      levelSection.style.display = 'block';
    });
  }

  if (backToBasicBtn) {
    backToBasicBtn.addEventListener('click', function() {
      // Seleccionar nivel básico
      selectLevel('basic');
    });
  }

  // Inicialización
  // Generar campos iniciales para tiempos por vuelta
  setTimeout(generateLapTimeFields, 0);
});

@app.route('/api/get_time')
def get_time():
    """API para obtener tiempos desde JavaScript"""
    name = request.args.get('name')
    stroke = request.args.get('stroke')
    distance = request.args.get('distance')
    pool = request.args.get('pool')
    
    # Aquí iría la lógica para obtener el tiempo desde la base de datos
    # Por ahora retornamos un tiempo simulado
    return jsonify({'time': '1:03.45'})

@app.route('/register')
def register():
    # Redirecciona a la prueba gratuita
    return redirect(url_for('free_trial'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if email:
            # En un entorno real, aquí verificarías si el correo existe en la base de datos
            # y enviarías un correo electrónico con instrucciones para restablecer la contraseña
            
            flash("Se han enviado instrucciones para restablecer tu contraseña a tu correo electrónico.", "success")
            return redirect(url_for('login'))
        else:
            flash("Por favor, introduce tu correo electrónico.", "danger")
            
    # Si es una solicitud GET o si el formulario no se procesó correctamente, mostrar el formulario
    return render_template('contraseñas.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea la base de datos y las tablas si no existen
    app.run(debug=True)