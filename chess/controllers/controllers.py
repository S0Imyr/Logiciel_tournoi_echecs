from chess.controllers.menus import Menu
from chess.views.menuview import MenuView


class BrowseControllers:
    def __init__(self):
        self.controller = None

    def start(self):
        """
        lance le menu d'accueil puis boucle pour naviguer
        entre les différents controleurs
        :return: None
        """
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    """
    Controleur du menu principal
    """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "Lancer un tournoi", Tournament())
        self.menu.add("auto", "Ajouter un nouveau joueur", NewPlayer())
        self.menu.add("auto", "Obtenir un rapport", RapportMenu())
        self.menu.add("q", "quitter", Ending())

        user_choice = self.view.get_user_choice()

        return user_choice.handler


class Tournament:
    """
    Gestionnaire du tournoi
    """
    def __init__(self):
        pass

    def __call__(self):
        print("Lancement tournoi") # A modifier -> views
        return


class NewPlayer:
    """
    Menu d'ajout de joueurs
    """

    def __call__(self):
        print("Définition d'un nouveau joueur")  # A modifier -> views
        return


class RapportMenu:
    """
    Menu des rapports
    """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "Liste des acteurs", ())
        self.menu.add("auto", "Liste des tournois", ())
        self.menu.add("auto", "Détail d'un tournoi", ())
        self.menu.add("auto", "Menu principal", HomeMenuController())
        self.menu.add("q", "quitter", Ending())

        user_choice = self.view.get_user_choice()

        return user_choice.handler


class Ending:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        print("Aurevoir")  # A modifier -> views

if __name__ == "__main__":
    app = BrowseControllers()
    app.start()