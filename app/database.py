from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

# Création de l'Engine qui va interagir avec la base de données
engine = create_engine('sqlite:///veille.sqlite', echo=True)
metadata = MetaData()

projet_table = Table('projet', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('nom', String(50), unique=True, nullable=False),
                    Column('description', String),
)

keyword_table = Table('keyword', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('mot_cle', String(50), unique=True, nullable=False),
)

canal_table = Table('canal', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('nom', String(100), nullable=False),
                    Column('description', String),
                    Column('projet_id', None, ForeignKey('projet.id')),
                    Column('keyword_id', None, ForeignKey('keyword.id')),
)

article_table = Table('article', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('url', String),
                    Column('type_contenu', String(50)),
                    Column('sujet_principal', String(50)),
                    Column('categorie', String(500)),
                    Column('synthese', String),
                    Column('canal_id', None, ForeignKey('canal.id')),
)

# Ensuite, vous créez les tables
def create_tables():
    metadata.create_all(engine)
