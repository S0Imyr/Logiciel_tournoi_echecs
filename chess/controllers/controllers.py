import datetime

from chess.models.game import Tournament
from chess.models.actors import Actor
from chess.models.database import DataBaseHandler

from chess.views.menuview import MenuView
from chess.views.flow import view_validation_new_actor, view_input_new_actor, \
    view_intro_home_menu, view_tournament_creation, view_tournament_players,\
    view_id_player, view_launch_tournament, view_round_matchs, \
    view_validation_actors_imported, view_tournament_final, \
    view_validation_export_actors, view_validation_players


from chess.controllers.menus import Menu
from chess.controllers.input import tournament_inputs, input_actor, \
    input_match_results, input_tournament_players

from tinydb import TinyDB


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
    actors = {}

    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        view_input_new_actor()
        actor_arguments = input_actor()
        actor = Actor(actor_arguments[0],
                      actor_arguments[1],
                      actor_arguments[2],
                      actor_arguments[3],
                      actor_arguments[4])
        Actors.actors[actor.actor_id] = actor
        view_validation_new_actor(actor)

        self.menu.add("auto", "Ajouter un nouveau joueur", Actors())
        self.menu.add("auto", "Exporter les joueurs", ExportActors(Actors.actors))
        self.menu.add("auto", "Retour au menu principal", HomeMenuController())
        self.menu.add("q", "Quitter", Ending())
        user_choice = self.view.get_user_choice()
        return user_choice.handler


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

        self.menu.add("auto",
                      "Ajouter les joueurs par id",
                      TournamentPlayers(self.tournament))
        self.menu.add("auto",
                      "Interrompre le tournoi",
                      TournamentPause(self.tournament))
        self.menu.add("auto",
                      "Retour au Menu Principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class TournamentPause:
    def __init__(self, tournament):
        self.tournament = tournament
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        self.menu.add("auto",
                      "Continuer et passer au tour suivant",
                      LaunchTournament(self.tournament))
        self.menu.add("auto",
                      "Interrompre le tournoi",
                      TournamentInterruption(self.tournament))

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class TournamentInterruption:
    def __init__(self, tournament):
        self.tournament = tournament
        handler = DataBaseHandler(TinyDB('db.json'))
        handler.database.table('tournament').truncate()
        handler.export_tournament(self.tournament)

    def __call__(self):
        return Ending()


class TournamentPlayers:
    """
    Gestion de l'entrée des joueurs
    """
    def __init__(self, tournament):
        self.tournament = tournament

    def __call__(self):
        actors = []
        actors_id = []
        while len(actors) < NB_PLAYERS:
            num_player = len(actors) + 1
            view_id_player(self.tournament, num_player)
            message = f"Veuillez indiquer " \
                      f"l'identifiant du joueur {num_player}: "
            actor_id = input_tournament_players(message)
            while actor_id not in Actors.actors:
                message += f"Identifiant inconnu."
                actor_id = input_tournament_players(message)
            actors_id.append(actor_id)
            actor = Actors.actors[actor_id]
            actors.append(actor)
        self.tournament.define_players(actors)
        view_validation_players(actors)
        return LaunchTournament(self.tournament)


class LaunchTournament:
    def __init__(self, tournament):
        self.tournament = tournament

    def __call__(self):
        num_round = len(self.tournament.rounds)
        if num_round == 0:
            view_launch_tournament(self.tournament)                               # Affichage lancement tournoi
        if num_round == 4:
            view_tournament_final()
        else:
            self.tournament.init_round(num_round)                                 # Instance de round et définition des matchs
            view_round_matchs(self.tournament.rounds[num_round])                  # Affichage des matchs
            winners = input_match_results(self.tournament.rounds[num_round])      # Attente, entrée des gagnants
            self.tournament.register_round_results(num_round, winners)            # Entrées dans instance de round
            view_round_matchs(self.tournament.rounds[num_round])                  # Affichage résultats
            return TournamentPause(self.tournament)                               # Export TDB ?


class ResumeTournament:
    def __call__(self):
        handler = DataBaseHandler(TinyDB('db.json'))
        tournament = handler.import_tournament()
        return LaunchTournament(tournament)


class ImportActors:
    def __init__(self):
        pass

    def __call__(self):
        handler = DataBaseHandler(TinyDB('db.json'))
        num_actors, actors = handler.import_actors()
        view_validation_actors_imported(actors)
        for actor in actors:
            Actors.actors[actor.actor_id] = actor
        return HomeMenuController()


class ExportActors:
    def __init__(self, actors):
        self.actors = actors

    def __call__(self):
        handler = DataBaseHandler(TinyDB('db.json'))
        for actor in self.actors:
            handler.export_actor(actor)
        view_validation_export_actors(self.actors)


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
