FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Installation des dépendances applicatives et d'un serveur WSGI de production (gunicorn)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copie du code applicatif
COPY . .

# Port exposé par Cloud Run
EXPOSE 8080

# Démarrage de l'application Flask via gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 "run:app"
