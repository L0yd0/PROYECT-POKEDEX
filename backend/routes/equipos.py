from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

#cargamos avriables de entorno:
load_dotenv()

#creamos el blueprint que es como si linkearamos esto con el app.py
equipos_bp = Blueprint('equipos', __name__)


#ponemos los endpoints es decir las funciones que va a ser nuestro programa por ejemplo solicitar datos, crear usuario, etc

#end point para el registro del equipo y eso me lo
@equipos_bp.route('/seleccion', methods=['POST'])
def registro():
    data = request.get_json()
    id_pokemon = data.get('id_pokemon')
    id_entrenador = data.get('id_entrenador')
