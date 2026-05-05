from flask import Flask, jsonify, request

app = Flask("juegos")
app.config['JSON_AS_ASCII'] = False  # Mostrar caracteres especiales correctamente


# Simulación de usuarios (más adelante esto vendrá de la BD)
users = [
    {
        "email": "juan@gmail.com",
        "password": "1234",
        "name": "Juan"
    }
]

@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenido a juegos"
    })

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    user = {
        "name": data["name"],
        "email": data["email"]
    }

    password_hash = generate_password_hash(password)
   
    conexion = conexion_sql()
    cursor = conexion.cursor()


    query = "INSERT INTO usuarios (username, email, password_hash) VALUES (%s, %s, %s)"


    valores = (username, email, password_hash)
   
    cursor.execute(query, valores)


    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({
        "message": "Usuario registrado correctamente",
        "user": user
    }), 201



# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Buscar usuario
    user_found = None
    for user in users:
        if user["email"] == email and user["password"] == password:
            user_found = user
            break
    
    password_hash = generate_password_hash(password)
   
    conexion = conexion_sql()
    cursor = conexion.cursor()


    query = "INSERT INTO usuarios (username, email, password_hash) VALUES (%s, %s, %s)"


    valores = (username, email, password_hash)
   
    cursor.execute(query, valores)


    conexion.commit()
    cursor.close()
    conexion.close()

    if user_found:
        return jsonify({
            "message": "Login correcto",
            "user": {
                "name": user_found["name"],
                "email": user_found["email"]
            }
        }), 200

    return jsonify({
        "message": "Email o contraseña incorrectos"
    }), 401

# PROFILE
@app.route('/profile', methods=['POST'])
def profile():
    data = request.get_json()

    email = data.get("email")

    # Buscar usuario por email
    user_found = None
    for user in users:
        if user["email"] == email:
            user_found = user
            break

    if user_found:
        return jsonify({
            "message": "Perfil encontrado",
            "profile": {
                "name": user_found["name"],
                "email": user_found["email"]
            }
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
    ]
    password_hash = generate_password_hash(password)
   
    conexion = conexion_sql()
    cursor = conexion.cursor()


    query = "INSERT INTO usuarios (username, email, password_hash) VALUES (%s, %s, %s)"


    valores = (username, email, password_hash)
   
    cursor.execute(query, valores)


    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({
        "message": "Menú principal",
        "options": menu_options
    }), 200 

if __name__ == '__main__':
    app.run(debug=True)
