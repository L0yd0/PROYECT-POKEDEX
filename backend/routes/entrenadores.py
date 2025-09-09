from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

#cargamos avriables de entorno:
load_dotenv()

#creamos el blueprint que es como si linkearamos esto con el app.py
entrenadores_bp = Blueprint('entrenadores', __name__)


#ponemos los endpoints es decir las funciones que va a ser nuestro programa por ejemplo solicitar datos, crear usuario, etc

#end point para el registro del entrenador y eso me lo
@entrenadores_bp.route('/registrar', methods=['POST'])
def registro():
    data = request.get_json()
    nombre_entrenador = data.get('nombre_entrenador')
    password = data.get('password')