
from fastapi.testclient import TestClient
from main import app  # On importe ton code FastAPI

client = TestClient(app) # On crée le client de test qui va simuler les requêtes HTTP


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

    # 2. On envoie la requête POST à l'API
    response = client.post("/predict", json=test_data)

    # 3. Les vérifications (Le robot vérifie le résultat)
    # On vérifie que le code de retour est 200 (Succès)
    assert response.status_code == 200
    
    # On vérifie que la réponse contient bien les clés que tu as définies dans main.py
    data = response.json()
    assert "prediction" in data
    assert "resultat" in data
    assert "probabilite_depart" in data
    
    # Optionnel : On peut même vérifier que la probabilité est cohérente (entre 0 et 1)
    assert 0 <= data["probabilite_depart"] <= 1


    # --- 2. TEST D'ERREUR (Le "Negative Test") ---
def test_predict_invalid_data():
    """
    Vérifie que l'API rejette les requêtes avec des données manquantes.
    Elle doit répondre 422 (Unprocessable Entity).
    """
    # On envoie seulement l'âge (il manque tous les autres champs !)
    incomplete_data = {"age": 30}

    # On envoie la requête
    response = client.post("/predict", json=incomplete_data)

    # Vérification : On attend une erreur 422 de la part de FastAPI/Pydantic
    assert response.status_code == 422
    print(f"\nSécurité : L'API a bien rejeté les données incomplètes (Code {response.status_code})")


def test_predict_edge_case_minimums():
    """
    Test de Seuil : On teste les valeurs minimales (18 ans, 0 expérience, 0 revenu).
    L'API doit répondre 200 et donner une prédiction cohérente.
    """
    # On prend les valeurs les plus basses possibles
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

    response = client.post("/predict", json=edge_data)

    # On vérifie que ça passe (200)
    assert response.status_code == 200
    
    data = response.json()
    print("\n--- Test de Seuil (Valeurs Min) ---")
    print(f"Prédiction    : {data['prediction']}")
    print(f"Résultat      : {data['resultat']}")
    print(f"Probabilité   : {data['probabilite_depart']}")