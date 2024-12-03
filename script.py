from pymongo import MongoClient
import requests
import json
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de OpenWeather API
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Variable de entorno para API Key
CITY = "Madrid"  # Cambia por la ciudad deseada
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
DB_NAME = os.getenv("COSMOS_DB_NAME")  # Variable de entorno para la base de datos
COLLECTION_NAME = os.getenv("COSMOS_COLLECTION_NAME")  # Nombre de la colección
CONNECTION = os.getenv("COSMOS_CONNECTION_STRING")  # Variable de entorno para la conexión a Cosmos DB

print(CONNECTION)

# Función para insertar datos en Cosmos DB
def insert_weather_data(client, data):
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    document_id = collection.insert_one(data).inserted_id
    print(f"Documento insertado con _id: {document_id}")

# Función para obtener datos meteorológicos
def get_weather_data():
    try:
        response = requests.get(WEATHER_URL)
        if response.status_code == 200:
            weather_data = response.json()
            # Formatear los datos
            formatted_data = {
                "city": weather_data["name"],
                "temperature": weather_data["main"]["temp"],
                "weather": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "pressure": weather_data["main"]["pressure"],
                "wind_speed": weather_data["wind"]["speed"],
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            return formatted_data
        else:
            print(f"Error al obtener los datos: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return None

# Bucle infinito para recopilar e insertar datos
while True:
    client = MongoClient(CONNECTION)
    weather_data = get_weather_data()
    if weather_data:
        print("Datos obtenidos del clima:")
        print(weather_data)
        insert_weather_data(client, weather_data)
        print("Datos insertados exitosamente en Cosmos DB")
    else:
        print("No se pudieron obtener los datos del clima.")
    
    # Pausa entre iteraciones (5 minutos)
    time.sleep(20)
