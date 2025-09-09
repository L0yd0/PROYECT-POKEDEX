from flask import Blueprint, request, jsonify
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
    cursor = get_db_connection 
    return "ruta de mis pokemones"