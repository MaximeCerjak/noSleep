from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from .database import create_tables


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

# Création de l'objet db de SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Initialisation de l'instance de l'application Flask
    app = Flask(__name__)
    
    # Configuration de l'URI de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/xampp/htdocs/lab/PYTHON/PYSEARCH/veille.sqlite'
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///veille.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialisation de l'objet db avec l'application Flask
    db.init_app(app)
    
    # Création des tables de la base de données si elles n'existent pas déjà
    with app.app_context():
        print("Création des tables...")
        try :
            create_tables()
        except Exception as e:
            print(e)
        print("Tables créées.")

    # Importation du Blueprint après l'initialisation de db pour éviter les importations cycliques
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app


