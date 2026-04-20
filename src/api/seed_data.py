import pandas as pd
import requests
import os

def run_seeding():
    # 1. Lire le JSON que tu as créé avec Pandas (orient='records')
    json_path = "api_data.json"
    url = "http://127.0.0.1:7860/predict" # URL locale au conteneur
    
    # Récupérer la clé API depuis l'environnement
    api_key = os.getenv("API_KEY") 
    headers = {"access_token": api_key}

    if os.path.exists(json_path):
        df = pd.read_json(json_path)
        data_list = df.to_dict(orient='records')
        
        for record in data_list:
            # Envoi avec la clé de sécurité
            requests.post(url, json=record, headers=headers)
        print("Seeding terminé !")