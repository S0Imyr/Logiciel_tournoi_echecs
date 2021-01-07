from chess.controllers.menus import Menu
from chess.views.menuview import MenuView
from chess.controllers.input import tournament_inputs, input_actor, prompt_id_num
import chess.views.flow


NB_PLAYERS = 8
NB_MATCH = 4
NB_ROUND = 4


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


class Actors:
    """
    Gestion des acteurs
    """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)
        self.actors = {}

    def __call__(self, tournament=None, num_player=None):
        chess.views.flow.view_new_player()
        actor = input_actor()
        self.actors[actor.actor_id] = actor
        chess.views.flow.view_validation_new_player(actor)
        if tournament and num_player:
            tournament.list_of_players[num_player-1] = actor.actor_id
            return TournamentPlayers(tournament)
        return Actors()

    def __getitem__(self, item):
        return self.actors[item]

    def __contains__(self, item):
        return item in self.actors


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
        self.menu.add("auto", "Ajouter un nouveau joueur", Actors())
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
    Menu du type d'introduction des joueurs du tournoi
    """
    def __init__(self, tournament):
        self.tournament = tournament
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        chess.views.flow.view_tournament_players(self.tournament)

        self.menu.add("auto", "Ajouter les joueurs par id", TournamentPlayers(self.tournament))
        self.menu.add("auto", "Ajouter un nouveau joueur (sans id)", Actors())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()

        return user_choice.handler


class TournamentPlayers:
    """
    Gestion de l'entrée des joueurs
    """
    def __init__(self, tournament):
        self.tournament = tournament

    def __call__(self):
        print(self.tournament.list_of_players)  ###### test
        while len(self.tournament.list_of_players) < NB_PLAYERS:
            num_player = len(self.tournament.list_of_players) + 1
            chess.views.flow.view_id_player(self.tournament, num_player)
            define_tournament_player(self.tournament, num_player)
        return LaunchTournament(self.tournament)


class LaunchTournament:
    def __init__(self, tournament):
        self.tournament = tournament

    def __call__(self):
        chess.views.flow.view_launch_tournament(self.tournament)                                # Affichage lancement tournoi
        for num_round in range(NB_ROUND):
            self.tournament.start_round(num_round)                                              # Instance de round et définition des matchs
            chess.views.flow.view_round_matchs(self.tournament.rounds[num_round])               # Affichage des matchs
            winners = chess.controllers.input.input_match_results(self.tournament.rounds[num_round])   # Attente, entrée des gagnants
            self.tournament.register_round_results(num_round, winners)                          # Entrées dans instance de round
            chess.views.flow.view_round_matchs(self.tournament.rounds[num_round])               # Affichage résultats
            # DataBase.export()                                                                 # Export TDB


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


def define_tournament_player(tournament, num_player):
    """
    Définit les joueurs d'un tournoi en demandant leur identifiant
    :return: instance de l'acteur
    """
    actor_id = prompt_id_num(f"Veuillez indiquer "
                             f"l'identifiant du joueur {num_player}: ")
    while actor_id not in Actors():  ######
        actor_id = prompt_id_num(f"Identifiant inconnu."
                                 f" Veuillez réessayer "
                                 f"l'identifiant du {num_player}: ")
    tournament.list_of_players.append(Actors().actors[actor_id])

if __name__ == "__main__":
    app = BrowseControllers()
    app.start()
