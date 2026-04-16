import os
from fastapi.testclient import TestClient
from main import app  # On importe ton code FastAPI

client = TestClient(app)

# --- CONFIGURATION DE LA SÉCURITÉ ---
# On récupère la clé API définie dans le .env (ou le CI)
# Si elle n'existe pas, on met une valeur par défaut pour éviter que ça plante
API_KEY = os.getenv("API_KEY", "mon_badge_secret_987")
HEADERS = {"X-API-KEY": API_KEY} 

# --- 1. TEST DE SUCCÈS (Le "Happy Path") ---
def test_predict_success():
    """
    Vérifie que l'API répond 200 et donne une prédiction 
    quand les données sont parfaitement remplies.
    """
    test_data = {
        "age": 41,
        "genre": "F",
        "revenu_mensuel": 5993,
        "statut_marital": "Célibataire",
        "poste": "Cadre Commercial",
        "nombre_experiences_precedentes": 8,
        "annee_experience_totale": 8,
        "annees_dans_l_entreprise": 6,
        "annees_dans_le_poste_actuel": 4,
        "satisfaction_employee_environnement": 2,
        "note_evaluation_precedente": 3,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "heure_supplementaires": "Oui",
        "augmentation_precedente_salaire_pct": 0.11,
        "nombre_participation_pee": 0,
        "nb_formations_suivies": 0,
        "distance_domicile_travail": 1,
        "niveau_education": 2,
        "domaine_etude": "Infra & Cloud",
        "frequence_deplacement": "Occasionnel",
        "annees_depuis_la_derniere_promotion": 0,
        "annes_sous_responsable_actuel": 5,
        "ratio_salaire_poste": 0.865505,
        "ratio_stagnation": 0.655738,
        "poste_penibilite_voyage": "Cadre Commercial_Occasionnel",
        "attente_promotion_pure": 4,
        "ratio_fidelite_manager": 1.1
    }

    # AJOUT : On passe les HEADERS ici
    response = client.post("/predict", json=test_data, headers=HEADERS)

    assert response.status_code == 200
    
    data = response.json()
    assert "prediction" in data
    assert "resultat" in data
    assert "probabilite_depart" in data
    assert 0 <= data["probabilite_depart"] <= 1


# --- 2. TEST D'ERREUR (Le "Negative Test") ---
def test_predict_invalid_data():
    """
    Vérifie que l'API rejette les requêtes avec des données manquantes.
    """
    incomplete_data = {"age": 30}

    # AJOUT : On passe les HEADERS même pour une erreur attendue
    # Car sinon on recevra un 403 (Interdit) avant même que l'API ne vérifie les données (422)
    response = client.post("/predict", json=incomplete_data, headers=HEADERS)

    assert response.status_code == 422


# --- 3. TEST DE SEUIL (Edge Cases) ---
def test_predict_edge_case_minimums():
    """
    Test de Seuil : Valeurs minimales.
    """
    edge_data = {
        "age": 18,
        "genre": "M",
        "revenu_mensuel": 0,
        "statut_marital": "Célibataire",
        "poste": "Technicien",
        "nombre_experiences_precedentes": 0,
        "annee_experience_totale": 0,
        "annees_dans_l_entreprise": 0,
        "annees_dans_le_poste_actuel": 0,
        "satisfaction_employee_environnement": 1,
        "note_evaluation_precedente": 1,
        "satisfaction_employee_nature_travail": 1,
        "satisfaction_employee_equipe": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "heure_supplementaires": "Non",
        "augmentation_precedente_salaire_pct": 0.0,
        "nombre_participation_pee": 0,
        "nb_formations_suivies": 0,
        "distance_domicile_travail": 1,
        "niveau_education": 1,
        "domaine_etude": "Autre",
        "frequence_deplacement": "Non-voyageur",
        "annees_depuis_la_derniere_promotion": 0,
        "annes_sous_responsable_actuel": 0,
        "ratio_salaire_poste": 0.0,
        "ratio_stagnation": 0.0,
        "poste_penibilite_voyage": "Technicien_Non-voyageur",
        "attente_promotion_pure": 0,
        "ratio_fidelite_manager": 0.0
    }

    # AJOUT : On passe les HEADERS ici
    response = client.post("/predict", json=edge_data, headers=HEADERS)

    assert response.status_code == 200