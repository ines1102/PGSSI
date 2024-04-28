from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)

# Configuration de la base de données principale
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pro.db'

# Configuration des binds pour des bases de données supplémentaires
app.config['SQLALCHEMY_BINDS'] = {
    'patients': 'sqlite:///data.db'
}

db = SQLAlchemy(app)

# Initialisation de l'extension LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'connexion'  # 'connexion' est le nom de la route de connexion

# Importer les vues après la création de 'app' et 'db'
from app import views
