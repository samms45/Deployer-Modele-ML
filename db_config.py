import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. On charge les variables d'environnement depuis le fichier .env
load_dotenv()

# 2. On récupère l'URL de la base. 
# Si elle n'existe pas dans le .env, on met une erreur explicite.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("L'URL de la base de données n'est pas configurée dans le fichier .env")

# 3. Configuration SQLAlchemy standard
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 4. Fonction pour FastAPI (inchangée, elle est déjà très bien !)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()