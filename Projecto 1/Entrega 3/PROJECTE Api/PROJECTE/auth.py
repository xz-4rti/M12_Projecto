from functools import wraps
from flask import request, jsonify
import mysql.connector
import bcrypt
import os

def verificar_apikey(apikey_proporcionada):
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        port=3306,
        database='proyecto_nba'
    )
    cursor = connection.cursor(dictionary=True)

    try:
        query = "SELECT api_key_hash FROM api_keys"
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            for row in result:
                api_key_hash = row['api_key_hash']
                if bcrypt.checkpw(apikey_proporcionada.encode('utf-8'), api_key_hash.encode('utf-8')):
                    return True
            return False
        else:
            return False
    except mysql.connector.Error as e:
        return False
    finally:
        cursor.close()
        connection.close()


def require_apikey(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        apikey_proporcionada = request.headers.get('X-API-KEY')
        if not apikey_proporcionada or not verificar_apikey(apikey_proporcionada):
            return jsonify({'message': 'API key no válida o ausente'}), 403
        return f(*args, **kwargs)
    return decorated_function

def generar_apikey():
    return os.urandom(16).hex()

def encriptar_apikey(apikey):
    return bcrypt.hashpw(apikey.encode('utf-8'), bcrypt.gensalt()).decode()

def guardar_apikey_encriptada(id_usuario, apikey_encriptada):
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        port=3306,
        database='proyecto_nba'
    )
    cursor = connection.cursor()

    try:
        query = "INSERT INTO api_keys (id_usuario, api_key_hash) VALUES (%s, %s)"
        cursor.execute(query, (id_usuario, apikey_encriptada))
        connection.commit()

    finally:
        cursor.close()
        connection.close()

def generar_y_guardar_apikey(id_usuario):
    apikey = generar_apikey()
    apikey_encriptada = encriptar_apikey(apikey)

    guardar_apikey_encriptada(id_usuario, apikey_encriptada)

    return apikey


