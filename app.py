
from flask import Flask, render_template 
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
    entreprises = Entreprise.query.all()
    print(entreprises)  # Affiche les entreprises dans la console pour le débogage
    return render_template('index.html', entreprises=entreprises)
if __name__ == '__main__':
    app.run(debug=True)  # debug=True permet de voir les erreurs et recharger auto


@app.route('/entreprise/<int:entrepriseid>')
def detail_entreprise(entrepriseid):
    entreprise = Entreprise.query.get_or_404(entrepriseid)
    return render_template('detail_entreprise.html', 
entreprise=entreprise)