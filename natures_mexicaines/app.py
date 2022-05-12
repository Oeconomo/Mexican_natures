from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from .constantes import SECRET_KEY, name

# produire les chemins vers les dossiers template et static
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

# initialiser l'application
app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
)

# On configure le secret flask
app.config['SECRET_KEY'] = SECRET_KEY
# Configuration de la base de données :
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Mise en place de la gestion d'utilisateur-rice-s
login = LoginManager(app)

# import des routes (en fin de fichier pour éviter une boucle d'import)
from .routes import generic
