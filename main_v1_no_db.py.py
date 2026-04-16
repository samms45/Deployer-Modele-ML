from fastapi import FastAPI
import joblib
from imblearn.pipeline import Pipeline as ImbPipeline
import pandas as pd
from pydantic import BaseModel
import os

# 1. Création de l'application FastAPI
app = FastAPI(title="Prédiction Attrition RH")

# 2. Définition du modèle de données (Le contrat Pydantic)
# On liste chaque colonne avec son type correspondant
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


# 3. Chargement du modèle au démarrage de l'API
# Assure-toi que le chemin vers ton fichier .joblib est correct
MODEL_PATH = os.path.join("models", "model_final_reg.joblib")
model = joblib.load(MODEL_PATH)

# 3. Chargement du modèle au démarrage de l'API
MODEL_PATH = os.path.join("models", "model_final_reg.joblib")
model = joblib.load(MODEL_PATH)

# --- PATCH DE COMPATIBILITÉ ---
# On va chercher le modèle à l'intérieur du pipeline pour corriger le bug
try:
    # Si c'est un pipeline imblearn/sklearn, le modèle est souvent à la dernière étape
    logistic_model = model.steps[-1][1]
    
    # On lui ajoute manuellement l'option qui lui manque
    if not hasattr(logistic_model, 'multi_class'):
        logistic_model.multi_class = 'ovr'
        print("Patch 'multi_class' appliqué avec succès !")
except Exception as e:
    print(f"Note: Impossible d'appliquer le patch, mais on continue... Erreur: {e}")
# ------------------------------

# 4. Route de bienvenue
@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de prédiction RH. Utilisez /predict pour tester. \n cimer les gros BouzBouz"}

# 5. Route de prédiction
@app.post("/predict")
def predict(data: EmployeeData):
    # Convertir les données reçues en dictionnaire puis en DataFrame Pandas
    df_input = pd.DataFrame([data.model_dump()])
    
    # Faire la prédiction avec ton Pipeline (Preprocessing + Modèle)
    prediction = model.predict(df_input)
    # Récupérer la probabilité (optionnel mais recommandé pour les RH)
    probability = model.predict_proba(df_input)
    
    return {
        "prediction": int(prediction[0]),
        "resultat": "Départ" if prediction[0] == 1 else "Reste",
        "probabilite_depart": round(float(probability[0][1]), 2)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)