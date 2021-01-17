import datetime

from chess.models.game import Tournament
from chess.models.actors import Actor
from chess.models.database import DataBaseHandler

from chess.views.menuview import MenuView
from chess.views.flow import view_validation_new_actor, view_input_new_actor, \
    view_intro_home_menu, view_tournament_creation, view_tournament_players,\
    view_id_player, view_launch_tournament, view_round_matchs, \
    view_validation_actors_imported, view_tournament_final, \
    view_validation_actors_exported, view_validation_players, \
    view_import_no_tournament

from chess.views.reports import report_actors_by_alpha, report_actors_by_rank,\
    report_tournaments_list, report_tournament_players, \
    report_tournament_matchs, report_tournament_rounds

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
        launch the home menu.
        A loop while to browse between the controllers.
        :return: None
        """
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class Actors:
    """
    Store the actors in a class attribute,
    the keys are the actors id and the values
    are the instances of actors.
    """
    actors = {}

    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        handler = DataBaseHandler()
        num_actors, actors = handler.import_actors()
        view_validation_actors_imported(actors)
        for actor in actors:
            Actors.actors[actor.actor_id] = actor
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
    Handle the main menu
    """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        view_intro_home_menu()
        self.menu.add("auto", "Importer des joueurs", ImportActors())
        self.menu.add("auto", "Ajouter un nouveau joueur", ImportActors(new_player=True))
        self.menu.add("auto", "Lancer un tournoi", TournamentCreation())
        self.menu.add("auto", "Reprendre un tournoi", ResumeTournament())
        self.menu.add("auto", "Obtenir un rapport", ReportMenu())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class TournamentCreation:
    """
    Handle the tournament creation
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
                      "Ajouter les joueurs par leur identifiant",
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
        handler = DataBaseHandler()
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
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        actors = []
        actors_id = []
        while len(actors) < NB_PLAYERS:
            num_player = len(actors) + 1
            view_id_player(self.tournament, num_player)
            message = "Vous pouvez revenir au menu principal en entrant 00000000. \nVeuillez indiquer " \
                      f"l'identifiant du joueur {num_player}: "
            error_message = ""
            actor_id = input_tournament_players(message)
            bug_dont_exist = 0
            bug_already_in = 0
            while actor_id in actors_id or actor_id not in Actors.actors:
                if actor_id == "00000000":
                    handler = HomeMenuController()
                    return handler()
                if actor_id in actors_id:
                    if bug_dont_exist == 0:
                        error_message = "Erreur: ce joueur est déjà présent dans le tournoi. "
                    bug_dont_exist += 1
                if actor_id not in Actors.actors:
                    if bug_already_in == 0:
                        error_message = "Erreur: identifiant inconnu. "
                    bug_already_in += 1
                actor_id = input_tournament_players(error_message + message)
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
        if not self.tournament:
            view_import_no_tournament()
            return HomeMenuController()
        num_round = len(self.tournament.rounds)
        if num_round == 0:
            view_launch_tournament(self.tournament)                               # Affichage lancement tournoi
        if num_round == 4:
            view_tournament_final(self.tournament.list_of_players)
        else:
            self.tournament.init_round(num_round)                                 # Instance de round et définition des matchs
            view_round_matchs(self.tournament.rounds[num_round])                  # Affichage des matchs
            winners = input_match_results(self.tournament.rounds[num_round])      # Attente, entrée des gagnants
            self.tournament.register_round_results(num_round, winners)            # Entrées dans instance de round
            view_round_matchs(self.tournament.rounds[num_round])                  # Affichage résultats
            return TournamentPause(self.tournament)                               # Export TDB ?


class ResumeTournament:
    def __call__(self):
        handler = DataBaseHandler()
        tournament = handler.import_tournament()
        return LaunchTournament(tournament)


class ImportActors:
    def __init__(self, new_player=False):
        self.new_player = new_player
        self.handler = HomeMenuController()

    def __call__(self):
        handler = DataBaseHandler()
        num_actors, actors = handler.import_actors()
        view_validation_actors_imported(actors)
        for actor in actors:
            Actors.actors[actor.actor_id] = actor
        tournament_table = handler.database.table("tournament")
        tournament_table.truncate()
        if self.new_player:
            self.handler = Actors()
        return self.handler()


class ExportActors:
    def __init__(self, actors):
        self.actors = actors

    def __call__(self):
        handler = DataBaseHandler()
        for actor in self.actors:
            handler.export_actor(actor)
        view_validation_actors_exported(self.actors)
        #actors_table = handler.database.table("actors")
        #actors_table.truncate()


class ReportMenu:
    """
    Menu des rapports
    """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "Liste des acteurs", ActorsList())
        self.menu.add("auto", "Liste des tournois", TournamentsList())
        self.menu.add("auto", "Rapports pour un tournoi", TournamentRapportMenu())
        self.menu.add("auto", "Retour au Menu principal", HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class ActorsList:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "Trier par ordre alphabétique", ActorsListAlphabetical())
        self.menu.add("auto", "Trier selon leur classement", ActorsListRank())
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto", "Retour au Menu principal", HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class ActorsListAlphabetical:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        report_actors_by_alpha()
        self.menu.add("auto", "Retour au choix du tri", ActorsList())
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto", "Retour au Menu principal", HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class ActorsListRank:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        report_actors_by_rank()
        self.menu.add("auto", "Retour au choix du tri", ActorsList())
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto", "Retour au Menu principal", HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class TournamentsList:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        report_tournaments_list()
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto", "Retour au Menu principal", HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class TournamentRapportMenu:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "Liste des joueurs du tournoi", TournamentPlayersList())
        self.menu.add("auto", "Liste des matchs du tournoi", TournamentMatchsList())
        self.menu.add("auto", "Liste des matchs du tournoi", TournamentRoundsList())
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto", "Retour au Menu principal", HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class TournamentPlayersList:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        report_tournament_players()
        self.menu.add("auto", "Retour au menu rapport du tournoi", TournamentRapportMenu())
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto", "Retour au Menu principal", HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class TournamentMatchsList:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        report_tournament_matchs()
        self.menu.add("auto", "Retour au menu rapport du tournoi", TournamentRapportMenu())
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto", "Retour au Menu principal", HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.handler


class TournamentRoundsList:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        report_tournament_rounds()
        self.menu.add("auto", "Retour au menu rapport du tournoi", TournamentRapportMenu())
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto", "Retour au Menu principal", HomeMenuController())
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
