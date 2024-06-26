# Importation des modules nécessaires
from flask import render_template, request, redirect, url_for, session, make_response 
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app import app, db
from app.models import Pro, Admin, Patient
import hashlib
import jsonify


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
    return render_template('index.html')

# Route pour la page d'inscription des professionnels
@app.route('/ajouter_pro', methods=['GET', 'POST'])
def ajouter_pro():
    error_message = None
    success_message = None

    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.form['email']

        # Vérifier si un professionnel avec le même e-mail existe déjà
        existing_pro = Pro.query.filter_by(email=email).first()

        if existing_pro:
            error_message = "Un professionnel avec cet e-mail existe déjà. Veuillez vous connecter."
        else:
            # Créer un nouveau professionnel
            new_pro = Pro(email=email)

            # Ajouter le nouveau professionnel à la base de données
            db.session.add(new_pro)
            db.session.commit()
            success_message = "Le professionnel a été inscrit avec succès."

    # Si la méthode est GET, afficher simplement le formulaire d'inscription
    return render_template('ajouter_pro.html', error_message=error_message, success_message=success_message)

#@socketio.on('message')
#def handle_message(message):
#    print('received message : '+message)
#   socketio.send('echo: '+message)

#@socketio.on('send_temporary_password')
#def send_temporary_password(data):
#    email = data['email']
#    temporary_password = data['temporary_password']
    # Code pour envoyer l'e-mail temporaire...
#    socketio.emit('send_temporary_password_response', {'email': email, 'temporary_password': temporary_password})

# Route pour la connexion d'un professionnel
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    error_message = None

    if request.method == 'POST':
        email = request.form['email']
        mdp = request.form['mdp']
        mdp_hache = hashlib.sha256(mdp.encode()).hexdigest()
        pro = Pro.query.filter_by(email=email).first()

        if pro:
            if pro.mdp == mdp_hache:
                pro.is_connected = True  # Définir is_connected sur True lorsque l'utilisateur est connecté
                login_user(pro)
                return render_template('dashboard.html')
            else:
                error_message = "Mot de passe incorrect. Veuillez réessayer."
        else:
            error_message = "Email non trouvé. Vous n'êtes pas enregistré en tant que professionnel."

    return render_template('index.html', error_message=error_message)

# Route pour la connexion des administrateurs
@app.route('/admin_access', methods=['GET', 'POST'])
def admin_access():
    error_message = None
    return render_template('admin_access.html', error_message=error_message)

@app.route('/connexion_admin', methods=['GET', 'POST'])
def connexion_admin():
    error_message = None

    if request.method == 'POST':
        nom = request.form.get('nom')
        mdp = request.form.get('mdp')

        if nom is not None and mdp is not None:
            mdp_hache = hashlib.sha256(mdp.encode()).hexdigest()
            admin = Admin.query.filter_by(nom=nom).first()

            if admin:
                if admin.mdp == mdp_hache:
                    response = make_response(redirect(url_for('dashboard_admin')))
                    response.set_cookie('admin_id', str(admin.id), secure=True, httponly=True, samesite='Strict')
                    return render_template('dashboard_admin.html', error_message=error_message)
                else:
                    error_message = "Mot de passe incorrect. Veuillez réessayer."
            else:
                error_message = "Email non trouvé. Vous n'êtes pas enregistré en tant qu'administrateur."
        else:
            error_message = "Tous les champs doivent être remplis."

    # Retourner le modèle avec le message d'erreur si la méthode est GET ou si la méthode est POST et qu'il y a une erreur
    return render_template('admin_access.html', error_message=error_message)

