from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

#cargamos avriables de entorno:
load_dotenv()

#creamos el blueprint que es como si linkearamos esto con el app.py
equipos_bp = Blueprint('equipos', __name__)


#ponemos los endpoints es decir las funciones que va a ser nuestro programa por ejemplo solicitar datos, crear usuario, etc


