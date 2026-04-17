import pytest
from fastapi.testclient import TestClient
import sys
import os
from dotenv import load_dotenv

# --- ÉTAPE 1 : RÉGLER LE GPS DE PYTHON ---
# On dit à Python de regarder dans le dossier parent AVANT de faire les imports
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# --- ÉTAPE 2 : LES IMPORTS ---
# Maintenant que le chemin est bon, on peut importer main
from main import app
from src.api.db_config import engine

# --- ÉTAPE 3 : CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("API_KEY")
HEADERS = {"access_token": API_KEY}



client = TestClient(app)

# --- TESTS DE CONNEXION ET BASE ---

def test_read_root():
    """Vérifie que l'API répond sur la racine (Pas besoin de clé ici)"""
    response = client.get("/")
    assert response.status_code == 200

def test_db_connection():
    """Vérifie que la connexion à PostgreSQL est possible"""
    try:
        connection = engine.connect()
        assert connection is not None
        connection.close()
    except Exception as e:
        pytest.fail(f"Erreur de connexion DB : {e}")

def test_get_history():
    """Vérifie que la récupération de l'historique fonctionne"""
    # AJOUT : on passe le dictionnaire HEADERS
    response = client.get("/history", headers=HEADERS) 
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# --- TESTS FONCTIONNELS (POUR LE COVERAGE) ---

def test_predict_success():
    """Vérifie qu'une prédiction complète fonctionne et s'enregistre"""
    payload = {
        "age": 35, "genre": "F", "revenu_mensuel": 4200, 
        "statut_marital": "Marié(e)", "poste": "Consultant",
        "nombre_experiences_precedentes": 2, "annee_experience_totale": 12,
        "annees_dans_l_entreprise": 7, "annees_dans_le_poste_actuel": 4,
        "satisfaction_employee_environnement": 4, "note_evaluation_precedente": 3,
        "satisfaction_employee_nature_travail": 4, "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3, "heure_supplementaires": "Non",
        "augmentation_precedente_salaire_pct": 0.15, "nombre_participation_pee": 1,
        "nb_formations_suivies": 3, "distance_domicile_travail": 12,
        "niveau_education": 4, "domaine_etude": "Infra & Cloud",
        "frequence_deplacement": "Rare", "annees_depuis_la_derniere_promotion": 2,
        "annes_sous_responsable_actuel": 3, "ratio_salaire_poste": 1.0,
        "ratio_stagnation": 0.3, "poste_penibilite_voyage": "Consultant_Rare",
        "attente_promotion_pure": 1, "ratio_fidelite_manager": 0.9
    }
    # AJOUT : on passe le dictionnaire HEADERS
    response = client.post("/predict", json=payload, headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert "resultat" in json_data
    assert "probabilite_depart" in json_data
    

def test_predict_invalid_data():
    """Vérifie que l'API rejette les données incomplètes (Erreur 422)"""
    # AJOUT : même pour une erreur de donnée, il faut d'abord montrer le badge !
    response = client.post("/predict", json={"age": "invalide"}, headers=HEADERS)
    assert response.status_code == 422