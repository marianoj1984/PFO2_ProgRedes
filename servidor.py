from flask import Flask, request, jsonify, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ---- BASE DE DATOS ----
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

init_db()

# ---- ENDPOINTS ----
@app.route('/registro', methods=['POST'])
def registro():
    data = request.json
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')
    if not usuario or not contraseña:
        return {'error': 'Usuario y contraseña requeridos'}, 400
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    password_hash = generate_password_hash(contraseña)
    try:
        c.execute("INSERT INTO usuarios (usuario, password_hash) VALUES (?,?)", (usuario, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return {'error': 'Usuario ya existe'}, 400
    conn.close()
    return {'mensaje': 'Usuario registrado exitosamente'}, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT password_hash FROM usuarios WHERE usuario=?", (usuario,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[0], contraseña):
        return {'mensaje': 'Inicio de sesión exitoso'}, 200
    return {'error': 'Usuario o contraseña incorrectos'}, 401

@app.route('/tareas', methods=['GET'])
def tareas():
    html = """
    <html>
    <head><title>Tareas</title></head>
    <body><h1>Bienvenido al Gestor de Tareas</h1></body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
