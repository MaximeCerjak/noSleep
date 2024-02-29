import requests
from analyse import content_analyz
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

def robot_txt_pass(url, user_agent='*'):

    # Vérifie si l'accès à l'URL est autorisé pour le user-agent donné selon le fichier robots.txt du site.
    
    # :param url: URL de la page à vérifier.
    # :param user_agent: User-agent utilisé pour le scraping.
    # :return: True si l'accès est autorisé, False sinon.

    parsed_url = urlparse(url)  # Analyse l'URL ici
    parser = RobotFileParser()
    parser.set_url(f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt")
    parser.read()
    return parser.can_fetch(user_agent, parsed_url.geturl())

def scrap_content(url):

    # Extrait le contenu textuel d'une page web.

    # :param url: URL de la page à scraper.
    # :return: Contenu textuel de la page, ou None si l'accès est interdit.

    # Vérification robots.txt
    if not robot_txt_pass(url):
        print("Accès non autorisé par le fichier robots.txt")
        return None

    # Extraction du contenu de la page
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphes = soup.find_all(['p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    contenu = ' '.join(paragraphe.get_text() for paragraphe in paragraphes)
    resp = {"contenu": contenu, "url": url}
    return resp

# Test de la fonction avec une URL exemple et l'analyse du contenu
url_test = "https://www.mongodb.com/cloud/atlas/lp/try3?utm_campaign=ea-ww_acq_atlas_prospecting&utm_source=readthedocs&utm_medium=display&utm_term=atlas&utm_content=code2&ea-publisher=dailydev"
contenu = scrap_content(url_test)
if contenu:
    print("Contenu extrait avec succès. Analyse en cours...")
    print(content_analyz(contenu))
else:
    print("Échec de l'extraction du contenu.")
