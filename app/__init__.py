from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ines.a1102@gmail.com'
app.config['MAIL_PASSWORD'] = 'Nessou.A@11022'

mail = Mail()
mail.init_app(app)


# Configuration de la base de données principale
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

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
