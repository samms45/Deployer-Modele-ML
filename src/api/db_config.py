import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

# On récupère l'URL
DATABASE_URL = os.getenv("DATABASE_URL")

# SI l'URL est vide OU si c'est du localhost (qui ne marchera pas sur HF)
if not DATABASE_URL or "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL:
    print("--- MODE DE SECOURS : SQLITE ACTIVE ---")
    DATABASE_URL = "sqlite:///./rh_prediction.db"
elif DATABASE_URL.startswith("postgres://"):
    # Correction pour SQLAlchemy 2.0
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()