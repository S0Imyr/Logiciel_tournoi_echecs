[English](#english-readme) | [Français](#french-readme)
# Chess Tournament Management Software
<a name="english-readme"></a>
Chess Tournament Management Software is a Python application designed to help chess clubs manage their tournaments offline and generate reports.


<a name="table-of-contents-english"></a>
- [Table of Contents](#table-of-contents-english)  
- [Installation](#installation-english)  
- [Configuration](#configuration-english)  

## Installation
<a name="installation-english"></a>

Navigate to a target directory in your terminal.

In the terminal, type the following commands one after the other :  
`git clone https://github.com/S0Imyr/Chess_Tournament_Software.git`  
`cd Chess_Tournament_Software`

In the terminal, type the following commands one after the other:  
`python -m venv env`  
`./env/Scripts/activate` on PC and `source env/bin/activate` on Linux and Mac.  

In the terminal, type:  
`pip install -r requirements.txt`

## Execution
In the terminal, type:

`python main.py`

Then, navigate through the menus by entering the number associated with the menu or action you want to perform.

## Validate the code with flake8
In the terminal, type:  
`pip install flake8-html`  
`flake8 chess --format=html --htmldir=flake_report`  

You will find a folder named "flake_report" in the Logiciel_tournoi_echecs directory with the flake8 reports.  
Click on "index" to view the summary.

# Logiciel de gestion de tournoi d'échecs
<a name="french-readme"></a>

Logiciel de gestion de tournoi d'échecs est une application Python conçue pour aider les clubs d'échecs à gérer leurs tournois hors ligne et à générer des rapports.
Le tournoi respecte le système de tournois "suisse".  
Le programme peut être interrompu en cours de compétition pour être repris par la suite.  
La programmation suit le Design Pattern MVC Modèle Vue Contrôleur

<a name="table-des-matières-français"></a>
- [Table des matières](#table-des-matières-français)  
- [Installation](#installation-français)  
- [Configuration](#configuration-français)  

## Installation
<a name="installation-français"></a>


Sur le terminal se placer sur un dossier cible.

**Copier les fichiers :**
Sur le terminal tapper successivement :  
`git clone https://github.com/S0Imyr/Logiciel_tournoi_echecs.git`  
`cd Logiciel_tournoi_echecs`  

Sur le terminal tapper successivement :  
`python -m venv env`  
`./env/Scripts/activate` sur PC et `source env/bin/activate` sur Linux et Mac.  

Sur le terminal tapper :
`pip install -r requirements.txt`



## Exécution
Sur le terminal tapper :

`python main.py`

Il s'agit ensuite de naviguer entre les menus en indiquant le nombre associé au menu ou à l'action que l'on souhaite réaliser.


## Valider le code avec flake8
Sur le terminal tapper :

`pip install flake8-html`  
`flake8 chess --format=html --htmldir=flake_report`  

Vous trouverez dans le dossier Logiciel_tournoi_echecs, un dossier flake_report avec les rapports de flake8.
Cliquer sur index pour avoir la synthèse.