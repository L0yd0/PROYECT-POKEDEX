from flask import Flask #importamos flask
from flask_jwt_extended import JWTManager #importamos el jwt
import os #importamos para interactue con el sistema operativo 
from dotenv import load_dotenv #para que podamos usar las variables de entorno

#cargamos las variables de entorno desde .env se carga para transmitirle que de mi archivo .env me jale todas mis variables de entorno 
load_dotenv()

#creamos la app de pokemon a traves de esta funcion 
def create_app():
    #instanciamos la app o sea le decimos cual sera el archivo principal, en este caso es app.py 
    app = Flask(__name__)
    #LE DIJIMOS QUE ACCEDA A LA JWT QUE PREVIAMENTE PUSE EN MI ARCHIVO .ENV 
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    #le decimos que use el jwt para nuestra app 
    jwt = JWTManager(app)

    return app #nos retorna la app 

#creamos la aplicacion y la arrancamos:
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080)) #AQUI LE DECIMOS QUE DE NUESTRO ARCHIVO .ENV EL PUERTO VA A SER EL MISMO QUE PUSIMOS EN NUESTRO ARCHIVO Y QUE LA TOME PARA NUESTRA VARIABLE port y le decimos que el valor lo convierta a entero por si entra algun inconveniente

    app.run(host="0.0.0.0", port = port, debug=True)#esto basicamente le estoy diciendo que corra mi app con run donde el host sera 0.0.0.0 para que acceda a cualquier direccion ip, port pues el port que defini que es el 8080 que esta en mi .env y debug true significa que autorecarga la app cada vez que le doy guardar o cambio algo del codigo









