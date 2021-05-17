# Projet 4
## Installation
Sur le terminal se placer sur un dossier cible.

***Copier les fichiers :***
Sur le terminal tapper successivement :
 - git clone https://github.com/S0Imyr/Projet4.git
 - cd Projet4

## Installer l'environnement virtuel :

Sur le terminal tapper successivement : 
- python -m venv env</li>
- source env/Scripts/activate (ou "source env/bin/activate" sur Linux et Mac).

## Installer les packages :
Sur le terminal tapper :

- pip install -r requirements.txt</li>


## Exécution
Sur le terminal tapper :

- python main.py

Il s'agit ensuite de naviguer entre les menus en indiquant le nombre associé au menu ou à l'action que l'on souhaite réaliser.


##Valider le code avec flake8
Sur le terminal tapper :

 - pip install flake8-html
 - flake8 chess --format=html --htmldir=flake_report

Vous trouverez dans le dossier Projet4, un dossier flake_report avec les rapports de flake8.
Cliquer sur index pour avoir la synthèse.