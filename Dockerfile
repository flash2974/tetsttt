FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier requirements et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du projet dans /app
COPY . /app

# Commande par défaut
CMD ["python", "-u", "main.py"]
