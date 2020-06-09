# WikiWFFR
Ensemble de scripts pour faciliter l'édition du Wiki Warframe FR

## Prérequis
- Python 3 (voir les dépendances du projet pour la version minimale requise)
- SLPP (https://github.com/SirAnthony/slpp; https://pypi.org/project/SLPP/)

## Contenu du dépot
- analyse.py : Fichier de tests, à ne pas utiliser
- droptables.py : Script permettant l'analyse, la modification et la mise à jour de la base de données "DropTable"
- modUtils.py : Script permettant l'analyse, la modification et la mise à jour de la base de données "Mods"

## TODO List
### Global
- Faire une interface graphique pour faciliter le travail
- Écrire un tutoriel d'installation

### Base de données des mods
- ~~Possibilité de charger des fichiers de données provenant des wikis~~
==> Partiellement effectué, requiert une édition des fichiers de données à la main pour que cela fonctionne
- Chargement automatique des fichiers depuis le wiki FR/EN
- Mise à jour du contenu de la BDD en se basant sur les pages des mods du wiki FR

## Changelogs

- v0.1 (09/06/2020) : 
    - Version initiale du dépot
    - Ajout de la classe modUtils, permettant de mettre à jour la base de données des mods
    
## License et Auteurs
Le code présent dans ce dépot est fournit suivant la license GPL v3.\
N'hésitez surtout pas à suggérer des modifications, donner vos remarques, et signaler des bugs.\
Auteur : DoctorTee