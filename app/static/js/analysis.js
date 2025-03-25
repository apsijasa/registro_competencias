/**
 * SWIM ANALYSIS - JavaScript para las funcionalidades de análisis
 * Este archivo contiene funciones específicas para las páginas de análisis de natación:
 * - ¿Qué tal si?
 * - Tiempo Meta
 * - Tiempos Competencia
 */

document.addEventListener('DOMContentLoaded', function() {
    // Detectar qué página de análisis está activa y cargar funcionalidades específicas
    const pageUrl = window.location.pathname;
    
    if (pageUrl.includes('que_tal_si')) {
        initWhatIfPage();
    } else if (pageUrl.includes('tiempo_meta')) {
        initTargetTimePage();
    } else if (pageUrl.includes('tiempos_competencia')) {
        initTimesRegistrationPage();
    }
});

/**
 * Inicializa la página "¿Qué tal si?"
 */
function initWhatIfPage() {
    // Referencias a elementos del DOM 
    const nombreSelect = document.getElementById('nombre');
    const strokeSelect = document.getElementById('stroke');
    const distanceSelect = document.getElementById('distance');
    const poolSelect = document.getElementById('pool');
    const improvementSelect = document.getElementById('improvement');

    // Referencias a los elementos de resumen
    const genderElement = document.getElementById('gender');
    const pbTimeElement = document.getElementById('pb_time');
    const avgSpeedElement = document.getElementById('avg_speed');
    const ttElement = document.getElementById('tt');
    const timeDifferenceElement = document.getElementById('time_difference');
    const avgTtSpeedElement = document.getElementById('avg_tt_speed');

    // Referencias a las tablas
    const actualSwimThead = document.getElementById('actual-swim-thead');
    const actualSwimTbody = document.getElementById('actual-swim-tbody');
    const idealSwimThead = document.getElementById('ideal-swim-thead');
    const idealSwimTbody = document.getElementById('ideal-swim-tbody');

    // Referencias a los lienzos de gráficos
    const historyChartCanvas = document.getElementById('historyChart');
    const actualSwimChartCanvas = document.getElementById('actualSwimChart');
    const idealSwimChartCanvas = document.getElementById('idealSwimChart');

    // Configurar gráficos si Chart.js está cargado
    let historyChart = null;
    let actualSwimChart = null;
    let idealSwimChart = null;

    // Variable para almacenar datos de la última carrera seleccionada
    let currentSwimData = null;
    let currentSwimType = 'basic'; // 'basic' o 'advanced'

    // Configurar event listeners
    if (nombreSelect && strokeSelect) {
        nombreSelect.addEventListener('change', updateSwimmerInfo);
        strokeSelect.addEventListener('change', updateDistances);
        
        if (distanceSelect) {
            distanceSelect.addEventListener('change', updateSwimmerInfo);
        }
        
        if (poolSelect) {
            poolSelect.addEventListener('change', updateSwimmerInfo);
        }
        
        if (improvementSelect) {
            improvementSelect.addEventListener('change', updateTargetSpeedWithImprovement);
        }
        
        // Inicializar la página
        updateDistances();
    }

    // Función para actualizar las distancias disponibles según el estilo
    function updateDistances() {
        if (!distanceSelect) return;
        
        const stroke = strokeSelect.value;
        distanceSelect.innerHTML = "";

        let distances = [];

        if (stroke === "free") {
            distances = [50, 100, 200, 400, 800, 1500];
        } else if (stroke === "fly" || stroke === "back" || stroke === "breast") {
            distances = [50, 100, 200];
        } else if (stroke === "im") {
            distances = [100, 200, 400];
        }

        distances.forEach(function (d) {
            const option = document.createElement("option");
            option.value = d;
            option.text = d + "m";
            distanceSelect.add(option);
        });

        // Actualizar datos con la nueva distancia seleccionada
        updateSwimmerInfo();
    }

    // Función para cargar la información del nadador y las carreras
    function updateSwimmerInfo() {
        if (!nombreSelect || !strokeSelect || !distanceSelect || !poolSelect) return;
        
        const nadadorId = nombreSelect.value;
        const stroke = strokeSelect.value;
        const distance = distanceSelect.value;
        const pool = poolSelect.value;

        // Hacer petición a la API
        fetch(`/api/get_time?name=${nadadorId}&stroke=${stroke}&distance=${distance}&pool=${pool}`)
            .then(response => response.json())
            .then(data => {
                // Simular datos con la información obtenida
                simulateSwimmerData(nadadorId, stroke, distance, pool, data.time);
            })
            .catch(error => {
                console.error('Error al obtener datos:', error);
                // Fallback: simular datos igualmente
                simulateSwimmerData(nadadorId, stroke, distance, pool, "1:03.45");
            });
    }

    // Función para simular datos del servidor
    function simulateSwimmerData(nadadorId, stroke, distance, pool, pbTime) {
        // Datos simulados
        const gender = "Masculino";
        const tt = calcularTiempoMeta(pbTime);

        // Calcular velocidad media (metros por segundo)
        const pbTimeSeconds = timeToSeconds(pbTime);
        const ttTimeSeconds = timeToSeconds(tt);
        const avgSpeed = (distance / pbTimeSeconds).toFixed(2);
        const avgTtSpeed = (distance / ttTimeSeconds).toFixed(2);
        const timeDifference = (pbTimeSeconds - ttTimeSeconds).toFixed(2);

        // Actualizar elementos de resumen si existen
        if (genderElement) genderElement.textContent = gender;
        if (pbTimeElement) pbTimeElement.textContent = pbTime;
        if (avgSpeedElement) avgSpeedElement.textContent = avgSpeed + " m/s";
        if (ttElement) ttElement.textContent = tt;
        if (timeDifferenceElement) timeDifferenceElement.textContent = timeDifference + " s";
        if (avgTtSpeedElement) avgTtSpeedElement.textContent = avgTtSpeed + " m/s";

        // Generar datos de carrera aleatorios
        generateRandomSwimData(distance, pool);

        // Actualizar gráfico histórico
        updateHistoryChart(nadadorId, stroke, distance, pool);
    }

    // Resto de funciones específicas para la página "¿Qué tal si?"...
    // Estas funciones incluirían el cálculo de tiempos, actualización de gráficos, etc.
    
    // Calcular tiempo meta (5% mejor que tiempo personal)
    function calcularTiempoMeta(pbTime) {
        const pbSeconds = timeToSeconds(pbTime);
        const ttSeconds = pbSeconds * 0.95;
        return secondsToTime(ttSeconds);
    }

    // Función para convertir tiempo en formato "mm:ss.cc" a segundos
    function timeToSeconds(timeStr) {
        if (!timeStr || timeStr === '-') return 0;

        let minutes = 0, seconds = 0, centiseconds = 0;

        if (timeStr.includes(':')) {
            // Formato mm:ss.cc
            const parts = timeStr.split(':');
            minutes = parseInt(parts[0]) || 0;

            if (parts[1].includes('.')) {
                const secParts = parts[1].split('.');
                seconds = parseInt(secParts[0]) || 0;
                centiseconds = parseInt(secParts[1]) || 0;
            } else {
                seconds = parseInt(parts[1]) || 0;
            }
        } else if (timeStr.includes('.')) {
            // Formato ss.cc
            const parts = timeStr.split('.');
            seconds = parseInt(parts[0]) || 0;
            centiseconds = parseInt(parts[1]) || 0;
        } else {
            // Solo segundos
            seconds = parseInt(timeStr) || 0;
        }

        return minutes * 60 + seconds + centiseconds / 100;
    }

    // Función para convertir segundos a formato "mm:ss.cc"
    function secondsToTime(totalSeconds) {
        if (isNaN(totalSeconds) || totalSeconds === 0) return '00:00.00';

        const minutes = Math.floor(totalSeconds / 60);
        const seconds = Math.floor(totalSeconds % 60);
        const centiseconds = Math.round((totalSeconds - Math.floor(totalSeconds)) * 100);

        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${centiseconds.toString().padStart(2, '0')}`;
    }
    
    // Función para actualizar la velocidad del tiempo meta con el porcentaje de mejora
    function updateTargetSpeedWithImprovement() {
        if (!improvementSelect || !avgSpeedElement || !avgTtSpeedElement) return;
        
        const improvement = parseFloat(improvementSelect.value) / 100;

        // Extraer solo el valor numérico de la velocidad actual
        const avgSpeedText = avgSpeedElement.textContent;
        const avgSpeed = parseFloat(avgSpeedText);

        const improvedSpeed = isNaN(avgSpeed) ? 0 : (avgSpeed / (1 - improvement)).toFixed(2);

        avgTtSpeedElement.textContent = improvedSpeed + " m/s";

        // Si ya tenemos datos de natación, actualizar la tabla ideal
        if (currentSwimData) {
            updateIdealSwimTable(currentSwimData, 1 - improvement);
            updateIdealSwimChart();
        }
    }
    
    // Resto de las funciones para el análisis "¿Qué tal si?"...
    function generateRandomSwimData(distance, pool) {
        // Implementación simulada para generar datos de natación
        // En una aplicación real, estos datos vendrían del servidor
        const poolLength = pool === '50m' ? 50 : 25;
        const laps = Math.ceil(distance / poolLength);
        
        // Por ahora, generamos datos simulados
        // ...
    }
    
    function updateHistoryChart(nadadorId, stroke, distance, pool) {
        // Implementación para actualizar el gráfico histórico
        // ...
    }
    
    function updateActualSwimTable(sections) {
        // Implementación para actualizar la tabla de nado actual
        // ...
    }
    
    function updateIdealSwimTable(sections, improvementFactor) {
        // Implementación para actualizar la tabla de nado ideal
        // ...
    }
    
    function updateActualSwimChart() {
        // Implementación para actualizar el gráfico de nado actual
        // ...
    }
    
    function updateIdealSwimChart() {
        // Implementación para actualizar el gráfico de nado ideal
        // ...
    }
}

/**
 * Inicializa la página "Tiempo Meta"
 */
function initTargetTimePage() {
    // Referencias a elementos del DOM
    const nameSelect = document.getElementById('name');
    const strokeSelect = document.getElementById('stroke');
    const distanceSelect = document.getElementById('Distance');
    const poolSelect = document.getElementById('pool');
    const timeInput = document.getElementById('time');
    
    // Configurar event listeners
    if (nameSelect) {
        nameSelect.addEventListener('change', loadTimingData);
    }
    
    if (strokeSelect) {
        strokeSelect.addEventListener('change', loadTimingData);
    }
    
    if (distanceSelect) {
        distanceSelect.addEventListener('change', loadTimingData);
    }
    
    if (poolSelect) {
        poolSelect.addEventListener('change', loadTimingData);
    }
    
    // Inicializar la página
    if (nameSelect && strokeSelect && distanceSelect && poolSelect) {
        loadTimingData();
    }
    
    // Función para cargar datos de tiempo
    function loadTimingData() {
        const selectedName = nameSelect.value;
        const selectedStroke = strokeSelect.value;
        const selectedDistance = distanceSelect.value;
        const selectedPool = poolSelect.value;
        
        // Hacer petición a la API
        fetch(`/api/get_time?name=${selectedName}&stroke=${selectedStroke}&distance=${selectedDistance}&pool=${selectedPool}`)
            .then(response => response.json())
            .then(data => {
                // Actualizar el campo de tiempo
                if (timeInput) {
                    timeInput.value = data.time;
                }
                
                // Generar zonas de entrenamiento
                generateTrainingZones(data.time);
            })
            .catch(error => {
                console.error('Error al obtener datos:', error);
            });
    }
    
    // Función para generar zonas de entrenamiento
    function generateTrainingZones(baseTime) {
        // Implementación para calcular y mostrar zonas de entrenamiento
        // ...
    }
}

/**
 * Inicializa la página "Tiempos Competencia"
 */
function initTimesRegistrationPage() {
    // Referencias a elementos del DOM
    const levelButtons = document.querySelectorAll('.select-level-btn');
    const registrationForm = document.getElementById('registration-form-section');
    const levelSection = document.querySelector('.level-selection-section');
    const proLevelMessage = document.getElementById('pro-level-message');
    const cancelBtn = document.getElementById('cancel-btn');
    const backToBasicBtn = document.getElementById('back-to-basic-btn');
    const distanceSelect = document.getElementById('distance');
    const poolLengthSelect = document.getElementById('pool_length');
    
    // Configurar botones de selección de nivel
    if (levelButtons.length > 0) {
        levelButtons.forEach(button => {
            button.addEventListener('click', function() {
                const level = this.getAttribute('data-level');
                selectLevel(level);
            });
        });
    }
    
    // Configurar otros event listeners
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            if (registrationForm && levelSection) {
                registrationForm.style.display = 'none';
                levelSection.style.display = 'block';
            }
        });
    }
    
    if (backToBasicBtn) {
        backToBasicBtn.addEventListener('click', function() {
            selectLevel('basic');
        });
    }
    
    if (distanceSelect && poolLengthSelect) {
        distanceSelect.addEventListener('change', generateLapTimeFields);
        poolLengthSelect.addEventListener('change', generateLapTimeFields);
    }
    
    // Función para seleccionar nivel
    function selectLevel(level) {
        if (!levelSection || !registrationForm || !proLevelMessage) return;
        
        // Ocultar sección de selección de nivel
        levelSection.style.display = 'none';
        
        // Actualizar el badge de nivel seleccionado y el input hidden
        const levelBadge = document.getElementById('selected-level-badge');
        const levelInput = document.getElementById('level_input');
        
        if (levelBadge) {
            levelBadge.textContent = level.charAt(0).toUpperCase() + level.slice(1);
        }
        
        if (levelInput) {
            levelInput.value = level;
        }
        
        // Lógica según el nivel
        if (level === 'basic') {
            // Mostrar formulario para nivel básico
            registrationForm.style.display = 'block';
            proLevelMessage.style.display = 'none';
            
            // Mostrar/ocultar contenedores según el nivel
            toggleLevelContainers(level);
            
            // Generar campos para tiempos por vuelta
            generateLapTimeFields();
        } else {
            // Para niveles Pro y Elite, mostrar mensaje de suscripción
            registrationForm.style.display = 'none';
            proLevelMessage.style.display = 'block';
            
            // Actualizar el mensaje con el nivel seleccionado
            const premiumLevelSpan = document.getElementById('premium-level');
            if (premiumLevelSpan) {
                premiumLevelSpan.textContent = level.charAt(0).toUpperCase() + level.slice(1);
            }
        }
    }
    
    // Función para mostrar/ocultar contenedores según el nivel
    function toggleLevelContainers(level) {
        const basicTimeContainer = document.getElementById('basic-time-container');
        const advancedTimeContainer = document.getElementById('advanced-time-container');
        const eliteAnalysisContainer = document.getElementById('elite-analysis-container');
        
        if (basicTimeContainer) {
            basicTimeContainer.style.display = 'block';
        }
        
        if (advancedTimeContainer) {
            advancedTimeContainer.style.display = level === 'basic' ? 'none' : 'block';
        }
        
        if (eliteAnalysisContainer) {
            eliteAnalysisContainer.style.display = level === 'elite' ? 'block' : 'none';
        }
    }
    
    // Función para generar campos de tiempo por vuelta
    function generateLapTimeFields() {
        const distance = parseInt(distanceSelect.value);
        const poolLength = parseInt(poolLengthSelect.value.replace(/[^\d]/g, '')); // Extraer solo números
        const lapTimes = document.getElementById('lap-times');
        
        if (!lapTimes) return;
        
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
    
    // Inicialización
    // Generar campos iniciales para tiempos por vuelta si estamos en la página correcta
    if (document.querySelector('.level-selection-section')) {
        setTimeout(() => {
            if (document.getElementById('lap-times')) {
                generateLapTimeFields();
            }
        }, 0);
    }
}