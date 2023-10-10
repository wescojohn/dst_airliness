import requests
from pymongo import MongoClient

api_key = "b26fc856-37fa-414d-a85f-3c51d6c007d4"
url = f"https://airlabs.co/api/v9/delays?delay=60&type=departures&api_key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()['response']

    if data:
        # Connexion à MongoDB
        client = MongoClient(host='mongodb', port=27017)
        db = client["dst_airliness"]

        # Nom de la collection
        collection_name = "flight_delay"

        # Vérifier si la collection existe
        if collection_name in db.list_collection_names():
            db[collection_name].drop()
            print(f"La collection '{collection_name}' existante a été supprimée")

        # Sélectionner ou créer une nouvelle collection
        collection = db[collection_name]

        # Insérer chaque vol dans la collection
        collection.insert_many(data)

        print("Données insérées dans MongoDB")
    else:
        print("Aucune donnée de vol à insérer")
else:
    print("Erreur lors de la requête HTTP")
