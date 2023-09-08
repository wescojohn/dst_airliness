import requests
from pymongo import MongoClient

api_key = "b26fc856-37fa-414d-a85f-3c51d6c007d4"
url = f"https://airlabs.co/api/v9/delays?delay=60&type=departures&api_key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()['response']

    if data:
        # print(f"Nombre de vols à insérer : {data}")

        # Connexion à MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["dst_airliness"]

        # Sélectionnez ou créez une collection
        collection = db["flight_delay"]

        # Insérer chaque vol dans la collection
        collection.insert_many(data)
        
        print("Données insérées dans MongoDB")
    else:
        print("Aucune donnée de vol à insérer")
else:
    print("Erreur lors de la requête HTTP")
