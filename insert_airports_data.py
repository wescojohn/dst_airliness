import requests
import mysql.connector

api_key = "b26fc856-37fa-414d-a85f-3c51d6c007d4"
url = f"https://airlabs.co/api/v9/airports?api_key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    airports_data = response.json()['response']
    
    # Établir la connexion à la base de données
    conn = mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="dst_airliness"
    )

    cursor = conn.cursor()

    # Vérifier si la table 'airports' existe déjà
    cursor.execute("SHOW TABLES LIKE 'airports'")
    table_exists = cursor.fetchone()

    if not table_exists:
        create_table_query = """
        CREATE TABLE airports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            iata_code VARCHAR(3),
            icao_code VARCHAR(4),
            city_code VARCHAR(3),
            country_code VARCHAR(2),
            lat FLOAT,
            lng FLOAT
        )
        """
        cursor.execute(create_table_query)
        conn.commit()

    insert_query = """
    INSERT INTO airports (name, iata_code, icao_code, city_code, country_code, lat, lng)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for airport_data in airports_data:
        airport = (
            airport_data['name'],
            airport_data.get('iata_code', None),
            airport_data.get('icao_code', None),
            airport_data.get('city_code', None),
            airport_data.get('country_code', None),
            airport_data.get('lat', None),
            airport_data.get('lng', None)
        )

        cursor.execute(insert_query, airport)
    
    conn.commit()

    # Fermer la connexion
    cursor.close()
    conn.close()
else:
    print("Erreur lors de la requête HTTP")
