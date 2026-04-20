# Définit la structure de tes tables.

from sqlalchemy import Column, Integer, String, Float, DateTime
from src.api.db_config import Base
import datetime
from sqlalchemy import func

class PredictionLog(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, server_default=func.now())
    
    # Inputs clés pour le monitoring
    age = Column(Integer)
    revenu_mensuel = Column(Integer)
    poste = Column(String)
    annees_dans_l_entreprise = Column(Integer)
    satisfaction_travail = Column(Integer)
    
    # Outputs du modèle
    prediction = Column(Integer)  # 0 ou 1
    probabilite = Column(Float)   # ex: 0.85
    resultat = Column(String)     # "Départ" ou "Reste"