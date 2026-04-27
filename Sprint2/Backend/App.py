from flask import Flask, jsonify, request  # added request

app = Flask("juegos ")  # Create Flask app

# Root route to test server
@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenido el juegos"
    })

# POST /registro endpoint
@app.route('/registro', methods=['POST'])
def registro():

    # Get JSON data from request
    data = request.get_json()

    # Simple simulated user creation
    user = {
        "name": data["name"],
        "email": data["email"]
    }

    return jsonify({
        "message": "Usuario registrado correctamente",
        "user": user
    }), 201

# Run server in debug mode
if __name__ == '__main__':
    app.run(debug=True)
