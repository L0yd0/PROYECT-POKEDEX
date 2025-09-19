from flask import Blueprint, jsonify, request
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
    #parametros de paginacion
    page = request.args.get('page', 1, type=int)
    per_page = 12
    #calculo el offset
    offset=(page-1)*per_page
    #hacemos una conexion a la base de datos a traves de cursor 
    cursor = get_db_connection()
    #hacemos la consulta de nuestra base de datos 
    cursor.execute("SELECT `id`, `nombre`, `tipoo`, `foto`, `ataque`, `vida`, `altura`, `peso`, `velocidad`, `descrip` FROM `pokemones` WHERE 1 LIMIT %s OFFSET %s", (per_page,offset))
    pokemones=cursor.fetchall() #lo manda como tupla 
    #obtener el numero total de pokemon para calcular las pags
    cursor.execute("SELECT COUNT(*) FROM `pokemones` WHERE 1")
    total_pokemones = cursor.fetchone()[0]
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
    
    total_pages = (total_pokemones + per_page-1) // per_page

    return jsonify({"pokemones":resultado,
                    "pagination":{
                        "current_page":page,
                        "per_page":per_page,
                        "total_pages":total_pages,
                        "total_pokemones":total_pokemones,
                        "has_next":page<total_pages,
                        "has_previous":page>1
                    }
                    })
    