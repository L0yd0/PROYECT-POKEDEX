from flask import Blueprint, jsonify
import os
from dotenv import load_dotenv
from config.db import get_db_connection

#cargamos avriables de entorno:
load_dotenv()

#creamos el blueprint que es como si linkearamos esto con el app.py
pokemones_bp = Blueprint('pokemones', __name__)

#ponemos los endpoints es decir las funciones que va a ser nuestro programa por ejemplo solicitar datos, crear usuario, etc

#end point para que nos de los pokemones de la pokedex 
@pokemones_bp.route('/pokedex', methods=['GET'])
def obtener():
    #hacemos una conexion a la base de datos a traves de cursor 
    cursor = get_db_connection()
    #hacemos la consulta de nuestra base de datos 
    cursor.execute("SELECT `id`, `nombre`, `tipoo`, `foto`, `ataque`, `vida`, `altura`, `peso`, `velocidad`, `descrip` FROM `pokemones` WHERE 1")
    pokemones=cursor.fetchall() #lo manda como tupla 
    #cerramos la peticion con la base de datos
    cursor.close()
    #ponemos las columnas para que quede mas legible el json
    columnas = ["id", "nombre", "tipoo", "foto", "ataque", "vida", "altura", "peso", "velocidad", "descrip"]
    #declaramos el diccionario donde se va a guardar
    resultado=[]
    #hacemos un bucle para que los datos que consulte en mi base de pokemones se guarde en las filas 
    for fila in pokemones:
        #con esto agregamos cada resultado en el diccionario haciendo el append para agregar y el dict para que lo convierta a diccionario lo de adentro que es zip(columnas, filas) esto es para ordenar las filas y columnas por ejemplo de columnas "id" lo emparejee con el id de nuestra base de datos
        resultado.append(dict(zip(columnas, fila)))

    return jsonify({"pokemones":resultado})
    