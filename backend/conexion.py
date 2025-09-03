import requests
import mysql.connector
import time
#aqui me conecto con MYSQL de Phpmyadmin en XAMPP
conexion = mysql.connector.connect(
    host ="localhost",
    user ="root",
    password ="",
    database = "pokedex_db"
)

cursor = conexion.cursor() # cursor nos permite acceder a consultas de mySQL

#ahora esta funcion es para solicitar y obtener los datos de un pokemon 
def obtener_datos_pokemon(id_pokemon): 
    try:
        url=f"https://pokeapi.co/api/v2/pokemon/{id_pokemon}" #accedemos a la url y le ponemos /{id_pokemon} ya que cuando se identifica con el numero te da el pokemon basicamente
        response = requests.get(url) #hacemos la solicitud a la apien el protocolo HTTP GET 
        data = response.json() #le decimos que nos devuelva la respuesta en formato json

        # Elegir imagen pixel art si existe, si no, official-artwork
        foto = data['sprites']['front_default'] or data['sprites']['other']['official-artwork']['front_default']

        #obtener descripcion de cada pokemon
        url_especie=f"https://pokeapi.co/api/v2/pokemon-species/{id_pokemon}"
        response_especie = requests.get(url_especie)
        data_especie = response_especie.json()
        #vamos a agarrar la descripcion en inglés
        descripcion = next(
        (texto['flavor_text'].replace("\n", " ").replace("\f", " ") 
        for texto in data_especie['flavor_text_entries'] 
        if texto['language']['name'] == 'en'),
        "No description available"
        )

        pokemon = {
            'id':data['id'],
            'nombre':data['name'],
            'tipoo':data['types'][0]['type']['name'],
            'foto':foto,
            'ataque' : data['stats'][1]['base_stat'],
            'vida': data['stats'][0]['base_stat'],
            'altura':data['height']/10,
            'peso' : data['weight']/10,
            'velocidad' : data['stats'][5]['base_stat'],
            'descrip' : descripcion
        }#en esto cargamos todos los datos que queremos de los pokemones nombre,altura, peso, etc
        return pokemon
    except Exception as e:
        print(f"Error con pokemon {id_pokemon}: {e}")
        return None
    

#aqui cargamos de la region 1 hasta kalos o sea 721 pokemones
print("cargando los 721 pokemones")
for i in range(1,722):
    pokemon = obtener_datos_pokemon(i)

    if pokemon:
        insertar_pokemon = """INSERT IGNORE INTO pokemones (id,nombre,tipoo,foto,ataque,vida,altura,peso,velocidad, descrip) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        valores = (
            pokemon['id'],
            pokemon['nombre'],
            pokemon['tipoo'],
            pokemon['foto'],
            pokemon['ataque'],
            pokemon['vida'],
            pokemon['altura'],
            pokemon['peso'],
            pokemon['velocidad'],
            pokemon['descrip']
        )
        #le decimos que con el cursor agarre insertar_pokemon y en vez de los parentesis vacios con %s los rellene
        cursor.execute(insertar_pokemon,valores)
        #hacemos que se actualice la base de datos
        conexion.commit()
        #le ponemos que se actualice cada .05 seg para no saturar a la api
        print("pokemon cargado correctamente")
        time.sleep(0.05)

print("Se cargo correctamente la pokedex")
#evitar errores cerramos el cursor
cursor.close()
#cerramos la conexion con la base de datos
conexion.close()

