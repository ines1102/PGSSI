from app import app, db
import hashlib

# Enveloppez le code qui nécessite le contexte de l'application Flask avec app.app_context()
with app.app_context():
    # Définition du modèle Pro dans la base de données
    class Pro(db.Model):
        _bind_key_ = 'users'
        __tablename__ = 'pro'  # Nom de la table dans la base de données
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        email = db.Column(db.String(80), nullable=False)
        mdp = db.Column(db.String(120), nullable=False)
        is_connected = False  # Ajout de l'attribut is_connected pour suivre l'état de connexion

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
    
     # Vérifiez s'il y a déjà un administrateur
    existing_admin = Admin.query.filter_by(nom='admin').first()

    # Si aucun administrateur n'existe, créez-en un
    if not existing_admin:
        mdp="admin"
        mdp_hache = hashlib.sha1(mdp.encode()).hexdigest()
        admin = Admin(nom='admin', mdp=mdp_hache)
        db.session.add(admin)
        db.session.commit()
