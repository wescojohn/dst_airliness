from flask import Flask, render_template
import folium
from folium import DivIcon
from pymongo import MongoClient

app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient(host='localhost', port=27017)
db = client["dst_airliness"]
collection = db["flight_collection"]

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

if __name__ == '__main__':
    app.run(debug=True)
