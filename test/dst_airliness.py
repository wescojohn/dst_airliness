import requests
import json

api_key = "b26fc856-37fa-414d-a85f-3c51d6c007d4"
url = f"https://airlabs.co/api/v9/flights?api_key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    flight_data = response.json()

    with open("flight_data.json", "w") as json_file:
        json.dump(flight_data, json_file, indent=4)
        
    print("Données de vol stockées dans le fichier 'flight_data.json'")
else:
    print("Erreur lors de la requête HTTP")
