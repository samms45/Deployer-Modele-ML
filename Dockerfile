# 1. Image de base (Python)
FROM python:3.11-slim

# 2. Dossier de travail dans le container
WORKDIR /app

# 3. Installation des outils nécessaires
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 4. Copie des fichiers de configuration et installation
COPY pyproject.toml .
RUN pip install uv && uv pip install --system .

# 5. Copie de TOUT ton code (src, main.py, etc.)
COPY . .

# 6. Exposition du port Hugging Face
EXPOSE 7860

# 7. Lancement de l'API
# Note: si ton application est dans main.py, on lance main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]