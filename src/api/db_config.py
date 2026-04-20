import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# On récupère l'URL du secret Hugging Face
DATABASE_URL = os.getenv("DATABASE_URL")

# Si DATABASE_URL contient "localhost" ou est vide, on force SQLite
# car Hugging Face ne peut pas se connecter à ton 'localhost'
if not DATABASE_URL or "localhost" in DATABASE_URL:
    # On crée un fichier local nommé rh_prediction.db
    SQLALCHEMY_DATABASE_URL = "sqlite:///./rh_prediction.db"
    # L'argument check_same_thread est spécifique à SQLite
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Si c'est une vraie URL (Postgres distante), on l'utilise
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()