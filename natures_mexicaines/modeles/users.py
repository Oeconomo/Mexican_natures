from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .. app import db, login
import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    login = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    # relations
    authorships = db.relationship("Authorship", back_populates="user")

    @staticmethod
    def identification(login, motdepasse):
        """ Identifie l'utilisateur et renvoie ses données

        :param login: Login de l'utilisateur
        :param motdepasse: Mot de passe envoyé par l'utilisateur
        :returns: Si réussite, données de l'utilisateur. Sinon None
        :rtype: User or None
        """
        utilisateur = User.query.filter(User.login == login).first()
        if utilisateur and check_password_hash(utilisateur.password, motdepasse):
            return utilisateur
        return None

    @staticmethod
    def creer(login, email, nom, motdepasse):
        """ Crée un compte utilisateur-rice. Retourne un tuple (booléen, User ou liste).
        Si il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur
        Sinon, elle renvoie True suivi de la donnée enregistrée

        :param login: Login de l'utilisateur-rice
        :param email: Email de l'utilisateur-rice
        :param nom: Nom de l'utilisateur-rice
        :param motdepasse: Mot de passe de l'utilisateur-rice (Minimum 6 caractères)

        """
        erreurs = []
        if not login:
            erreurs.append("Le login fourni est vide")
        if not email:
            erreurs.append("L'email fourni est vide")
        if not nom:
            erreurs.append("Le nom fourni est vide")
        if not motdepasse or len(motdepasse) < 6:
            erreurs.append("Le mot de passe fourni est vide ou trop court")

        # On vérifie que personne n'a utilisé cet email ou ce login
        uniques = User.query.filter(
            db.or_(User.email == email, User.login == login)
        ).count()
        if uniques > 0:
            erreurs.append("L'adresse mail fournie ou le nom d'utilisateur ont déjà été utilisées")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        # On crée un utilisateur
        utilisateur = User(
            name=nom,
            login=login,
            email=email,
            password=generate_password_hash(motdepasse)
        )

        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(utilisateur)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        """ Retourne l'id de l'objet actuellement utilisé

        :returns: ID de l'utilisateur
        :rtype: int
        """
        return self.id

# TODO : implementer API
    """
        def to_jsonapi_dict(self):
        #It ressembles a little JSON API format but it is not completely compatible
        
        return {
            "type": "people",
            "attributes": {
                "name": self.nom
            }
        }
    """


@login.user_loader
def trouver_utilisateur_via_id(identifiant):
    return User.query.get(int(identifiant))


# TODO : remplir la table automatiquement quand un objet est créé
class Authorship(db.Model):
    __tablename__ = "authorship"
    id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    objet_id = db.Column(db.Integer, db.ForeignKey('object.id'))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # relations
    user = db.relationship("User", back_populates="authorships")
    Object = db.relationship("Object", back_populates="authorships")