from .. app import db

# tables de relations = propriétés du modèle conceptuel, issues de l'ontologie CIDOC CRM

"""
Dans un premier temps les tables de relation n'avaient pas de clés primaires sur db.sqlite. 
Cependant, l'ORM ne peut pas parser les références d'un modèle sans clé primaire. 
Une clé étrangère peut être une clé primaire, et nous aurions pu choisir les meilleurs candidats de chaque table de
relations comme clé primaire, mais cette approche aura à terme des limites car toutes les clés étrangères doivent 
théoriquement pouvoir se répéter. 
Par ailleurs, si la documentation flask-sqlalchemy recommande d'utiliser des tables et non pas des modèles pour les 
tables de relation, nous avons préféré de le faire tout de même car ces tables contiennent d'autres informations 
que les clés étrangères.
références : 
https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships
https://stackoverflow.com/questions/24872541/could-not-assemble-any-primary-key-columns-for-mapped-table
https://stackoverflow.com/questions/17636106/can-a-foreign-key-act-as-a-primary-key
"""



# CIDOC CRM P132 : Spaciotemporally overlaps with
class Spaciotemporally_overlaps_with(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event_within_event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    description = db.Column(db.Text)
    id_flask = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)


# CIDOC CRM P53 : Has former or current location
class Has_location(db.Model):
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    from_date = db.Column(db.Text)
    to_date = db.Column(db.Text)
    description = db.Column(db.Text)
    id_flask = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)


# CIDOC CRM P94 : Has created
class Has_produced(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'), nullable=False)
    description = db.Column(db.Text)
    id_flask = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)


# CIDOC CRM P107 : Has current or former member
class Is_member(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    from_date = db.Column(db.Text)
    to_date = db.Column(db.Text)
    description = db.Column(db.Text)
    id_flask = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)


# CIDOC CRM P12 : Was present at
class Was_present(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'))
    from_date = db.Column(db.Text)
    to_date = db.Column(db.Text)
    id_flask = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)