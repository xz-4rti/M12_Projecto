from flask import Flask, jsonify, render_template, request
from bd import obtener_jugadores, obtener_equipos, obtener_estadisticas
from auth import require_apikey, generar_y_guardar_apikey  

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/jugadores", methods=['GET'])
@require_apikey  
def get_jugadores():
    id_equipo = request.args.get('id_equipo')
    posicion = request.args.get('posicion')
    edad = request.args.get('edad')

    jugadores = obtener_jugadores(id_equipo, posicion, edad)

    if isinstance(jugadores, tuple) and jugadores[1] == 500:
        return jsonify(jugadores[0]), 500
    
    return jsonify(jugadores)

@app.route("/equipos", methods=['GET'])
@require_apikey
def get_equipos():
    abreviacion = request.args.get('abreviacion')
    nombre = request.args.get('nombre')
    ano_fundacion = request.args.get('ano_fundacion')
    ciudad = request.args.get('ciudad')

    equipos = obtener_equipos(abreviacion, ano_fundacion, nombre, ciudad)

    if isinstance(equipos, tuple) and equipos[1] == 500:
        return jsonify(equipos[0]), 500
    
    return jsonify(equipos)

@app.route("/estadisticas", methods=['GET'])
@require_apikey
def get_estadisticas():
    estadisticas = obtener_estadisticas()

    if isinstance(estadisticas, tuple) and estadisticas[1] == 500:
        return jsonify(estadisticas[0]), 500

    return jsonify(estadisticas)

@app.route("/generar_apikey", methods=['POST'])
def generar_apikey():
    id_usuario = request.json.get('id_usuario')
    
    if not id_usuario:
        return jsonify({'message': 'Se necesita un ID de usuario'}), 400

    nueva_apikey = generar_y_guardar_apikey(id_usuario)
    
    return jsonify({'message': 'Clave API generada', 'api_key': nueva_apikey})

if __name__ == "__main__":
    app.run(debug=True, port=5001, host='localhost')
