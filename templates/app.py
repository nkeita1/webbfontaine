from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///annuaires.db' #le fichier de la base de données
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # remove the warnings
db = SQLAlchemy(app)

class Entreprise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    telephone = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    categorie = db.Column(db.String(50), nullable=True)
    def __repr__(self):
        return f'<Entreprise{self.nom}>'

@app.route('/')
def index():
    searchquery = request.args.get('q')
    selected_categorie = request.args.get('categorie')
    query = Entreprise.query

    if searchquery:
        query = query.filter(
            (Entreprise.nom.ilike(f'%{searchquery}%')) |
            (Entreprise.description.ilike(f'%{searchquery}%')) |
            (Entreprise.adresse.ilike(f'%{searchquery}%'))
        )
    if selected_categorie and selected_categorie != 'all':
        query = query.filter(Entreprise.categorie == selected_categorie)
    entreprises = query.all()
    categories = [c[0] for c in db.session.query(Entreprise.categorie).distinct().all()]
    return render_template('index.html', entreprises=entreprises, search_query=searchquery, selected_categorie=selected_categorie, categories=categories)


@app.route('/entreprise/<int:entreprise_id>')
def detail_entreprise(entreprise_id):
    entreprise = Entreprise.query.get_or_404(entreprise_id)
    return render_template('detail_entreprise.html', entreprise=entreprise)

@app.route('/ajouter', methods=['GET'])
def afficher_form_ajouter():
    return render_template('ajouter_entreprise.html') 

@app.route('/ajouter', methods=['GET','POST'])
def ajouter_entreprise():
    if request.method == 'POST':
        nom = request.form['nom']
        adresse = request.form['adresse']
        email = request.form['email']
        telephone = request.form['telephone']
        description = request.form['description']
        categorie = request.form['categorie']

        nouvelle_entreprise = Entreprise(
            nom=nom,
            adresse=adresse,
            email=email,
            telephone=telephone,
            description=description,
            categorie=categorie
        )
        
        db.session.add(nouvelle_entreprise)
        db.session.commit()
        
        flash('Entreprise ajoutée avec succès!', 'success')
        return redirect(url_for('index'))
    
    return render_template('ajouter_entreprise.html')

@app.route('/modifier/<int:entrepriseid>', methods=['GET', 'POST'])
def modifier_entreprise(entrepriseid):
    entreprise = Entreprise.query.get_or_404(entrepriseid)
    if request.method == 'POST':
        # Mettez à jour les attributs de l'entreprise avec les données du formulaire
        entreprise.nom = request.form['nom']
        entreprise.adresse = request.form['adresse']
        entreprise.telephone = request.form.get('telephone')
        entreprise.email = request.form.get('email')
        entreprise.description = request.form.get('description')
        entreprise.categorie = request.form.get('categorie')
        db.session.commit() # Sauvegardez les changements
        flash('Entreprise modifiée avec succès !', 'info')
        return redirect(url_for('detail_entreprise', entrepriseid=entreprise.id))

    # Pour la méthode GET, pré-remplissez le formulaire avec
    # les données existantes de l'entreprise
    return render_template('modifier_entreprise.html', entreprise=entreprise)

@app.route('/supprimer/<int:entrepriseid>', methods=['POST'])
def supprimer_entreprise(entrepriseid):
    entreprise = Entreprise.query.get_or_404(entrepriseid)
    db.session.delete(entreprise) # Supprime l'entreprise
    db.session.commit() # Sauvegarde les changements
    flash('Entreprise supprimée avec succès !', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)