from flask import Flask, Response 
import folium
from folium import DivIcon
from pymongo import MongoClient
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import io

app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient(host='mongodb', port=27017)
db = client["dst_airliness"]
collection = db["flight_collection"]
collection_flight_delay = db["flight_delay"]

# Remplacez les informations de connexion par les vôtres
db_user = 'root'
db_password = 'root'
db_host = 'mysql'
db_name = 'dst_airliness'

# Créez une connexion à la base de données avec SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

# Chargez les données depuis la table airports
df_airports = pd.read_sql("SELECT * FROM airports", engine)

# Chargez les données depuis la table airlines
df_airlines = pd.read_sql("SELECT * FROM airlines", engine)

# Chargez les données depuis MongoDB
df_flight = pd.DataFrame(list(collection.find()))
df_flight_delay = pd.DataFrame(list(collection_flight_delay.find()))

@app.route('/')
def show_flight_map():
    # Créez une carte Folium centrée sur une position de départ
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Parcourez les données de vol dans la base de données
    for flight in collection.find():
        lat = flight['lat']
        lng = flight['lng']
        flight_number = flight.get('flight_number', 'N/A')

        # Créez une icône de marqueur personnalisée (avion)
        icon = DivIcon(
            icon_size=(20, 20),
            icon_anchor=(10, 10),
            html=f'<div style="font-size: 12px; color: red;">✈️</div>'
        )

        # Ajoutez un marqueur pour chaque vol sur la carte avec une pop-up
        folium.Marker(
            [lat, lng],
            icon=icon,
            tooltip=f"Flight: {flight_number}",
            popup=f"Flight: {flight_number}<br>Latitude: {lat}<br>Longitude: {lng}"
        ).add_to(m)

    return m._repr_html_()


@app.route('/analyse')
def analyse():
    # Votre code d'analyse ici
    # Remplacer le nombre d'échantillons par le nombre souhaité
    df_flight_sample = df_flight.sample(n=1000)
    df_airports_sample = df_airports.sample(n=1000)
    df_airlines_sample = df_airlines.sample(n=1000)
    df_flight_delay_sample = df_flight_delay.sample(n=1000)

    #Jointure pour obtenir le temps moyen de retard par compagnie aérienne
    # Jointure entre flight_delay et airlines sur airline_icao
    df_delay_airline = pd.merge(df_flight_delay_sample, df_airlines_sample, left_on="airline_icao", right_on="icao_code", how="inner")

    # Calcul du temps moyen de retard par compagnie aérienne
    avg_delay_duration_by_airline = df_delay_airline.groupby('airline_icao')['delayed'].mean()

    # Sélectionnez les 20 premières compagnies aériennes et leurs temps moyens de retard associés
    top_airlines = avg_delay_duration_by_airline.head(20)

    # Créez un graphique à barres pour afficher ces données
    # Sélectionnez les 20 premières compagnies aériennes et leurs temps moyens de retard associés
    top_airlines = avg_delay_duration_by_airline.head(20)

    # Créez un graphique à barres pour afficher ces données
    plt.figure(figsize=(12, 6))
    top_airlines.plot(kind='bar', color='skyblue')
    plt.xlabel('Compagnie Aérienne (ICAO Code)')
    plt.ylabel('Temps Moyen de Retard')
    plt.title('Temps Moyen de Retard par Compagnie Aérienne (Top 20)')
    plt.xticks(rotation=45)

    # Créez des objets BytesIO pour stocker les trois images en mémoire
    img_buffer_airlines = io.BytesIO()
    plt.savefig(img_buffer_airlines, format='png', dpi=300)
    img_buffer_airlines.seek(0)

    #Jointure pour obtenir le nombre total de vols par ville de départ
    # Jointure entre flight et airports sur departure_icao
    df_flight_airport = pd.merge(df_flight_sample, df_airports_sample, left_on="dep_icao", right_on="icao_code", how="inner")
    # Calcul du nombre total de vols par ville de départ
    total_flights_by_city = df_flight_airport['name'].value_counts()

    # Sélectionnez les 20 premières villes de départ et leurs nombres de vols associés
    top_cities = total_flights_by_city.head(20)

    # Créez un graphique à barres pour afficher ces données
    plt.figure(figsize=(12, 6))
    top_cities.plot(kind='bar', color='skyblue')
    plt.xlabel('Ville de Départ')
    plt.ylabel('Nombre de Vols')
    plt.title('Nombre Total de Vols par Ville de Départ (Top 20)')
    plt.xticks(rotation=45)

    # Créez des objets BytesIO pour stocker les trois images en mémoire
    img_buffer_cities = io.BytesIO()
    plt.savefig(img_buffer_cities, format='png', dpi=300)
    img_buffer_cities.seek(0)

    #Jointure pour obtenir la distribution des retards par aéroport de départ
    # Jointure entre flight_delay et airports sur departure_icao
    df_delay_airport = pd.merge(df_flight_delay_sample, df_airports_sample, left_on="dep_icao", right_on="icao_code", how="inner")

    # Distribution des retards par aéroport de départ
    delay_distribution_by_airport = df_delay_airport.groupby('name')['delayed'].value_counts()

    # Sélectionnez les 20 premiers aéroports de départ et leurs distributions de retards associées
    top_airports = delay_distribution_by_airport.unstack().sum(axis=1).sort_values(ascending=False).head(20)

    # Créez un graphique à barres pour afficher ces données
    plt.figure(figsize=(12, 6))
    top_airports.plot(kind='bar', color='coral')
    plt.xlabel('Aéroport de Départ')
    plt.ylabel('Nombre de Retards')
    plt.title('Distribution des Retards par Aéroport de Départ (Top 20)')
    plt.xticks(rotation=45)  # Faites pivoter les étiquettes de l'axe x pour qu'elles soient lisibles

    # Créez des objets BytesIO pour stocker les trois images en mémoire
    img_buffer_airports = io.BytesIO()
    plt.savefig(img_buffer_airports, format='png', dpi=300)
    img_buffer_airports.seek(0)

    # Concaténez les trois images en une seule
    final_image = io.BytesIO()
    plt.figure(figsize=(36, 6))
    plt.subplots_adjust(wspace=0.5)
    plt.subplot(1, 3, 1)
    plt.imshow(plt.imread(img_buffer_airlines))
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(plt.imread(img_buffer_cities))
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(plt.imread(img_buffer_airports))
    plt.axis('off')

    plt.savefig(final_image, format='png', dpi=300)
    final_image.seek(0)

    # Créez une réponse HTTP avec l'image finale
    return Response(final_image, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
