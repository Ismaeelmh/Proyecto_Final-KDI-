from flask import Flask, jsonify, request

app = Flask("juegos")

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


if __name__ == '__main__':
    app.run(debug=True)
