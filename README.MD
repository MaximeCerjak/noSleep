# PYSEARCH

## Description
Ce projet est un robot de veille qui permet de rechercher des informations sur internet et de les stocker dans une base de données locale.

## Installation
Pour installer le projet, il suffit de cloner le dépôt et d'installer les dépendances avec la commande suivante:
```bash
pip install -r requirements.txt
```

## Utilisation
Pour utiliser le projet, il suffit de lancer le script `main.py` avec la commande suivante:
```bash
python main.py
```

## Composition

### Scripts

- `main.py`: Script principal qui lance le robot de veille.
- `collecte.py`: Script qui permet de rechercher des informations sur internet par mot clé.
- `database.py`: Script qui permet de stocker les informations collectées dans une base de données locale.
- `scraping.py`: Script qui permet de récupérer les informations d'une page web.
- `analyse.py`: Script qui permet d'analyser les informations collectées.
- `document.py`: Script qui permet de stocker les informations collectées dans un fichier.