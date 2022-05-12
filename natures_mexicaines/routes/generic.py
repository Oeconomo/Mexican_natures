from flask import render_template, request, flash, redirect
from sqlalchemy import or_
from flask_login import login_user, current_user, logout_user, login_required

from ..constantes import entrees_par_page
from natures_mexicaines.app import app, name, login
from natures_mexicaines.modeles.users import User
from natures_mexicaines.modeles.entities import Object, Person, Group, Event, Place
from natures_mexicaines.modeles.properties import Spaciotemporally_overlaps_with, Has_location, Has_produced, Is_member, \
    Was_present


# les modules non utilisés seront implémentés à l'avenir

# Racine de l'application
@app.route("/")
def home():
    objects = Object.query.all()
    persons = Person.query.all()
    # Notre modèle conceptuel rassemble les personnes morales étudiées ("objets historiques)" et les institutions
    # actuelles de conservation au sein d'une même entité "group". Dans la colonne objet_historique, La valeur booléenne
    # True permet de signaler les groupes qui font partie du réseau transnational étudié :
    moral_persons = Group.query.filter(Group.objet_historique == "1").all()
    return render_template("pages/home.html", name=name, objects=objects, persons=persons, moral_persons=moral_persons)


# TODO : implémenter cartographie des objets, événements, lieux
@app.route("/carte")
def carte():
    return render_template("pages/carte.html", name=name)


# TODO : implémenter filtres de recherche, et autocomplétion avec miniature à l'aide d'une API
@app.route("/rechercher")
def rechercher():
    return render_template("pages/rechercher.html", name=name)


@app.route("/recherche")
def recherche():
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = []
    titre = "Recherche"
    if motclef:
        resultats = Object.query.filter(or_(
            Object.name.like("%{}%".format(motclef)),
            Object.production_date.like("%{}%".format(motclef)),
            Object.type.like("%{}%".format(motclef)),
            Object.description.like("%{}%".format(motclef)))).paginate(page=page, per_page=entrees_par_page)
        titre = 'Recherche : "' + motclef + '"'
    return render_template("pages/recherche.html", resultats=resultats, titre=titre, keyword=motclef)


# TODO : implémenter un index général. Pour connecter toutes les tables entité, créér une table de relation "entités "les référençant.
"""
@app.route("/index")
def index():
"""


@app.route("/objects/index")
def index_objects():
    """ Renvoie l'index des objets par ordre alphabétique."""
    objects = Object.query.order_by(Object.type.asc()).all()
    return render_template("pages/index_objets.html", name=name, objects=objects)


@app.route("/persons/index")
def index_persons():
    """ Renvoie l'index des personnes par ordre alphabétique."""
    persons = Person.query.order_by(Person.birth.asc()).all()
    return render_template("pages/index_persons.html", name=name, persons=persons)


@app.route("/moral_persons/index")
def index_moral_persons():
    """ Renvoie l'index des personnes morales étudiées par ordre alphabétique."""
    # on filtre les instances qui ne sont pas des objets d'étude historique
    moral_persons = Group.query.filter(Group.objet_historique == "1").all()
    return render_template("pages/index_moral_persons.html", name=name, moral_persons=moral_persons)


@app.route("/conservation_institution/index")
def index_institutions_conservation():
    """ Renvoie l'index des institutions de conservation par ordre alphabétique."""
    # on filtre les instances qui ne sont pas des institutions de conservation
    institutions_conservation = Group.query.filter(Group.objet_historique == "0").order_by(Group.name.asc()).all()
    return render_template("pages/index_institutions_conservation.html", name=name,
                           institutions_conservation=institutions_conservation)


@app.route("/events/index")
def index_events():
    """ Renvoie l'index des événements par ordre alphabétique."""
    events = Event.query.order_by(Event.start.asc()).all()
    return render_template("pages/index_events.html", name=name, events=events)


@app.route("/places/index")
def index_places():
    """ Renvoie l'index des villes par ordre alphabétique."""
    places = Place.query.order_by(Place.name.asc()).all()
    return render_template("pages/index_places.html", name=name, places=places)


@app.route("/objects/<int:objet_id>")
def is_object(objet_id):
    """ Renvoie chaque objets de la base de données
    :param objet_id: identifiant de l'objet, int
    :return: render_template("pages/object.html")
    """
    object = Object.query.get_or_404(objet_id)
    # Les images et les liens apparaissent que s'ils existent :
    if object.image != 'None':
        image = object.image
    if object.lien != 'None':
        lien = object.lien

    # on établie des relations de chaque entrée avec d'autres tables, en la mettant de coté quand il y en a pas :

    # personnes :
    # TODO : transformer ce code en fonction avec pour arguments la table ciblée, afin de ne pas tout re-écrire
    #  Nous pourrons ainsi implémenter toutes les relations du modèle conceptuel dans les notices des entités
    producteurs = Has_produced.query.filter(Has_produced.object_id == objet_id).all()
    # si l'objet se trouve référencé dans la table relationnelle concernée :
    if producteurs:
        # on crée une liste pour rassembler tous les éléments
        personnes = []
        for producteur in producteurs:
            # on vérifie que l'objet est bien lié à un id de personne (car il peut être présent pour faire référence
            # à d'autres entités)
            if producteur.person_id is not None:
                personne_refers = producteur.person_id
                # on ajoute l'élément à la liste
                personnes += Person.query.filter(Person.id == personne_refers).all()
            else:
                # (on a pas réussi à faire référence à une cellule de type NULL dans les conditions du gabarit HTML,
                # donc on fait référence à une chaîne de caractères arbitraire)
                # si l'objet est présent mais que sa valeur est NULL :
                personnes = "rien"
    # Si l'objet ne se trouve pas dans la table relationnelle concernée :
    else:
        personnes = "rien"

    # localisations (code similaire, on en fera une fonction) :
    # seul l'objet 1 a une localisation renseignée
    locations = Has_location.query.filter(Has_location.object_id == objet_id).all()
    if locations:
        places = []
        for location in locations:
            if location.place_id is not None:
                place_refers = location.place_id
                places += Place.query.filter(Place.id == place_refers).all()
            else:
                places = "rien"
    else:
        places = "rien"
    return render_template("pages/object.html", name=name, object=object, image=image, lien=lien,
                           places=places, personnes=personnes)


