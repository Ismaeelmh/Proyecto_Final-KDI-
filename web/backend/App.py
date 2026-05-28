from flask import Flask, jsonify, redirect, render_template, request, session, send_from_directory, send_file  # Importar Flask y utilidades JSON
from flask_cors import CORS  # Permitir conexión con frontend
from werkzeug.security import generate_password_hash, check_password_hash  # Encriptar y verificar contraseñas
import mysql.connector  # Importar conector MySQL
import os
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JUEGOS_DIR = os.path.join(BASE_DIR, "..", "..", "Juegos")

@app.route('/Juegos/<path:filename>')
def juegos(filename):
    import mimetypes
    base_dir = "/home/ubuntu/Proyecto_Final-KDI-/Juegos"
    full_path = os.path.join(base_dir, filename)

    if not os.path.exists(full_path):
        return f"File not found: {filename}", 404

    mime_type, _ = mimetypes.guess_type(full_path)
    if not mime_type:
        mime_type = 'application/octet-stream'

    response = send_file(full_path, mimetype=mime_type)

    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'credentialless'
    response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


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

@app.route('/perfil')
def perfil_page():
    return render_template('perfil.html')

@app.route('/feedback')
def feedback_page():
    return render_template('feedback.html')


@app.route('/rankings')
def rankings_page():
    return render_template('rankings.html')

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


@app.route('/api/feedback/<juego>', methods=['GET'])
def obtener_feedback(juego):
    cursor = db.cursor(dictionary=True)

    query = """
    SELECT username, mensaje
    FROM feedback
    WHERE juego = %s
    ORDER BY id DESC
    """

    cursor.execute(query, (juego,))

    mensajes = cursor.fetchall()

    cursor.close()

    return jsonify(mensajes), 200

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

@app.route("/usuario")
def obtener_usuario():
    if "usuario_id" not in session:
        return jsonify({"error": "No login"}), 401

    return jsonify({
        "usuario_id": session["usuario_id"],
        "nombre": session["nombre"]
    })
    
@app.route("/guardar_puntuacion", methods=["POST"])
def guardar_puntuacion():
    try:
        datos = request.get_json()

        usuario_id = datos.get("usuario_id")
        juego = datos.get("juego")
        modo = datos.get("modo")
        puntuacion = datos.get("puntuacion")

        if not all([usuario_id, juego, modo, puntuacion]):
            return jsonify({"error": "Faltan datos"}), 400

        cursor = db.cursor()

        query = """
        INSERT INTO detalles_partida (usuario_id, juego, modo, puntuacion)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (usuario_id, juego, modo, puntuacion))
        db.commit()
        cursor.close()

        return jsonify({"ok": True}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "server error"}), 500


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)