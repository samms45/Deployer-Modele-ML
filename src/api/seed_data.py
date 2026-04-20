import json
import requests
import os

# Ajoute bien les arguments json_path et url ici !
def run_seeding(json_path="api_data.json", url="http://127.0.0.1:7860/predict"):
    if not os.path.exists(json_path):
        print(f"Fichier {json_path} introuvable.")
        return False

    # On récupère la clé API pour passer la sécurité du main.py
    api_key = os.getenv("API_KEY")
    headers = {"access_token": api_key} if api_key else {}

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            employees = json.load(f)
        
        if isinstance(employees, dict):
            employees = [employees]

        for emp in employees:
            # On ignore les erreurs de connexion pendant les tests
            try:
                requests.post(url, json=emp, headers=headers, timeout=2)
            except:
                pass 
                
        return True
    except Exception as e:
        print(f"Erreur : {e}")
        return False

if __name__ == "__main__":
    run_seeding()