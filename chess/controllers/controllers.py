from chess.controllers.menus import Menu
from chess.views.menuview import MenuView
from chess.controllers.input import tournament_inputs
from chess.controllers.input import input_actor
import chess.views.flow


NB_PLAYERS = 8


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
        chess.views.flow.view_intro_home_menu()
        self.menu.add("auto", "Lancer un tournoi", TournamentCreation())
        self.menu.add("auto", "Ajouter un nouveau joueur", NewPlayer())
        self.menu.add("auto", "Obtenir un rapport", RapportMenu())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()

        return user_choice.handler


class TournamentCreation:
    """
    Gestionnaire création du tournoi
    """
    def __init__(self):
        self.tournament = None

    def __call__(self):
        chess.views.flow.view_tournament_creation()
        self.tournament = tournament_inputs()

        return TournamentPlayersMenu(self.tournament)


class TournamentPlayersMenu:
    """
    Introduction des joueurs du tournoi
    """
    def __init__(self, tournament):
        self.tournament = tournament
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        chess.views.flow.view_tournament_players(self.tournament)

        self.menu.add("auto", "Ajouter les joueurs par id", TournamentPlayers(self.tournament))
        self.menu.add("auto", "Ajouter un nouveau joueur (sans id)", NewPlayer(self.tournament))
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()

        return user_choice.handler


class TournamentPlayers:
    def __init__(self, tournament):
        self.tournament = tournament

    def __call__(self):
        while len(self.tournament.list_of_players) < NB_PLAYERS:
            num_player = len(self.tournament.list_of_players)+1
            chess.views.flow.view_id_player(num_player)
            chess.controllers.input.define_tournament_player(self.tournament, num_player)
        return LaunchTournament(self.tournament)


class NewPlayer:
    """
    Gestion d'ajout de joueurs
    """
    def __init__(self, tournament=None):
        self.tournament = tournament
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        chess.views.flow.view_new_player()
        actor = input_actor()
        chess.views.flow.view_validation_new_player(actor)
        if self.tournament:
            self.tournament.list_of_players.append(actor)
            return TournamentPlayers(self.tournament)
        return NewPlayer()


class LaunchTournament:
    def __init__(self, tournament):
        self.tournament = tournament

    def __call__(self):
        pass


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
        self.menu.add("q", "Quitter", Ending())

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
