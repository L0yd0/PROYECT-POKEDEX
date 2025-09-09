from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt
import datetime
from config.db import get_db_connection
import traceback
import os
from dotenv import load_dotenv

#cargamos avriables de entorno:
load_dotenv()

#creamos el blueprint que es como si linkearamos esto con el app.py
entrenadores_bp = Blueprint('entrenadores', __name__)

#incializamos el bcryt para generar los hashes de usuario
bcrypt = Bcrypt()
#ponemos los endpoints es decir las funciones que va a ser nuestro programa por ejemplo solicitar datos, crear usuario, etc


#end point para el registro de los entrenadores 
@entrenadores_bp.route('/registrar', methods=['POST'])
def registro():
    #obtengo los datos del json medinate el metodo post 
    data = request.get_json()
    nombre_entrenador = data.get('nombre_entrenador')
    password = data.get('password')

    #validamos que si nos haya dado su nombre y contrasenia y si no pues le lanzamos un error 400 
    if not nombre_entrenador or not password:
        return jsonify({"msg":"Faltan datos de entrenador"}), 400 
    
    #nos conectamos a la base de datos
    cursor = get_db_connection()

    try:
        #verifico que mi entrenador no se cree 2 veces
        cursor.execute("SELECT * FROM entrenadores where nombre_entrenador = %s", (nombre_entrenador,))
        existing_entrenador = cursor.fetchone()

        if existing_entrenador:
            return jsonify({"error":"Ese entrenador ya existe"}), 400
        #hash a la contrasenia usando bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        #insertar el usuario mediante sql
        cursor.execute('''INSERT INTO entrenadores (nombre_entrenador, password) VALUES (%s, %s)''',(nombre_entrenador, hashed_password))
        #hacemos el commit 
        cursor.connection.commit()
        return jsonify({"mensaje":"El entrenador se creo con exito"}), 201
    
    except Exception as e:
        return jsonify({"error":f"Error al querer registrar entrenador {str(e)}"}), 500
    finally:
        #cerramos la conexion a la base de datos despues de consultarlo
        cursor.close()   
#hacemos un endpoint para que el usuario inicie sesion es decir el login 
@entrenadores_bp.route('/login', methods=['POST'])
def login():
    #solicitamos los datos en formato json
    data = request.get_json()
    nombre_entrenador = data.get('nombre_entrenador')
    password = data.get('password')
    #validamos que si pasen los datos'
    if not nombre_entrenador or not password:
        return jsonify({"error":"Faltan datos de entrenador"}), 400
    #conectamos con la base de datos 
    cursor = get_db_connection()

    #consultamos los datos del entrenador que se intenta loggear
    cursor.execute("SELECT password, id_usuario FROM entrenadores where nombre_entrenador = %s", (nombre_entrenador,))
    #obtenemos el hash del password es decir leemos la password normal pero le puse hash donde me va a guardar el hash o sea la contraenia cifrada y la posicion del usuario 
    stored_password_hash = cursor.fetchone()
    #cerramos el cursor
    cursor.close()

    #verificamos la contrasenia comparando la stored_password y la comparamos con el que le demos nosotros para ver si existe 
    if stored_password_hash and bcrypt.check_password_hash(stored_password_hash[0],password):
        #generamos el jason web token para cada entrenador le pondremos 1 anio
        expires = datetime.timedelta(hours=24)