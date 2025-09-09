#este archivo nos permite conectar nuestro programa directamente a nuestra base de datos 
from flask_mysqldb import MySQL
import os 
from dotenv import load_dotenv

#cargamos variables de entorno 
load_dotenv()

#inciializamos flask_mysql
mysql=MySQL()

#configuramos el acceso a nuestra base de datos para nuestra app 
def init_db(app):
    #configuramos la base con la instancia de flask o sea nuestro archivo app
    app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
    app.config['MYSQL_USER'] = os.getenv("DB_USER")
    app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
    app.config['MYSQL_DB'] = os.getenv("DB_NAME")
    app.config['MYSQL_PORT'] = int(os.getenv("DB_PORT"))

    #INICIALIZAMOS LA CONEXION DE MYSQL 
    mysql.init_app(app)

#funcion para obtener el cursor a la base de datos 
def get_db_connection():
    #devuelve el cursor que nos permite interactuar con la base de datos 
    try:
        connection = mysql.connection
        return connection.cursor()
    except Exception as e:
        raise RuntimeError(f"Hay un error, no me puedo conectar a la base de datos {e}")