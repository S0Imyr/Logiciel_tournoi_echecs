import datetime

from chess.models.game import Tournament
from chess.models.actors import Actor

from chess.views.menuview import MenuView
from chess.views.flow import view_validation_new_player, view_new_actor, \
    view_intro_home_menu, view_tournament_creation, view_tournament_players,\
    view_id_player, view_launch_tournament, view_round_matchs

from chess.controllers.menus import Menu
from chess.controllers.input import tournament_inputs, input_actor, \
    input_match_results, input_tournament_players


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

    def __call__(self):
        view_new_actor()
        actor_arguments = input_actor()
        actor = Actor(actor_arguments[0],
                      actor_arguments[1],
                      actor_arguments[2],
                      actor_arguments[3],
                      actor_arguments[4])
        self.actors[actor.actor_id] = actor
        view_validation_new_player(actor)
        # Enregistrer dans la DB

        self.menu.add("auto", "Ajouter un nouveau joueur", Actors())
        self.menu.add("auto", "Retour au menu principal", HomeMenuController())
        self.menu.add("q", "Quitter", Ending())
        user_choice = self.view.get_user_choice()
        return user_choice.handler

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
        view_intro_home_menu()
        self.menu.add("auto", "Lancer un tournoi", TournamentCreation())
        self.menu.add("auto", "Reprendre un tournoi", ResumeTournament())
        self.menu.add("auto", "Ajouter un nouveau joueur", Actors())
        self.menu.add("auto", "Importer des joueurs", ImportActors())
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
        view_tournament_creation()
        tournament_arguments = tournament_inputs()
        self.tournament = Tournament(tournament_arguments[0],
                                     tournament_arguments[1],
                                     tournament_arguments[2],
                                     tournament_arguments[3])
        self.tournament.start_date = datetime.date.today()
        # Export information ? step 0
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
        view_tournament_players(self.tournament)

        self.menu.add("auto", "Ajouter les joueurs par id", TournamentPlayers(self.tournament))
        self.menu.add("auto", "Retour au Menu Principal", HomeMenuController())
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
        players = []
        while len(self.tournament.list_of_players) < NB_PLAYERS:
            num_player = len(self.tournament.list_of_players) + 1
            view_id_player(self.tournament, num_player)
            message = f"Veuillez indiquer "
            f"l'identifiant du joueur {num_player}: "
            actor_id = input_tournament_players(num_player, message)
            while actor_id not in Actors():  ######
                message += f"Identifiant inconnu."
                actor_id = input_tournament_players(num_player, message)
            players.append(actor_id)
            # view pour valider les joueur mis
        self.tournament.define_players(players)
        # Export
        return LaunchTournament(self.tournament)


class LaunchTournament:
    def __init__(self, tournament):
        self.tournament = tournament

    def __call__(self):
        view_launch_tournament(self.tournament)                                   # Affichage lancement tournoi
        for num_round in range(NB_ROUND):
            self.tournament.start_round(num_round)                                # Instance de round et définition des matchs
            view_round_matchs(self.tournament.rounds[num_round])                  # Affichage des matchs
            winners = input_match_results(self.tournament.rounds[num_round])      # Attente, entrée des gagnants
            self.tournament.register_round_results(num_round, winners)            # Entrées dans instance de round
            view_round_matchs(self.tournament.rounds[num_round])                  # Affichage résultats
            # step += 1
            # Export()                                                            # Export TDB


class ResumeTournament:
    pass


class ImportActors:
    def __init__(self):
        pass

    def __call__(self):
        pass
        """serialized_actors = actors_table.all()
        nb_actors = len(serialized_actors)
        chess.views.flow.view_import_actors(nb_actors)
        return HomeMenuController()"""


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
