import json
import requests
import os

def run_seeding(json_path="api_data.json", url="https://samss1010-api-prediction-rh.hf.space/predict"):
    if not os.path.exists(json_path):
        print(f"❌ Fichier {json_path} introuvable.")
        return False

    api_key = os.getenv("API_KEY", "mon_badge_secret_987") # Remplace par ta vraie clé
    headers = {"access_token": api_key}

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            employees = json.load(f)
        
        if isinstance(employees, dict):
            employees = [employees]

        print(f"🚀 Début de l'injection de {len(employees)} individus...")
        
        success_count = 0
        for i, emp in enumerate(employees):
            try:
                # On augmente un peu le timeout pour être sûr
                res = requests.post(url, json=emp, headers=headers, timeout=10)
                
                if res.status_code == 200:
                    success_count += 1
                else:
                    print(f"⚠️ Ligne {i+1} : Erreur {res.status_code}")
                    print(f"   Détail : {res.text}") # Affiche pourquoi l'API refuse
            except Exception as e:
                print(f"❌ Ligne {i+1} : Erreur de connexion : {e}")
                
        print(f"✅ Terminé ! {success_count}/{len(employees)} ajoutés avec succès.")
        return True
    except Exception as e:
        print(f"🔥 Erreur critique : {e}")
        return False

if __name__ == "__main__":
    run_seeding()