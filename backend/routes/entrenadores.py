from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt
import datetime
from config.db import get_db_connection
import traceback
import os
from dotenv import load_dotenv

#cargamos variables de entorno:
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
        #validar si ya existe el entrenador
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
    #obtenemos el hash del password es decir leemos la password normal pero le puse hash donde me va a guardar el hash o sea la contraenia cifrada y la posicion del usuario o sea nos va a devolver ('oiwjowjejfowj', id_usuario)
    stored_password_hash = cursor.fetchone()
    #cerramos el cursor
    cursor.close()

    #verificamos la contrasenia comparando la stored_password y la comparamos con el que le demos nosotros para ver si existe 
    if stored_password_hash and bcrypt.check_password_hash(stored_password_hash[0],password):
        #generamos el jason web token para cada entrenador le pondremos 24 hrs
        expires = datetime.timedelta(hours=24)

        access_token = create_access_token(
            identity=str(stored_password_hash[1]),
            expires_delta=expires
        )

        return jsonify({"accesToken":access_token}), 200
    else:
        return jsonify({"error":"credenciales incorrectas"}), 401
    
#hacemos un endpoint para el perfil para mostrar nombre, id y sus pokemones que escogio 
@entrenadores_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    #obtenemos la identidad de nuestro usuario mediante su token
    current_user = get_jwt_identity()
    #conexion a la base de datos
    cursor = get_db_connection()
    #obtener los datos del usuario 
    query = "SELECT id_usuario, nombre_entrenador FROM entrenadores WHERE id_usuario=%s"
    #le pedimos que ejecute nuestra peticion
    cursor.execute(query,(current_user,))
    #la jalamos como tupla o sea fila 
    entrenador_fila=cursor.fetchone()

    #le hacemos un inner join para saber que pokemones tiene cada entrenador
    cursor.execute("""SELECT p.id AS id_pokemon, p.nombre AS nombre_pokemon, p.foto AS foto FROM equipo eq INNER JOIN pokemones p ON eq.id_pokemon = p.id WHERE eq.id_entrenador = %s """, (current_user,))
    equipo_filas = cursor.fetchall()
    #cerramos la peticion
    cursor.close()
    #creo una variable que me ponga sus pokemones en filas
    equipo = []
    for fila in equipo_filas:
        equipo.append({
            "id":fila[0],
            "nombre":fila[1],
            "foto":fila[2]
            })

    #si el entrenador existe, que me pase todos sus datos
    if entrenador_fila:
        entrenador_info={
            "id_usuario":entrenador_fila[0],
            "nombre_entrenador":entrenador_fila[1],
            "equipo":equipo
        }
        return jsonify({"entrenador":entrenador_info}), 200
    else:
        return jsonify({"error":"entrenador no encontrado"}), 404
