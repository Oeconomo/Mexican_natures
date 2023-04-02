<p align="center"><img width="923" alt="home" src="https://github.com/Oeconomo/Mexican_natures/blob/main/natures_mexicaines/static/images/home.png?raw=true"></p>

# Natures mexicaines

Natures mexicaines fédère des objets visuels ayant servi à "inventer" la nature mexicaine au XIXe siècle, soit des artefacts ayant été mobilisés pour développer une culture intellectuelle sur les richesses naturelles d'une nation en construction. Il réunit des ressources numériques provenant de plusieurs institutions à travers le monde et en propose de nouvelles, avec l'ambition de cartographier leurs circulations au XIXe siècle dans le cadre d'un réseau de production de connaissances comprenant le Mexique, les États-Unis et la France.

Cet instrument continuera à être développé au long de ce parcours doctoral. Ses contenus et sa base de données seront renforcés dans la perspective d'en faire un instrument de valorisation en même temps qu'un appui scientifique robuste. 

La base de données qui alimente ce site est matérialisée par un modèle physique SQLite. Le modèle conceptuel est constitué d'entités et de propriétés (associations) issues de l'ontologie CIDOC CRM et ambitionne d'évoluer en conformité avec ses préconisations, ce qui permettra d'assurer sa cohérence au fil de sa complexification. le CIDOC CRM est un modèle de référence non prescriptif, orienté objet, pouvant être déployé dans une base de données relationnelles. Dans le cadre de ce projet, son intérêt réside dans la possibilité de croiser des données spatiales et temporelles constituant la vie d'objets patrimoniaux, en relation avec des informations contextuelles qui leur donnent leur signification culturelle et historique. Il permet de les mettre en lien avec les agents (personnes, institutions, évènements) qui les concernent historiquement. 

Cette application web a été développé dans le cadre du master "Technologies numériques appliquées à l'histoire" de l'École nationale des chartes. Elle sert à appuyer et à valoriser une recherche doctorale effectuée en codirection à Paris 1 Panthéon-sorbonne et à l'École des hautes études en sciences sociales.


## Fonctionnalités 
- Met en valeur une base de données SQLite avec des notices (objets, personnes, personnes morales, événements) liées entre elles.
- Index par type d'entité
- Formulaire d'inscription et de connexion pour des utilisateurs qui souhaitent contribuer à la base. Une fois connécté, il est possible d'ajouter ou d'éliminer des entrées
- formulaire de recherche
- carte des entités et des circulations (en cous de développement)
- onglet ressources numériques
- visionneur et implémentation iiif pour mettre à disposition des objets numériques complexes (en cous de développement)
- API (en cous de développement)
- recherche avancée et autocomplétaion avec icônes (en cous de développement)
- facettes pour ordonner les index
- récupération automatique d'objets numériques pour des sites avec des corpus importants (Gallica, Europeana) (en cous de développement)
- hierarchie de droits pour les utilisateurs


## Installer et lancer Natures mexicaines 
Les commandes sont à effectuer dans un terminal.  

**Prérequis**

Votre ordinateur doit avoir les installations suivantes : 
- python3 (tutoriel : https://www.w3schools.com/python/default.asp)
- git (tutoriel : https://www.w3schools.com/git/)

**Installer l'application** 
- Cloner le dêpot sur votre ordinateur : `git clone https://github.com/Oeconomo/Mexican_natures`
- Se déplacer dans le dossier cloné : `cd ~/chemin/vers/le/dossier`
- Installer un environnement virtuel : `virtualenv -p python3 env`
- Activer l'environnement virtuel : `source env/bin/activate`
- Installer les paquets nécessaires : `pip install -r requirements.txt`

**Lancer l'application**

Chaque fois que vous voudrez lancer l'application, tapez les commandes suivantes :
- ouvrir un terminal
- Se déplacer dans le dossier cloné : `cd ~/chemin/vers/le/dossier` (si vous venez d'installer l'application, cela est déjà fait)
- Activer l'environnement virtuel : `source env/bin/activate` (si vous venez d'installer l'application, cela est déjà fait)
- Lancer l'application : `python3 run.py`
- Cliquer sur le lien ou taper l'adresse du serveur local sur un navigateur
- Pour fermer l'application, fermez la fenêtre du terminal ou arrêtez le processus (control+c). Pour désactiver l'environnement virtuel : `deactivate`
