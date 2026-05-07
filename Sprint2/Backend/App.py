from flask import Flask, jsonify, request, session  # Importar Flask y utilidades JSON
from flask_cors import CORS  # Permitir conexión con frontend
from werkzeug.security import generate_password_hash, check_password_hash  # Encriptar y verificar contraseñas
import mysql.connector  # Importar conector MySQL

app = Flask("juegos")  # Crear aplicación Flask
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
    return jsonify({"message": "Bienvenido a juegos"})  # Ruta principal


# REGISTRO
@app.route('/registro', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validar campos vacíos
    if not username or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    cursor = db.cursor(dictionary=True)

#VERIFICAR SI EL USUARIO O EMAIL YA EXISTE EN LA BASE DE DATOS 
    cursor.execute(query, (email, username))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        return jsonify({"error": "Usuario o email ya existe"}), 409

    # Encriptar contraseña
    password_hash = generate_password_hash(password)

    # Insertar usuario
    query = "INSERT INTO usuarios (username, email, password_hash) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, email, password_hash))

    db.commit()
    cursor.close()

    return jsonify({
        "message": "Usuario registrado correctamente",
        "user": {
            "username": username,
            "email": email
        }
    }), 201


# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Obtener datos enviados

    username = data.get("username")
    password = data.get("password")

    cursor = db.cursor(dictionary=True)  # Cursor tipo diccionario
   
    query = "SELECT * FROM usuarios WHERE username = %s"
    cursor.execute(query, (username,)) 
    
    user_found = cursor.fetchone()  # Buscar usuario
    cursor.close()

    # Verificar contraseña
    if user_found and check_password_hash(user_found["password_hash"], password):
        session["user"] = user_found["email"] # Guardar usuario en sesión
        return jsonify({
            "message": "Login correcto",
            "user": {
                "username": user_found["username"],
                "email": user_found["email"]
            }
        }), 200

    return jsonify({
        "message": "username o contraseña incorrectos"
    }), 401


# PROFILE
@app.route('/profile', methods=['POST'])
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


# MENU
@app.route('/menu', methods=['GET'])
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


if __name__ == '__main__':
    app.run(debug=True)  # Ejecutar servidor en modo debug