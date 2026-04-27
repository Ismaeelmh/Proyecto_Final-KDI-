from flask import Flask, jsonify, request

app = Flask("Juegos")

@app.route('/')
def home():
    return jsonify({
        "mensaje": "API de juegos funcionando"
    })

@app.route('/api/saludo', methods=['GET'])
def juegos():
    return jsonify({
        "juegos": "Hola, esta es una API básica con Flask"
    })

@app.route('/api/sumar', methods=['POST'])
def sumar():
    data = request.get_json()

    num1 = data.get("num1", 0)
    num2 = data.get("num2", 0)

    return jsonify({
        "resultado": num1 + num2
    })

@app.route('/registro', methods=['GET'])
def registro_form():
    return """
    <h2>Registro</h2>

    <form action="/api/registro" method="post">
        <label>Email:</label><br>
        <input type="email" name="email"><br><br>

        <label>Username:</label><br>
        <input type="username" name="username"><br><br>

        <label>Password:</label><br>
        <input type="password" name="password"><br><br>

        <button type="submit">Enviar</button>
    </form>
    """
@app.route('/login', methods=['GET'])
def login_form():
    return """
    <h2>login</h2>

    <form action="/api/login" method="post">
        <label>Username:</label><br>
        <input type="username" name="username"><br><br>

        <label>Password:</label><br>
        <input type="password" name="password"><br><br>

        <button type="submit">Enviar</button>
    </form>
    """
if __name__ == '__main__':
    app.run(debug=True)


