import os
import joblib
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dotenv import load_dotenv

# --- CONFIGURATION DES CHEMINS & CHARGEMENT ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "src", "api", "model_final_reg.joblib")

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    raise FileNotFoundError(f"Modèle introuvable à : {MODEL_PATH}")

# --- LES IMPORTS DE TON CODE ---
from src.api.db_config import engine, get_db 
from src.api.db_models import Base, PredictionLog 
from src.api.init_db import init_db

# --- SYNCHRONISATION DE LA BASE DE DONNÉES ---
# Ce bloc force la création de la colonne 'timestamp' si elle manque
try:
    print("--- SYNCHRONISATION DE LA BASE DE DONNÉES ---")
    # Si l'erreur de colonne persiste, remplace create_all par :
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Base de données synchronisée avec succès.")
except Exception as e:
    print(f"Attention - Erreur lors de la synchro DB : {e}")

# --- CONFIGURATION SÉCURITÉ ---
load_dotenv()

# Debug pour Hugging Face
print("--- DEBUG CONNEXION ---")
db_url_check = os.getenv("DATABASE_URL")
if db_url_check:
    print(f"DATABASE_URL détectée (début) : {db_url_check[:15]}...")
else:
    print("ERREUR : DATABASE_URL est introuvable !")

API_KEY_VAL = os.getenv("API_KEY")
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(header_api_key: str = Security(api_key_header)):
    if header_api_key == API_KEY_VAL:
        return header_api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Accès refusé : Clé API invalide ou absente"
    )

# --- INITIALISATION API ---
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

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API RH. cimer les gros BouzBouz"}

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
        print(f"Erreur SQL insertion : {e}")
        db.rollback()

    return {
        "prediction": prediction,
        "resultat": result_text,
        "probabilite_depart": round(probability, 2)
    }

@app.get("/history", dependencies=[Depends(get_api_key)])
def get_history(db: Session = Depends(get_db)):
    try:
        # On récupère les logs. Le tri se fera via Python si la colonne timestamp est capricieuse au début
        history = db.query(PredictionLog).all()
        return history
    except Exception as e:
        return {"error": f"Impossible de récupérer l'historique : {e}"}

# --- LANCEMENT ---
if __name__ == "__main__":
    import uvicorn
    # Configuration impérative pour Hugging Face
    uvicorn.run(app, host="0.0.0.0", port=7860)