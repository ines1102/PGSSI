# Importation des modules nécessaires
from flask import Flask, render_template, request, redirect, url_for, session, make_response 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required
from app import app, db
import hashlib

# Clé secrète pour la gestion des sessions
app.secret_key = "123"

# Définition du modèle Pro dans la base de données
class Pro(UserMixin, db.Model):
    _bind_key_ = 'pro'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    mdp = db.Column(db.String(120), nullable=False)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

# Initialisation de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'connexion'

@login_manager.user_loader
def load_user(user_id):
    return Pro.query.get(int(user_id))

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html', title='MDM')

# Route pour l'inscription d'un médecin
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    error_message = None
    success_message=None
    success = False

    if request.method == 'POST':
        email = request.form['email']
        mdp = request.form['mdp']
        mdp_hache = hashlib.sha1(mdp.encode()).hexdigest()

        pro_existant = Pro.query.filter_by(email=email).first()
        if pro_existant:
            error_message = "Un profession avec ce email existe déjà. Veuillez vous connecter."
        else:
            nouveau_pro = Pro(email=email, mdp=mdp_hache)
            db.session.add(nouveau_pro)
            db.session.commit()
            success_message = "Le Pro a été inscrit avec succès"
            success = True

    return render_template('inscription.html', error_message=error_message, success=success, success_message=success_message)

# Route pour la connexion d'un professionnel
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    error_message = None

    if request.method == 'POST':
        email = request.form['email']
        mdp = request.form['mdp']
        mdp_hache = hashlib.sha1(mdp.encode()).hexdigest()
        Pro = Pro.query.filter_by(email=email).first()

        if Pro:
            if Pro.mdp == mdp_hache:
                response = make_response(redirect(url_for('dashboard')))
                response.set_cookie('user_id', str(Pro.id), secure=True, httponly=True, samesite='Strict')
                return response
            else:
                error_message = "Mot de passe incorrect. Veuillez réessayer."
        else:
            error_message = "Email non trouvé. Vous n'etes pas enregistré en tant que professionnel."

    return render_template('connexion.html', error_message=error_message)

# Route pour le dashboard après la connexion
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# Route pour afficher le profil du médecin connecté et permettre la modification du mot de passe
@app.route('/profil', methods=['GET', 'POST'])
def profil():
    error_message_profile = None  # Message d'erreur du profil
    error_message_form = None  # Message d'erreur du formulaire
    success_message = None # Message de succès de modification
    user_id = request.cookies.get('user_id')

    if user_id:
        current_user = Pro.query.get(int(user_id))

    if request.method == 'POST':
        if 'modifier_mot_de_passe' in request.form:
            mot_de_passe_actuel = request.form['mot_de_passe_actuel']
            nouveau_mot_de_passe = request.form['nouveau_mot_de_passe']
            confirmer_mot_de_passe = request.form['confirmer_mot_de_passe']

            # Vérification du mot de passe actuel
            if hashlib.sha1(mot_de_passe_actuel.encode()).hexdigest() != current_user.mdp:
                error_message_form = "Mot de passe actuel incorrect. Veuillez réessayer."
            elif nouveau_mot_de_passe != confirmer_mot_de_passe:
                error_message_form = "Les nouveaux mots de passe ne correspondent pas. Veuillez réessayer."
            else:
                # Mise à jour du mot de passe
                current_user.mdp = hashlib.sha1(nouveau_mot_de_passe.encode()).hexdigest()
                db.session.commit()
                success_message = "Mot de passe mis à jour avec succès."

    return render_template('profil.html', current_user=current_user, error_message_profile=error_message_profile, error_message_form=error_message_form, success_message=success_message)
