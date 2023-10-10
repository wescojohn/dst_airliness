# Utilisez une image Python appropriée comme base
FROM python:3.8

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers d'application dans le conteneur
COPY . /app

# Installez les dépendances de l'application
RUN pip install -r requirements.txt

# Commande pour exécuter l'application Flask au démarrage du conteneur
CMD ["python", "app.py"]
