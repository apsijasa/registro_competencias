/**
 * SWIM ANALYSIS - JavaScript común para todas las páginas
 * Este archivo contiene funcionalidades generales que se utilizan en toda la aplicación
 */

document.addEventListener('DOMContentLoaded', function() {
    // Manejo de la navegación móvil
    setupMobileNavigation();
    
    // Inicialización de tooltips y popovers si se usa Bootstrap
    initBootstrapComponents();
    
    // Manejo de alertas flash
    setupFlashAlerts();
    
    // Inicialización de formularios
    setupForms();
    
    // Scroll suave para enlaces internos
    setupSmoothScroll();
});

/**
 * Configura la navegación para dispositivos móviles
 */
function setupMobileNavigation() {
    const toggler = document.querySelector('.navbar-toggler');
    const collapse = document.querySelector('.navbar-collapse');

    if (toggler && collapse) {
        toggler.addEventListener('click', function() {
            collapse.classList.toggle('show');
        });

        // Cerrar el menú cuando se hace clic en un enlace
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (collapse.classList.contains('show')) {
                    collapse.classList.remove('show');
                }
            });
        });

        // Manejo de dropdowns en móvil
        const dropdowns = document.querySelectorAll('.dropdown');
        dropdowns.forEach(dropdown => {
            const toggle = dropdown.querySelector('.dropdown-toggle');
            if (toggle) {
                toggle.addEventListener('click', function(e) {
                    if (window.innerWidth < 992) {
                        e.preventDefault();
                        dropdown.classList.toggle('show');
                        
                        // Mostrar/ocultar el menú dropdown
                        const dropdownMenu = dropdown.querySelector('.dropdown-menu');
                        if (dropdownMenu) {
                            if (dropdown.classList.contains('show')) {
                                dropdownMenu.style.display = 'block';
                            } else {
                                dropdownMenu.style.display = 'none';
                            }
                        }
                    }
                });
            }
        });
    }
}

/**
 * Inicializa componentes de Bootstrap si están disponibles
 */
function initBootstrapComponents() {
    // Inicializar tooltips si existe la función
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }
    
    // Inicializar popovers si existe la función
    if (typeof bootstrap !== 'undefined' && bootstrap.Popover) {
        const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
        popovers.forEach(popover => {
            new bootstrap.Popover(popover);
        });
    }
}

/**
 * Configura el comportamiento de las alertas flash
 */
function setupFlashAlerts() {
    // Cerrar automáticamente las alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            // Verificar si el alert aún existe en el DOM
            if (document.body.contains(alert)) {
                // Si Bootstrap está cargado, usar su API para cerrar
                if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                    new bootstrap.Alert(alert).close();
                } else {
                    // De lo contrario, simplemente ocultar el elemento
                    alert.style.opacity = '0';
                    setTimeout(() => {
                        alert.style.display = 'none';
                    }, 300);
                }
            }
        }, 5000);
    });
}

/**
 * Configura comportamientos para los formularios
 */
function setupForms() {
    // Validación del lado del cliente
    const forms = document.querySelectorAll('form:not(.no-validate)');
    forms.forEach(form => {
        // Solo validar si no tiene la clase 'no-validate'
        if (!form.classList.contains('no-validate')) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                
                form.classList.add('was-validated');
                
                // Validaciones personalizadas
                validatePasswordMatch(form);
            });
        }
    });
    
    // Mascaras para inputs
    setupInputMasks();
}

/**
 * Valida que las contraseñas coincidan
 * @param {HTMLFormElement} form Formulario que contiene los campos de contraseña
 */
function validatePasswordMatch(form) {
    const password = form.querySelector('input[name="password"]');
    const confirmPassword = form.querySelector('input[name="confirm_password"]');
    
    if (password && confirmPassword) {
        if (password.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity('Las contraseñas no coinciden');
        } else {
            confirmPassword.setCustomValidity('');
        }
    }
}

/**
 * Configura máscaras para campos de entrada
 */
function setupInputMasks() {
    // Implementar máscaras si son necesarias
    // Por ejemplo, para campos de teléfono, tarjetas de crédito, etc.
}

/**
 * Configura el desplazamiento suave para enlaces internos
 */
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]:not([data-bs-toggle])').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            
            // No hacer nada si el href es solo "#"
            if (targetId === '#') return;
            
            e.preventDefault();
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Desplazamiento suave
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Ajustar por el header fijo
                    behavior: 'smooth'
                });
                
                // Actualizar la URL sin recargar la página
                window.history.pushState(null, null, targetId);
            }
        });
    });
}