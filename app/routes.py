from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from sqlalchemy.sql import select, insert, update, delete
from .database import engine, projet_table, canal_table, article_table, keyword_table, engine
from contextlib import contextmanager

main = Blueprint('main', __name__)




@contextmanager
def get_connection():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/projets', methods=['GET'])
def list_projets():
    with engine.connect() as conn:
        s = select(projet_table)
        result = conn.execute(s)
        projets = [dict(row) for row in result.mappings()]
    return jsonify(projets), 200



@main.route('/projet/new', methods=['GET'])
def new_projet():
    return render_template('projectForm.html')

@main.route('/projet', methods=['POST'])
def create_projet():
    data = request.form
    with engine.connect() as conn:
        try:
            ins = projet_table.insert().values(nom=data['nom'], description=data.get('description', ''))
            conn.execute(ins)
        except Exception as e:
            # Log l'erreur pour le débogage
            print("Erreur lors de l'insertion du projet :", str(e))
            return jsonify({'error': 'Impossible de créer le projet.'}), 400
        else:
            # Si aucune exception n'est levée, commit la transaction
            conn.commit()
            return redirect(url_for('main.index')), 302

@main.route('/projet/<int:projet_id>', methods=['GET'])
def projet_detail(projet_id):
    with engine.connect() as conn:
        s = select(projet_table).where(projet_table.c.id == projet_id)
        projet = conn.execute(s).fetchone()
        if projet is None:
            return "Projet non trouvé", 404

        projet_dict = dict(projet._mapping)

        s = select(canal_table).where(canal_table.c.projet_id == projet_id)
        canaux = [dict(row._mapping) for row in conn.execute(s)]

        articles = []
        for canal in canaux:
            s = select(article_table).where(article_table.c.canal_id == canal['id'])
            articles.extend([dict(row._mapping) for row in conn.execute(s)])

        keywords = {}
        for canal in canaux:
            s = select(keyword_table).where(keyword_table.c.id == canal['keyword_id'])
            keyword = conn.execute(s).fetchone()
            print(type(keyword))  # Pour vérifier le type de l'objet
            print(keyword) 
            if keyword:
                # Accès correct aux colonnes par leur nom
                keywords[canal['keyword_id']] = keyword._mapping['mot_cle']

    return render_template('projet_detail.html', projet=projet_dict, canaux=canaux, articles=articles, keywords=keywords)


@main.route('/projet/<int:projet_id>', methods=['DELETE'])
def delete_projet(projet_id):
    conn = engine.connect()
    d = delete(projet_table).where(projet_table.c.id == projet_id)
    result = conn.execute(d)
    conn.close()
    return jsonify({'status': 'success', 'message': 'Projet supprimé'}), 200

@main.route('/projet/<int:projet_id>/canal/new', methods=['GET'])
def new_canal(projet_id):
    return render_template('canalForm.html', projet_table=projet_table, projet_id=projet_id)

@main.route('/projet/<int:projet_id>/canal/new', methods=['POST'])
def create_canal(projet_id):
    nom_canal = request.form.get('nom_canal')
    mot_cle_text = request.form.get('mot_cle')
    
    with get_connection() as conn:
        with conn.begin():
            keyword_select = select(keyword_table).where(keyword_table.c.mot_cle == mot_cle_text)
            keyword_result = conn.execute(keyword_select).fetchone()
            
            if keyword_result:
                keyword_id = keyword_result.id
            else:
                keyword_insert = keyword_table.insert().values(mot_cle=mot_cle_text)
                keyword_id = conn.execute(keyword_insert).inserted_primary_key[0]
            
            canal_insert = canal_table.insert().values(
                nom=nom_canal,
                description='',  # Ajoutez une description si nécessaire
                projet_id=projet_id,
                keyword_id=keyword_id
            )
            conn.execute(canal_insert)
    
    return redirect(url_for('main.projet_detail', projet_id=projet_id))

@main.route('/canal/<int:canal_id>', methods=['DELETE'])
def delete_canal(canal_id):
    conn = engine.connect()
    d = delete(canal_table).where(canal_table.c.id == canal_id)
    result = conn.execute(d)
    conn.close()
    return jsonify({'status': 'success', 'message': 'Canal supprimé'}), 200

@main.route('/canal/<int:canal_id>/article', methods=['POST'])
def create_article(canal_id):
    data = request.form
    conn = engine.connect()
    ins = article_table.insert().values(url=data['url'], type_contenu=data['type_contenu'], sujet_principal=data['sujet_principal'], categorie=data['categorie'], synthese=data['synthese'], canal_id=canal_id)
    result = conn.execute(ins)
    conn.close()
    return redirect(url_for('main.get_canal', canal_id=canal_id)), 302

@main.route('/canal/<int:canal_id>', methods=['GET'])
def get_canal(canal_id):
    conn = engine.connect()
    s = select([canal_table]).where(canal_table.c.id == canal_id)
    result = conn.execute(s).fetchone()
    if result is None:
        return jsonify({'error': 'Canal non trouvé'}), 404
    return jsonify(dict(result)), 200

@main.route('/canal/<int:canal_id>/articles', methods=['GET'])
def list_articles(canal_id):
    conn = engine.connect()
    s = select([article_table]).where(article_table.c.canal_id == canal_id)
    result = conn.execute(s)
    articles = [dict(row) for row in result]
    result.close()
    return jsonify(articles), 200

@main.route('/article/<int:article_id>', methods=['GET'])
def get_article(article_id):
    conn = engine.connect()
    s = select([article_table]).where(article_table.c.id == article_id)
    result = conn.execute(s).fetchone()
    if result is None:
        return jsonify({'error': 'Article non trouvé'}), 404
    return jsonify(dict(result)), 200

@main.route('/article/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    conn = engine.connect()
    d = delete(article_table).where(article_table.c.id == article_id)
    result = conn.execute(d)
    conn.close()
    return jsonify({'status': 'success', 'message': 'Article supprimé'}), 200

@main.route('/article/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    data = request.form
    conn = engine.connect()
    u = update(article_table).where(article_table.c.id == article_id).values(url=data['url'], type_contenu=data['type_contenu'], sujet_principal=data['sujet_principal'], categorie=data['categorie'], synthese=data['synthese'])
    result = conn.execute(u)
    conn.close()
    return redirect(url_for('main.get_article', article_id=article_id)), 302

