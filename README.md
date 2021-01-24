# Projet 4
<h2> Installation</h2>
Sur le terminal se placer sur un dossier cible. <br>
<br>
<b>Copier les fichiers :</b> <br>
Sur le terminal tapper successivement : <br>
<ul>
    <li>git clone https://github.com/S0Imyr/Projet4.git </li>
    <li>cd Projet4</li>
</ul>
<br>
<b>Installer l'environnement virtuel :</b> <br>
Sur le terminal tapper successivement : <br>
<ul>
    <li>python -m venv env</li>
    <li>source env/Scripts/activate (ou "source env/bin/activate" sur Linux et Mac).</li>
</ul>
<br>
<b>Installer les packages :</b> <br>
Sur le terminal tapper : <br>
<ul>
    <li>pip install -r requirements.txt</li>
</ul>

<h2> Exécution </h2>
Sur le terminal tapper : <br>
<ul>
    <li>python main.py</li>
</ul>
Il s'agit ensuite de naviguer entre les menus en indiquant le nombre associé au menu ou à l'action que l'on souhaite réaliser.


<h2> Valider le code avec flake8 </h2>
Sur le terminal tapper : <br>
<ul>
    <li>pip install flake8-html</li>
    <li>flake8 chess --format=html --htmldir=flake_report</li>
</ul>
Vous trouverez dans le dossier Projet4, un dossier flake_report avec les rapports de flake8.
Cliquer sur index pour avoir la synthèse.