import openai

openai.api_key = ''

def content_analyz(data):
    text = data['contenu']
    url = data['url']
    # Initialisation de la session de chat avec GPT-3.5-turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Vous êtes un modèle très compétent en analyse de texte. TA REPONSE NE DOIT CONTENIR QU'UN MOT OU UN GROUPE DE MOTS REPRESENTANT UN TYPE DE CONTENU WEB."},
            {"role": "user", "content": f"Quel est le type de ce contenu? {text[:1500]}"},
        ]
    )
    type_contenu = response.choices[0].message.content
    # type_contenu = response.choices[0].message['content']


    # Pour le sujet principal
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Vous êtes un modèle très compétent en analyse de texte. TA REPONSE NE DOIT CONTENIR QU'UN MOT OU UN GROUPE DE MOTS REPRESENTANT LE SUJET PRINCIPAL ABORDé."},
            {"role": "user", "content": f"Quel est le sujet principal de ce contenu? {text[:1500]}"},
        ]
    )
    sujet_principal = response.choices[0].message.content
    # sujet_principal = response.choices[0].message['content']


    # Pour la catégorie
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Vous êtes un modèle très compétent en analyse de texte. TA REPONSE NE DOIT CONTENIR QU'UN MOT, GROUPE DE MOTS OU LISTE DE MOTS (en tableau [cat1, cat2, cat3, ...]) REPRESENTANT UNE CATEGORIE DE CONTENU."},
            {"role": "user", "content": f"Dans quelle catégorie ce contenu peut-il être classé? Tech, social, politique, science... {text[:1500]}"},
        ]
    )
    categorie = response.choices[0].message.content
    # categorie = response.choices[0].message['content']


    # Pour la synthèse du contenu
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Vous êtes un modèle très compétent en analyse de texte."},
            {"role": "user", "content": f"Peux-tu faire une synthèse de ce contenu? {text[:1500]}"},
        ]
    )
    synthese = response.choices[0].message.content
    # synthese = response.choices[0].message['content']

    return {
        "url": url,
        "type": type_contenu,
        "sujet": sujet_principal,
        "categorie": categorie,
        "synthese": synthese
    }