# Route pour ajouter un patient
@app.route('/ajouter_patient', methods=['GET', 'POST'])
def ajouter_patient():
    error_message = None
    success_message = None

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        sexe = request.form.get('sexe')
        taille = request.form['taille']
        poids = request.form['poids']

        # Vérifier si le patient existe déjà dans la base de données
        existing_patient = Patient.query.filter_by(nom=nom, prenom=prenom).first()

        if existing_patient:
            error_message = "Ce patient existe déjà dans la base de données."
        else:
            # Créer un nouveau patient
            nouveau_patient = Patient(nom=nom, prenom=prenom, sexe=sexe, taille=taille, poids=poids)

            # Ajouter le nouveau patient à la base de données
            db.session.add(nouveau_patient)
            db.session.commit()

            # Message de succès
            success_message = "Le patient a été ajouté avec succès."

    # Afficher le formulaire d'ajout de patient avec les messages appropriés
    return render_template('ajouter_patients.html', error_message=error_message, success_message=success_message)


@app.route('/delete_patients', methods=['POST'])
def delete_patients():
    if request.method == 'POST':
        # Récupérer les identifiants des patients à supprimer depuis le formulaire
        patient_ids = request.form.getlist('patientIds[]')

        # Supprimer les patients de la base de données
        for patient_id in patient_ids:
            patient = Patient.query.get(patient_id)
            if patient:
                db.session.delete(patient)

        # Appliquer les changements dans la base de données
        db.session.commit()

        # Rediriger vers une autre page après la suppression
        return redirect(url_for('patients'))
    
@app.route('/delete_pro', methods=['POST'])
def delete_pro():
    if request.method == 'POST':
        # Récupérer les identifiants des pro à supprimer depuis le formulaire
        pro_ids = request.form.getlist('proIds[]')

        # Supprimer les pro de la base de données
        for pro_ids in pro_ids:
            pro = Pro.query.get(pro_ids)
            if pro:
                db.session.delete(pro)

        # Appliquer les changements dans la base de données
        db.session.commit()

        # Rediriger vers une autre page après la suppression
        return redirect(url_for('pro'))

# Route pour la déconnexion
@app.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    numero_unique = request.args.get('numero_unique')
    if numero_unique:
        # Recherche du patient correspondant au numéro unique dans la base de données
        patient = Patient.query.filter_by(numero_unique=numero_unique).first()
        if patient:
            # Si le patient est trouvé, affichez ses informations
            return render_template('fiche_patient.html', patient=patient)
        else:
            # Si aucun patient n'est trouvé, renvoyer un message d'erreur JSON ou une page d'erreur
            return jsonify(error="Aucun patient trouvé avec ce numéro unique.")
    else:
        # Si aucun numéro unique n'est fourni, affichez simplement le dashboard ou une page d'erreur
        return render_template('dashboard.html')

# Route pour le dashboard de l'administrateur après la connexion
@app.route('/dashboard_admin')
@login_required
def dashboard_admin():
    return render_template('dashboard_admin.html')

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
        if hashlib.sha256(mot_de_passe_actuel.encode()).hexdigest() != current_user.mdp:
            error_message_form = "Mot de passe actuel incorrect. Veuillez réessayer."
        elif nouveau_mot_de_passe != confirmer_mot_de_passe:
            error_message_form = "Les nouveaux mots de passe ne correspondent pas. Veuillez réessayer."
        else:
            # Mise à jour du mot de passe
            current_user.mdp = hashlib.sha256(nouveau_mot_de_passe.encode()).hexdigest()
            db.session.commit()
            success_message = "Mot de passe mis à jour avec succès."

    return render_template('profil.html', error_message_profile=error_message_profile, error_message_form=error_message_form, success_message=success_message)

# Route pour afficher les patients dans un tableau
@app.route('/patients')
def patients():
    patients = Patient.query.all()
    return render_template('afficher_patients.html', patients=patients)

# Route pour afficher les patients dans un tableau
@app.route('/pro')
def pro():
    pros = Pro.query.all()
    return render_template('afficher_pro.html', pros=pros)


# Route pour afficher la fiche d'un patient
@app.route('/fiche_patient')
def fiche_patient():
    # Récupérer le numéro unique du patient à partir de la requête GET
    numero_unique = request.args.get('numero_unique')

    # Rechercher le patient correspondant dans la base de données en utilisant le numéro unique
    patient = Patient.query.filter_by(numero_unique=numero_unique).first()

    # Passer les informations du patient au modèle fiche_patient.html pour affichage
    return render_template('fiche_patient.html', patient=patient)