from .. app import db

# Entités du modèle conceptuel, issues de l'ontologie CIDOC CRM

# CIDOC CRM E22 : Human-Made Object
class Object(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    production_date = db.Column(db.Text)
    type = db.Column(db.Text)
    description = db.Column(db.Text)
    image = db.Column(db.Text)
    lien = db.Column(db.Text)
    # relations
    authorships = db.relationship("Authorship", back_populates="Object")

    @staticmethod
    def methode_ajout_objet(name, production_date, type, description, image, lien):
        """ Fonction pour ajouter un objet à la base de données.
            :param *: variables envoyées par le formulaire
            :type * : Text
            :returns: ajout dans la table object """
        erreurs = []
        if not name:
            erreurs.append("veuillez renseigner le nom de l'objet")
        if not type:
            erreurs.append("veuillez renseigner le type d'objet")
        if not image:
            erreurs.append("veuillez fournir une URL vers une image (cette base vise à référencer et valoriser des objets visuels numériques)")
        if not description:
            erreurs.append("veuillez fournir une description")

        # verifier que le nom de l'objet est unique
        uniques = Object.query.filter(
            db.or_(Object.name == name)
        ).count()
        if uniques > 0:
            erreurs.append("Cet objet semble être déjà dans la base de données")

        # si il y a une ou plusieurs eurreurs
        if len(erreurs) > 0:
            return False, erreurs

        # On ajoute l'entrée
        nouvel_object = Object(
            name=name,
            production_date=production_date,
            type=type,
            description=description,
            image=image,
            lien=lien
        )
        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(nouvel_object)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, nouvel_object
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def methode_suprression_objet(objet_id):
        """ Supprimer un objet de la table object dans la base de données.
            :param objet_id: id de l'objet à supprimer
            :type objet: integer
            :returns: suppression de l'objet sélectionné de la table objects de la base de données """
        supprimer = Object.query.get(objet_id)
        try:
            # TODO la suppression ne fonctionne pas, probablement ici car le résultat est l'erreur
            db.session.delete(supprimer)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


# CIDOC CRM E21 : Person
class Person(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    birth = db.Column(db.Text)
    death = db.Column(db.Text)
    description = db.Column(db.Text)
    image = db.Column(db.Text)


# CIDOC CRM E74 : Group
class Group(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    creation = db.Column(db.Text)
    dissolution = db.Column(db.Text)
    objet_historique = db.Column(db.Boolean)
    description = db.Column(db.Text)
    image = db.Column(db.Text)


# CIDOC CRM E5 : Event
class Event(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    start = db.Column(db.Text)
    end = db.Column(db.Text)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    description = db.Column(db.Text)
    image = db.Column(db.Text)


# CIDOC CRM E53 : Place
class Place(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    lat = db.Column(db.Text)
    lon = db.Column(db.Text)
    description = db.Column(db.Text)


