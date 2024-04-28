# Importation des modules nécessaires
from flask import render_template, request, redirect, url_for, session, make_response 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required
from app import app, db
from app.models import Pro, Admin
import hashlib

# Clé secrète pour la gestion des sessions
app.secret_key = "123"

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
    success_message = None

    if request.method == 'POST':
        try:
            email = request.form['email']
            mdp = request.form['mdp']
            mdp_hache = hashlib.sha1(mdp.encode()).hexdigest()

            pro_existant = Pro.query.filter_by(email=email).first()
            if pro_existant:
                error_message = "Un professionnel avec cet e-mail existe déjà. Veuillez vous connecter."
            else:
                nouveau_pro = Pro(email=email, mdp=mdp_hache)
                db.session.add(nouveau_pro)
                db.session.commit()
                success_message = "Le professionnel a été inscrit avec succès."
        except KeyError:
            error_message = "Tous les champs doivent être remplis."

    return render_template('inscription.html', error_message=error_message, success_message=success_message)

# Route pour la connexion d'un professionnel
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    error_message = None

    if request.method == 'POST':
        email = request.form['email']
        mdp = request.form['mdp']
        mdp_hache = hashlib.sha1(mdp.encode()).hexdigest()
        pro = Pro.query.filter_by(email=email).first()

        if pro:
            if pro.mdp == mdp_hache:
                login_user(pro)
                return redirect(url_for('dashboard'))
            else:
                error_message = "Mot de passe incorrect. Veuillez réessayer."
        else:
            error_message = "Email non trouvé. Vous n'êtes pas enregistré en tant que professionnel."

    return render_template('connexion.html', error_message=error_message)


# Route pour la connexion des administrateurs
@app.route('/admin_access', methods=['GET', 'POST'])
def admin_access():
    error_message = None

    if request.method == 'POST':
        email = request.form.get('email')
        mdp = request.form.get('mdp')

        if email is not None and mdp is not None:
            mdp_hache = hashlib.sha1(mdp.encode()).hexdigest()
            admin = Admin.query.filter_by(email=email).first()

            if admin:
                if admin.mdp == mdp_hache:
                    response = make_response(redirect(url_for('dashboard')))
                    response.set_cookie('admin_id', str(admin.id), secure=True, httponly=True, samesite='Strict')
                    return response
                else:
                    error_message = "Mot de passe incorrect. Veuillez réessayer."
            else:
                error_message = "Email non trouvé. Vous n'êtes pas enregistré en tant qu'administrateur."
        else:
            error_message = "Tous les champs doivent être remplis."

    return render_template('admin_access.html', error_message=error_message)


# Route pour la déconnexion
@app.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('index'))

# Route pour le dashboard après la connexion
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Route pour afficher le profil du médecin connecté et permettre la modification du mot de passe
@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    error_message_profile = None  # Message d'erreur du profil
    error_message_form = None  # Message d'erreur du formulaire
    success_message = None # Message de succès de modification

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

    return render_template('profil.html', error_message_profile=error_message_profile, error_message_form=error_message_form, success_message=success_message)
