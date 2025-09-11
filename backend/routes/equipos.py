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
equipos_bp = Blueprint('equipos', __name__)

#ponemos los endpoints es decir las funciones que va a ser nuestro programa por ejemplo solicitar datos, crear usuario, etc

#end point para el registro del equipo de maximo 6 como en los juegos 
@equipos_bp.route('/seleccion', methods=['POST'])
@jwt_required()
def registro():
    #obtenemos la identidad de nuestro usuario mediante su token
    current_user = get_jwt_identity()
    #solicitamos el nombre del pokemon
    data = request.get_json()
    nombre= data.get('nombre')
    cursor = get_db_connection()
    #hacemos la peticion para verificar si el pokemon existe mediante su nombre
    cursor.execute("SELECT id, nombre, tipoo FROM pokemones WHERE nombre =%s", (nombre,))
    #me devuelve el pokemon como tupla
    pokemon = cursor.fetchone()
    if not pokemon:
        return jsonify({"error":"Pokemon no encontrado"}), 404
    #verificamos que no tenga mas de 6 pokemones
    cursor.execute("SELECT COUNT(*) FROM equipo WHERE id_entrenador=%s", (current_user,))
    cantidad_fila=cursor.fetchone()[0]
    if cantidad_fila>=6:
        cursor.close()
        return jsonify({"error":"solo puedes tener 6"})
    #insertamos el pokemon en el equipo 
    cursor.execute("INSERT INTO `equipo`(`id_pokemon`, `id_entrenador`) VALUES (%s, %s)",(pokemon[0], current_user))
    cursor.connection.commit()
    #cerramos la peticion
    cursor.close()
    #mensaje de que ya fue agregado le ponemos pokemon[1] ya que es la posicion de nuestra tupla 
    return jsonify({"mensaje":f"El pokemon: {pokemon[1]} fue agregado a tu equipo"}), 201
#hacemos un endpoint para eliminar pokemones casi lo mismo que arriba pero un poco diferente 
@equipos_bp.route('/borrar', methods=["DELETE"])
@jwt_required()
def borrar():
    #obtenemos la identidad del usuario de nuevo 
    current_user = get_jwt_identity()
    #solicitamos el nombre del pokemon 
    data = request.get_json()
    nombre=data.get('nombre')
    cursor = get_db_connection()
    #hacemos la peticion
    cursor.execute("SELECT eq.id_pokemon, p.nombre FROM equipo eq INNER JOIN pokemones p ON eq.id_pokemon = p.id WHERE eq.id_entrenador=%s AND p.nombre = %s", (current_user, nombre))

    #lo devuelvo como tupla
    pokemon = cursor.fetchone()
    #si el pokemon no existe en nuestro equipo entonces pues no se puede borrar
    if not pokemon:
        cursor.close()
        return jsonify({"error":"Ese pokemon no esta en tu equipo"}), 404
    #y ya si si existe pues lo puedes eliminar y hacemos la peticion
    cursor.execute("DELETE FROM equipo WHERE id_entrenador=%s AND id_pokemon=%s",(current_user, pokemon[0]))
    #hacemos el commit
    cursor.connection.commit()
    #cerramos la conexion
    cursor.close()
    return jsonify({"mensaje":"Pokemon eliminado con exito"}), 200