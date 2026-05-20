from flask import Flask, jsonify, redirect, render_template, request, session  # Importar Flask y utilidades JSON
from flask_cors import CORS  # Permitir conexión con frontend
from werkzeug.security import generate_password_hash, check_password_hash  # Encriptar y verificar contraseñas
import mysql.connector  # Importar conector MySQL

app = Flask(__name__, template_folder="../frontend", static_folder="../frontend") # Crear aplicación Flask
CORS(app)  # Activar CORS


app.secret_key = "saguacate" # Clave secreta para sesiones


# Conexión con MySQL en servidor EC2
db = mysql.connector.connect(
    host="3.234.171.83",
    user="visualcode",
    password="saguacate",
    database="saguacate",
    port=3306
)

print("Conexión MySQL AWS exitosa")  # Confirmar conexión

@app.route('/')
def home():
    return render_template('registro.html') # Ruta principal

# FRONTEND ROUTES (HTML)
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/registro')
def registro_page():
    return render_template('registro.html')

@app.route('/menu')
def menu_page():
    return render_template('menu.html')


# REGISTRO
@app.route('/api/registro', methods=['POST'])
def register():
    data = request.get_json()  # Obtener datos enviados 

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validar campos vacíos
    if not username or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    password_hash = generate_password_hash(password)  # Encriptar contraseña

    cursor = db.cursor()  # Crear cursor SQL
    query = "INSERT INTO usuarios (username, email, password_hash) VALUES (%s, %s, %s)"
    valores = (username, email, password_hash)

    cursor.execute(query, valores)  # Ejecutar inserción
    db.commit()  # Guardar cambios
    cursor.close()  # Cerrar cursor

    return jsonify({
        "message": "Usuario registrado correctamente",
        "user": {
            "username": username,
            "email": email
        }
    }), 201


# LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # Validate input
    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    cursor = db.cursor(dictionary=True)

    # Find user by username
    query = "SELECT * FROM usuarios WHERE username = %s"
    cursor.execute(query, (username,))
    user_found = cursor.fetchone()
    cursor.close()

    # User not found
    if not user_found:
        return jsonify({"error": "Usuario no existe"}), 401

    # Wrong password
    if not check_password_hash(user_found["password_hash"], password):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    # Save session / Juegos
    session["usuario_id"] = user_found["id"]
    session["nombre"] = user_found["username"]

    return jsonify({
        "message": "Login correcto",
        "user": {
            "username": user_found["username"],
            "email": user_found["email"]
        }
    }), 200


# PROFILE
@app.route('/api/profile', methods=['POST'])
def profile():
    data = request.get_json()  # Obtener email enviado

    email = data.get("email")

    cursor = db.cursor(dictionary=True)  # Crear cursor SQL
    query = "SELECT username, email FROM usuarios WHERE email = %s"
    cursor.execute(query, (email,))
    user_found = cursor.fetchone()  # Buscar perfil
    cursor.close()

    if user_found:
        return jsonify({
            "message": "Perfil encontrado",
            "profile": user_found
        }), 200

    return jsonify({
        "message": "Usuario no encontrado"
    }), 404

# ACTUALIZAR PROFILE
@app.route('/api/profile/update', methods=['PUT'])
def update_profile():

    # Obtener datos enviados
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validar datos
    if not username or not email or not password:

        return jsonify({
            "error": "Faltan datos"
        }), 400

    # Encriptar nueva contraseña
    password_hash = generate_password_hash(password)

    # Crear cursor SQL
    cursor = db.cursor()

    # Actualizar perfil
    query = """
    UPDATE usuarios
    SET email = %s, password_hash = %s
    WHERE username = %s
    """

    valores = (email, password_hash, username)

    # Ejecutar query
    cursor.execute(query, valores)

    # Guardar cambios
    db.commit()

    cursor.close()

    return jsonify({
        "message": "Perfil actualizado correctamente"
    }), 200


# MENU
@app.route('/api/menu', methods=['GET'])
def menu():

    menu_options = [
        "Iniciar Juego",
        "Perfil",
        "Cerrar Sesión"
    ]  # Opciones del menú

    return jsonify({
        "message": "Menú principal",
        "options": menu_options
    }), 200

# SISTEMA DE FEEDBACK Por cada juego
@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.get_json()

    # check JSON body exists
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    username = data.get("username")
    mensaje = data.get("mensaje")
    juego = data.get("juego")

    # allowed games
    JUEGOS_VALIDOS = ["buscaminas", "serpiente"]

    # validations
    if not username:
        return jsonify({"error": "Falta el username"}), 400

    if not mensaje:
        return jsonify({"error": "Falta el mensaje"}), 400

    if not juego:
        return jsonify({"error": "Falta el juego"}), 400

    if juego not in JUEGOS_VALIDOS:
        return jsonify({"error": "Juego inválido"}), 400

    if len(mensaje) < 3:
        return jsonify({"error": "Mensaje muy corto"}), 400

    if len(mensaje) > 500:
        return jsonify({"error": "Mensaje muy largo"}), 400

    # insert into MySQL
    try:
        cursor = db.cursor()

        query = """
        INSERT INTO feedback (username, mensaje, juego)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (username, mensaje, juego))
        db.commit()

        return jsonify({"message": "Feedback enviado correctamente"}), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": "Error al guardar feedback"}), 500

    finally:
        cursor.close()

# API USERS
@app.route('/api/users', methods=['GET'])
def get_users():

    return jsonify({
        "message": "API users funcionando"
    }), 200


# API USERS MYSQL
@app.route('/api/users/mysql', methods=['GET'])
def get_users_mysql():

    # Crear cursor SQL
    cursor = db.cursor(dictionary=True)

    # Query obtener usuarios
    query = "SELECT id, username, email FROM usuarios"

    cursor.execute(query)

    users = cursor.fetchall()

    cursor.close()

    return jsonify({
        "users": users
    }), 200


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)