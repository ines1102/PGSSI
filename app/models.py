from app import app, db
import hashlib
import secrets
import time
import qrcode
import os
import string
import random

# Définition du modèle Pro dans la base de données
class Pro(db.Model):
    _bind_key_ = 'users'
    __tablename__ = 'pro'  # Nom de la table dans la base de données
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False)
    mdp = db.Column(db.String(120), nullable=False)
    is_connected = False  # Ajout de l'attribut is_connected pour suivre l'état de connexion

    def __init__(self, email):
        self.email = email
        self.mdp = self.generate_temporary_password()
    
    def generate_temporary_password(self, length=8):
        """Generate a temporary password with random alphanumeric characters."""
        # Définition des caractères possibles pour le mot de passe temporaire
        characters = string.ascii_letters + string.digits  # lettres majuscules et minuscules + chiffres
        # Génération du mot de passe temporaire en choisissant des caractères aléatoires
        temporary_password = ''.join(random.choice(characters) for _ in range(length))
        return temporary_password
    
    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.is_connected  # Renvoie True uniquement si l'utilisateur est connecté

    def is_anonymous(self):
        return False


# Définition du modèle Admin dans la base de données
class Admin(db.Model):
    _bind_key_ = 'users'
    __tablename__ = 'admin'  # Nom de la table dans la base de données
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(80), nullable=False)
    mdp = db.Column(db.String(120), nullable=False)

    def get_id(self):
        return str(self.id)
    
    def is_active(self):
            return True


class Patient(db.Model):
    _bind_key_ = 'users'
    __tablename__ = 'patients'  # Nom de la table dans la base de données
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)
    taille = db.Column(db.Integer, nullable=False)  # En cm
    poids = db.Column(db.Integer, nullable=False)  # En kg
    numero_unique = db.Column(db.String(64), unique=True, nullable=False)  # Ajout d'une colonne pour le numéro unique

    def __init__(self, nom, prenom, sexe, taille, poids):
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.taille = taille
        self.poids = poids
        self.numero_unique = self.generate_unique_key()  # Générer un numéro unique lors de l'initialisation
        # Appel à la méthode generate_qr_code pour générer et enregistrer le QR code
        self.qr_code_filepath = self.generate_qr_code()

    def generate_unique_key(self):
        random_string = secrets.token_hex(16)  # Génération d'une chaîne aléatoire sécurisée
        timestamp = str(int(time.time()))  # Horodatage actuel converti en chaîne
        combined_string = random_string + timestamp  # Concaténation de la chaîne aléatoire et de l'horodatage

        # Hachage de la chaîne combinée pour obtenir un numéro unique
        unique_key = hashlib.sha256(combined_string.encode()).hexdigest()
        return unique_key  # Retourne le numéro unique généré

    def generate_qr_code(self):
        # Création du dossier qr_code s'il n'existe pas déjà
        if not os.path.exists("qr_code"):
            os.makedirs("qr_code")

        # Chemin complet du fichier QR code
        qr_code_filepath = os.path.join("qr_code", f"{self.numero_unique}.png")

        # Génération du QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.numero_unique)
        qr.make(fit=True)

        # Enregistrement du QR code dans le dossier qr_code
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_code_filepath)

        return qr_code_filepath
    def __repr__(self):
        return f"Patient('{self.nom}', '{self.prenom}', '{self.sexe}', {self.taille}cm, {self.poids}kg, {self.numero_unique})"
        
# Enveloppez le code qui nécessite le contexte de l'application Flask avec app.app_context()
with app.app_context():
    # Créez toutes les tables définies dans les modèles de votre application
    db.create_all()

    # Vérifiez s'il y a déjà un administrateur
    existing_admin = Admin.query.filter_by(nom='admin').first()

    # Si aucun administrateur n'existe, créez-en un
    if not existing_admin:
        mdp = "admin"
        mdp_hache = hashlib.sha256(mdp.encode()).hexdigest()
        admin = Admin(nom='admin', mdp=mdp_hache)
        db.session.add(admin)
        db.session.commit()