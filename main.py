import os
import joblib
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, Security, status # Ajout Security et status
from fastapi.security.api_key import APIKeyHeader # Pour le système de badge
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dotenv import load_dotenv # Pour lire le .env

# --- CONFIGURATION SÉCURITÉ ---
load_dotenv() # On charge le .env (DATABASE_URL, API_KEY, etc.)
API_KEY_VAL = os.getenv("API_KEY") # On récupère ton badge secret
API_KEY_NAME = "access_token"      # Le nom que l'utilisateur devra taper

# Le "Vigile" : il regarde si la clé dans le Header est la même que dans le .env
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(header_api_key: str = Security(api_key_header)):
    if header_api_key == API_KEY_VAL:
        return header_api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Accès refusé : Clé API invalide ou absente"
    )
# ------------------------------

from db_config import get_db
from db_models import PredictionLog

app = FastAPI(title="Prédiction Attrition RH Sécurisée")

class EmployeeData(BaseModel):
    age: int
    genre: str  
    revenu_mensuel: int
    statut_marital: str  
    poste: str  
    nombre_experiences_precedentes: int
    annee_experience_totale: int
    annees_dans_l_entreprise: int
    annees_dans_le_poste_actuel: int
    satisfaction_employee_environnement: int
    note_evaluation_precedente: int
    satisfaction_employee_nature_travail: int
    satisfaction_employee_equipe: int
    satisfaction_employee_equilibre_pro_perso: int
    heure_supplementaires: str  
    augmentation_precedente_salaire_pct: float
    nombre_participation_pee: int
    nb_formations_suivies: int
    distance_domicile_travail: int
    niveau_education: int
    domaine_etude: str  
    frequence_deplacement: str 
    annees_depuis_la_derniere_promotion: int
    annes_sous_responsable_actuel: int
    ratio_salaire_poste: float
    ratio_stagnation: float
    poste_penibilite_voyage: str  
    attente_promotion_pure: int
    ratio_fidelite_manager: float

# Chargement du modèle
MODEL_PATH = os.path.join("models", "model_final_reg.joblib")
model = joblib.load(MODEL_PATH)

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API RH. cimer les gros BouzBouz"}

# ROUTE PRÉDICT : Ajout de la dépendance de sécurité
@app.post("/predict", dependencies=[Depends(get_api_key)])
def predict(data: EmployeeData, db: Session = Depends(get_db)):
    df_input = pd.DataFrame([data.model_dump()])
    
    prediction = int(model.predict(df_input)[0])
    probability = float(model.predict_proba(df_input)[0][1])
    result_text = "Départ" if prediction == 1 else "Reste"

    try:
        new_log = PredictionLog(
            age=data.age,
            poste=data.poste,
            revenu_mensuel=data.revenu_mensuel,
            annees_dans_l_entreprise=data.annees_dans_l_entreprise,
            satisfaction_travail=data.satisfaction_employee_nature_travail,
            prediction=prediction,
            probabilite=round(probability, 2),
            resultat=result_text
        )
        db.add(new_log)
        db.commit()
    except Exception as e:
        print(f"Erreur SQL : {e}")

    return {
        "prediction": prediction,
        "resultat": result_text,
        "probabilite_depart": round(probability, 2)
    }

# ROUTE HISTORY : Ajout de la dépendance de sécurité
@app.get("/history", dependencies=[Depends(get_api_key)])
def get_history(db: Session = Depends(get_db)):
    try:
        history = db.query(PredictionLog).order_by(PredictionLog.timestamp.desc()).limit(10).all()
        return history
    except Exception as e:
        return {"error": f"Impossible de récupérer l'historique : {e}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)