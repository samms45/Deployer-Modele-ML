import json
import requests

# Charger les données du fichier
with open("api_data.json", "r", encoding="utf-8") as f:
    employees = json.load(f)

url = "http://127.0.0.1:8000/predict"

print(f"Injection de {len(employees)} employés en cours...")

for emp in employees:
    response = requests.post(url, json=emp)
    if response.status_code == 200:
        print(f" Succès pour le poste : {emp['poste']}")
    else:
        print(f"Erreur pour {emp['poste']} : {response.text}")

print("\n Terminé ! Voir ton history ou pgAdmin.")