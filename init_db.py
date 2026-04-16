# Le script pour générer les tables.

from db_config import engine, Base  # On utilise le nouveau nom ici
import db_models                    # Et ici aussi

print("--- Tentative de connexion à PostgreSQL ---")
try:
    Base.metadata.create_all(bind=engine)
    print("--- SUCCÈS : La table 'predictions' a été créée ! ---")
except Exception as e:
    print(f"--- ERREUR : Connexion impossible --- \n{e}")