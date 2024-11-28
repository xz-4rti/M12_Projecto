import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        connection = mysql.connector.connect(
            user="root",
            password="",
            host="127.0.0.1",
            port=3306,
            database="proyecto_nba",
        )
        print("Conexión a la base de datos establecida.")
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def obtener_jugadores(id_equipo=None, posicion=None, edad=None):
    connection = crear_conexion()
    if connection is None:
        return {"error": "Error en la conexión a la base de datos"}, 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT nombre, id_equipo, edad, posicion FROM jugadores WHERE 1=1"
        params = []

        if id_equipo:
            query += " AND id_equipo = %s"
            params.append(id_equipo)

        if posicion:
            query += " AND posicion = %s"
            params.append(posicion)

        if edad:
            query += " AND edad = %s"
            params.append(edad)

        cursor.execute(query, tuple(params))
        data = cursor.fetchall()

    except Error as e:
        print(f"Error al ejecutar la consulta en jugadores: {e}")
        return {"error": "Error en la consulta de la base de datos"}, 500

    finally:
        cursor.close()
        connection.close()

    return data

def obtener_equipos(abreviacion=None, ano_fundacion=None, nombre=None, ciudad=None):
    connection = crear_conexion()
    if connection is None:
        return {"error": "Error en la conexión a la base de datos"}, 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT abreviacion, nombre, ciudad, ano_fundacion FROM equipos WHERE 1=1"
        params = []

        if abreviacion:
            query += " AND abreviacion = %s"
            params.append(abreviacion)

        if nombre:
            query += " AND nombre = %s"
            params.append(nombre)

        if ano_fundacion:
            query += " AND ano_fundacion = %s"
            params.append(ano_fundacion)

        if ciudad:
            query += " AND ciudad = %s"
            params.append(ciudad)

        cursor.execute(query, tuple(params))
        data = cursor.fetchall()

    except Error as e:
        print(f"Error al ejecutar la consulta en equipos: {e}")
        return {"error": "Error en la consulta de la base de datos"}, 500

    finally:
        cursor.close()
        connection.close()

    return data

def obtener_estadisticas():
    connection = crear_conexion()
    if connection is None:
        return {"error": "Error en la conexión a la base de datos"}, 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT jugadores.nombre, estadisticas.minutos_jugados, estadisticas.porcentaje_tl, 
               estadisticas.porcentaje_triples, estadisticas.puntos_totales
        FROM estadisticas
        JOIN jugadores ON estadisticas.id_jugador = jugadores.id
        """
        cursor.execute(query)
        data = cursor.fetchall()

    except Error as e:
        print(f"Error al ejecutar la consulta en estadisticas: {e}")
        return {"error": "Error en la consulta de la base de datos"}, 500

    finally:
        cursor.close()
        connection.close()

    return data
