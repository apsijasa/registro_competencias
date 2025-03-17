import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('registro_competencia.db')
conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
cursor = conn.cursor()

# Mostrar todas las tablas
print("=== TABLAS ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(table['name'])

# Mostrar usuarios
print("\n=== USUARIOS ===")
cursor.execute("SELECT id, email, first_name, last_name FROM user;")
users = cursor.fetchall()
for user in users:
    print(f"ID: {user['id']}, Email: {user['email']}, Nombre: {user['first_name']} {user['last_name']}")

# Mostrar registros de prueba gratuita
print("\n=== REGISTROS DE PRUEBA GRATUITA ===")
cursor.execute("SELECT id, email, first_name, last_name FROM free_trial_registration;")
registrations = cursor.fetchall()
for reg in registrations:
    print(f"ID: {reg['id']}, Email: {reg['email']}, Nombre: {reg['first_name']} {reg['last_name']}")

# Cerrar conexión
conn.close()