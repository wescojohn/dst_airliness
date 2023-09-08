import pymongo
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Connexion à MongoDB
client = pymongo.MongoClient('localhost', 27017)
db = client['dst_airliness']
collection = db['flight_delay']

# Extraction des données de la collection MongoDB
cursor = collection.find({}, {"_id": 0})

# Création d'un DataFrame pandas à partir des données MongoDB
df = pd.DataFrame(list(cursor))

# Traitement des données
# Suppression des colonnes inutiles
df.drop(['cs_airline_iata', 'cs_flight_number', 'cs_flight_iata'], axis=1, inplace=True)

# Conversion des colonnes de date/heure en format datetime
date_columns = ['dep_time', 'dep_estimated', 'dep_actual', 'arr_time', 'arr_estimated']
for col in date_columns:
    df[col] = pd.to_datetime(df[col])

# Calcul de la durée du vol en minutes
df['flight_duration_minutes'] = (df['arr_time'] - df['dep_time']).dt.total_seconds() / 60

# Encodage des colonnes catégorielles
df_encoded = pd.get_dummies(df, columns=['airline_iata', 'dep_iata', 'arr_iata'], drop_first=True)

# Analyse des retards
average_delay = df_encoded['delayed'].mean()
max_delay = df_encoded['delayed'].max()
min_delay = df_encoded['delayed'].min()

# Affichage des statistiques
print(f"Statistiques des retards :")
print(f"Retard moyen : {average_delay} minutes")
print(f"Retard maximum : {max_delay} minutes")
print(f"Retard minimum : {min_delay} minutes")

# Analyse par compagnie aérienne
average_delay_by_airline = df.groupby('airline_iata')['delayed'].mean()
print("\nRetard moyen par compagnie aérienne :")
print(average_delay_by_airline)

# Analyse par aéroport d'arrivée
average_delay_by_arrival_airport = df.groupby('arr_iata')['delayed'].mean()
print("\nRetard moyen par aéroport d'arrivée :")
print(average_delay_by_arrival_airport)

# Fermeture de la connexion à MongoDB
client.close()