@app.route("/persons/<int:person_id>")
def person(person_id):
    """ Renvoie chaque personne dans la base de données
    :param person_id: identifiant de la personne, int
    :return: render_template("pages/person.html")
    """
    person = Person.query.get_or_404(person_id)
    if person.image != 'None':
        image = person.image

    # relations avec d'autres tables
    # voici un exemple d'un autre type d'entité référencé dans la même table :

    # institutions concernées (code similaire) :
    est_membre = Is_member.query.filter(Is_member.person_id == person_id).all()
    if est_membre:
        institutions = []
        for organisme in est_membre:
            if organisme.group_id is not None:
                institution_refers = organisme.group_id
                institutions += Group.query.filter(Group.id == institution_refers).all()
            else:
                institutions = "rien"
    else:
        institutions = "rien"
    return render_template("pages/person.html", name=name, person=person, image=image,
                           institutions=institutions)


@app.route("/moral_person/<int:moral_person_id>")
def moral_person(moral_person_id):
    """ Renvoie chaque personne morale étudiée
    :param moral_person_id: identifiant de la personne morale, int
    :return: render_template("pages/moral_person.html")
    """
    moral_person = Group.query.get_or_404(moral_person_id)
    if moral_person.image != 'None':
        image = moral_person.image
    return render_template("pages/moral_person.html", name=name, moral_person=moral_person, image=image)


@app.route("/conservation_institution/<int:institution_conservation_id>")
def institution_conservation(institution_conservation_id):
    """ Renvoie chaque institution de conservation
    :param institution_conservation_id: identifiant de l'institutiton de conservation, int
    :return: render_template("pages/conservation_institution.html)
    """
    institution_conservation = Group.query.get_or_404(institution_conservation_id)
    if institution_conservation.image != 'None':
        image = institution_conservation.image
    return render_template("pages/conservation_institution.html", name=name,
                           institution_conservation=institution_conservation, image=image)


@app.route("/events/<int:event_id>")
def event(event_id):
    """ Renvoie chaque événement renseigné dans la base de données
    :param event_id: identifiant de l'événement, int
    :return: render_template("pages/event.html")
    """
    event = Event.query.get_or_404(event_id)
    if event.image != 'None':
        image = event.image

    # Exemple de relation (1-n), un événement ne pouvant être associé qu'à une ville
    ville = Place.query.filter(Place.id == event.place_id).all()
    return render_template("pages/event.html", name=name, event=event, image=image,
                           ville=ville)


# page d'information
@app.route("/mentions_legales")
def mentions_legales():
    return render_template("pages/mentions_legales.html", name=name)


# page d'information
@app.route("/about")
def about():
    return render_template("pages/about.html", name=name)


# page d'information
@app.route("/conceptual_model")
def modele_conceptuel():
    return render_template("pages/modele_conceptuel.html", name=name)


@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route pour les inscriptions
    """
    if request.method == "POST":
        # On a statut, données, car la fonction inscription dans users.py retourne soit "False, erreurs", soit "True,
        # utilisateur"
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html", name=name)


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # GET enverra vers la page "connexion.html", POST permettra de connecter l'utilisateur
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
    return render_template("pages/connexion.html", name=name)


login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")


@app.route("/create", methods=["GET", "POST"])
@login_required
def ajout():
    return render_template("pages/ajout.html", name=name)


@app.route("/objects/create_object", methods=["GET", "POST"])
@login_required
def ajout_objet():
    """ Route vers le formulaire d'ajout objet.
    """
    if request.method == "POST":
        statut, donnees = Object.methode_ajout_objet(
            name=request.form.get("name", None),
            production_date=request.form.get("production_date", None),
            type=request.form.get("type", None),
            description=request.form.get("description", None),
            image=request.form.get("image", None),
            lien=request.form.get("lien", None)
        )
        if statut is True:
            flash("Objet ajouté à la base", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(donnees), "error")
            return render_template("pages/ajout_objet.html")
    else:
        return render_template("pages/ajout_objet.html", name=name)


@app.route("/objects/<int:objet_id>/delete", methods=["POST", "GET"])
@login_required
def supprimer_objet(objet_id):
    """ Route pour le formulaire de suppression d'un objet.
        :param objet_id: identifiant de l'objet
        :type objet_id: int
    """
    supprimer = Object.query.get(objet_id)

    if request.method == "POST":
        statut = Object.methode_suprression_objet(
            objet_id=objet_id
        )
        if statut is True:
            flash("L'objet a été supprimé de la base", "success")
            return redirect("/")
        else:
            flash("Échec", "error")
            return redirect("/")
    else:
        return render_template("pages/delete_object.html", supprimer=supprimer)


@app.route("/en_construction")
def en_construction():
    """ Renvoie vers une page indiquant que la ressource est en phase de développement.
    :return: render_template("pages/page_en_construction.html")
    """
    return render_template("pages/page_en_construction.html", name=name)