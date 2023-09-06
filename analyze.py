import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient(host='localhost', port=27017)
db = client["dst_airliness"]
collection = db["flight_collection"]

# Parcourez les données de vol dans MongoDB et calculez le temps au sol
for flight in collection.find():
    if flight['status'] == 'landed':
        # L'avion est au sol, enregistrez l'heure d'arrivée
        arrival_time = flight['updated']
    elif flight['status'] == 'scheduled':
        # L'avion est programmé, enregistrez l'heure de départ prévue
        departure_time = flight['updated']

        # Calculez le temps au sol en soustrayant l'heure de départ de l'heure d'arrivée
        time_on_ground = arrival_time - departure_time

        # Mettez à jour MongoDB avec le temps au sol calculé
        collection.update_one({'_id': flight['_id']}, {'$set': {'time_on_ground': time_on_ground}})

# Charger les données depuis MongoDB
cursor = collection.find()
df = pd.DataFrame(list(cursor))

# Analyse 1 : Temps moyen au sol par compagnie
avg_ground_time = df.groupby('airline_icao')['time_on_ground'].mean()

# Affichage des résultats de l'analyse 1
print("Analyse 1 : Temps moyen au sol par compagnie")
print(avg_ground_time)

# Analyse 2 : Distribution des avions par aéroport d'arrivée
arrivals_distribution = df.groupby(['airline_icao', 'arr_icao']).size().unstack(fill_value=0)

# Affichage des résultats de l'analyse 2
print("\nAnalyse 2 : Distribution des avions par aéroport d'arrivée")
print(arrivals_distribution)

# Visualisation de la distribution des avions par aéroport d'arrivée
arrivals_distribution.plot(kind='bar', stacked=True)
plt.xlabel('Compagnies Aériennes')
plt.ylabel('Nombre d\'avions')
plt.title('Distribution des avions par compagnie dans les aéroports d\'arrivée')
plt.legend(title='Aéroports d\'arrivée')
plt.show()

# Fermeture de la connexion MongoDB
client.close()
