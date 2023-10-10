import requests
import mysql.connector

api_key = "b26fc856-37fa-414d-a85f-3c51d6c007d4"
url = f"https://airlabs.co/api/v9/airlines?api_key={api_key}"

# Effectuer la demande HTTP pour récupérer les données des compagnies aériennes
response = requests.get(url)

if response.status_code == 200:
    airline_data = response.json()['response']
else:
    print("Erreur lors de la requête HTTP pour les compagnies aériennes")

# Établir la connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root",
    database="dst_airliness"
)

cursor = conn.cursor()

# Créer la table "airlines" si elle n'existe pas déjà
# Vérifier si la table 'airlines' existe déjà
cursor.execute("SHOW TABLES LIKE 'airlines'")
table_exists = cursor.fetchone()

if not table_exists:
    create_table_query = """
    CREATE TABLE IF NOT EXISTS airlines (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        iata_code VARCHAR(5),
        icao_code VARCHAR(3)
    )
    """

    cursor.execute(create_table_query)
    conn.commit()

# Insérer les données des compagnies aériennes dans la table "airlines"
insert_query = """
INSERT INTO airlines (name, iata_code, icao_code)
VALUES (%s, %s, %s)
"""

for airline in airline_data:
    airline_info = (
        airline.get('name', ''),
        airline.get('iata_code', ''),
        airline.get('icao_code', '')
    )
    cursor.execute(insert_query, airline_info)

conn.commit()

# Fermer la connexion à la base de données
conn.close()
