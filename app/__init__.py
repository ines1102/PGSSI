from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource 

app = Flask(__name__)

api = Api(app)

# Configuration de la base de données principale
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_medecins.db'  # BD principale

# Configuration des binds pour des bases de données supplémentaires
app.config['SQLALCHEMY_BINDS'] = {
    'patients': 'sqlite:///data_patients.db'
}

db = SQLAlchemy(app)

from app import views
