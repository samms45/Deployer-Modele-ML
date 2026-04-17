from src.api.db_config import engine
from src.api.db_models import Base

def init_db():
    # Crée les tables dans la base de données
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès.")

if __name__ == "__main__":
    init_db()