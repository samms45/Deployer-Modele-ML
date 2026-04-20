import json
import requests
import os

def run_seeding(json_path="api_data.json", url="http://0.0.0.0:7860/predict"):
    if not os.path.exists(json_path):
        print(f"Fichier {json_path} introuvable.")
        return False

    with open(json_path, "r", encoding="utf-8") as f:
        employees = json.load(f)

    print(f"Injection de {len(employees)} employés en cours...")
    
    # On retourne True si au moins un truc a été tenté
    return len(employees) > 0

if __name__ == "__main__":
    # Ton code original reste ici pour l'usage manuel
    run_seeding()