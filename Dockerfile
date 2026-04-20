# 1. Image de base Python
FROM python:3.11-slim

# 2. Dossier de travail dans le serveur Hugging Face
WORKDIR /app

# 3. Installation de Git (nécessaire pour certains packages)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 4. Copie des fichiers de configuration et installation des dépendances
# On utilise 'uv' comme dans ta version pour que ce soit rapide
COPY pyproject.toml .
RUN pip install uv && uv pip install --system .

# 5. Copie de TOUT ton code (ton dossier src, ton main.py, etc.)
COPY . .

# 6. RÉGLAGE CRUCIAL : On dit à Python de regarder dans /app pour trouver 'src'
# C'est ce qui règle l'erreur "ModuleNotFoundError: No module named src"
ENV PYTHONPATH=/app

# 7. Port utilisé par Hugging Face
EXPOSE 7860

# 8. LA COMMANDE FINALE (Le grand nettoyage)
# - Il crée les tables (init_db)
# - Il insère tes 10 lignes de test (seed_data)
# - Il lance ton API (uvicorn)
CMD python src/api/init_db.py && python src/api/seed_data.py && uvicorn main:app --host 0.0.0.0 --port 7860