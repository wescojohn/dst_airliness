# Utilisez l'image Python 3.8 comme base
FROM python:3.8

# Copiez les scripts Python dans l'image
COPY insert_data.py /app/insert_data.py
COPY insert_delay_data.py /app/insert_delay_data.py
COPY insert_airlines_data.py /app/insert_airlines_data.py
COPY insert_airports_data.py /app/insert_airports_data.py

# Installez les dépendances
RUN pip install requests pymongo mysql-connector-python

# Commande pour exécuter le script principal au démarrage du conteneur
CMD ["python", "/app/insert_data.py"]
