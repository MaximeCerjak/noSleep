import requests

API_KEY = ""
CSE_ID = ""

def result_gcsearch(mot_cle, api_key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': mot_cle,
        'key': api_key,
        'cx': cse_id,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Ceci lèvera une exception si la requête a échoué
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête Google Custom Search: {e}")
        return None
    
# Test de la fonction avec un mot-clé exemple
resultats = result_gcsearch("Python programmation", API_KEY, CSE_ID)

if resultats:
    print("Résultats trouvés :")
    for item in resultats.get("items", []):
        print(f"Titre : {item['title']}, Lien : {item['link']}")
else:
    print("Aucun résultat trouvé ou erreur lors de la requête.")

