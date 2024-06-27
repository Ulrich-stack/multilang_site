# Utilisez une image officielle de Python comme image de base
FROM python:3.12

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier tout le code source dans le conteneur
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Appliquer les migrations de la base de données
RUN python manage.py migrate

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 8000

# Démarrer l'application
CMD ["gunicorn", "multilang_site.wsgi:application", "--bind", "0.0.0.0:8000"]
