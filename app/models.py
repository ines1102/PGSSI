from app import db

# Définition du modèle Pro dans la base de données
class Pro(db.Model):
    _bind_key_ = 'pro'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    mdp = db.Column(db.String(120), nullable=False)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

# Définition du modèle Admin dans la base de données
class Admin(db.Model):
    _bind_key_ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    mdp = db.Column(db.String(120), nullable=False)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True