# -*- coding: utf-8 -*-


"""
This module handles the menu and the navigation between them.
"""


import datetime

from chess.models.tournament import Tournament
from chess.models.actors import Actor
from chess.models.database import DataBaseHandler

from chess.views.menuview import MenuView
from chess.views.flow import view_validation_new_actor, view_input_new_actor,\
    view_intro_home_menu, view_tournament_creation, view_tournament_players,\
    view_id_player, view_launch_tournament, view_round_matches, \
    view_validation_actors_imported, view_tournament_final, \
    view_validation_actors_exported, view_validation_players, \
    view_import_no_tournament, view_players_rank, view_actors_menu, \
    view_no_actor_id

from chess.views.reports import report_actors_by_alpha, report_actors_by_rank, \
    report_tournaments_list, report_tournament_players, \
    report_tournament_matches, report_tournament_rounds, \
    report_no_tournament, view_tournament_reports

from chess.controllers.menus import Menu
from chess.controllers.input import tournament_inputs, input_actor, \
    input_match_results, input_tournament_players, input_tournament_id,\
    input_actor_id, input_actor_new_rank


NB_PLAYERS = 8
NB_MATCH = 4
NB_ROUND = 4
ID_WIDTH = 8


class BrowseControllers:
    """ Handles the navigation between controllers. """
    def __init__(self):
        """ The attribute controller stores the next controller."""
        self.controller = None

    def start(self):
        """
        Launches the home menu.
        A loop while to browse between the controllers.
        :return: None
        """
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    """ Handles the main menu. """
    def __init__(self):
        """
        The attribute menu is a instance of Menu, the option are added in __call__.
        The attribute view handles the display of the menu.
        """
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        """ Calls the display of the menu's introduction.
        The menu is created and the get_user_choice method
        asks for the user choice.
        """
        view_intro_home_menu()
        self.menu.add("auto", "Rentrer ou modifier des joueurs", ActorsMenu())
        self.menu.add("auto", "Lancer un tournoi", TournamentCreation())
        self.menu.add("auto", "Reprendre un tournoi", ResumeTournament())
        self.menu.add("auto", "Obtenir un rapport", ReportMenu())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class ActorsMenu:
    """ Handles the menu of players settings. """
    def __init__(self):
        """
        The attribute menu is a instance of Menu, the option are added in __call__.
        The attribute view handles the display of the menu.
        """
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        """ Calls the display of the menu's introduction.
        The menu is created and the get_user_choice method
        asks for the user choice.
        """
        view_actors_menu()
        self.menu.add("auto", "Importer les joueurs", ImportActors())
        self.menu.add("auto", "Ajouter un nouveau joueur", Actors())
        self.menu.add("auto", "Modifier le classement d'un joueur", ActorsRank())
        self.menu.add("auto",
                      "Retour au menu principal et sauvegarder les joueurs",
                      ExportActors(Actors.actors.values()))
        self.menu.add("auto",
                      "Retour au menu principal sans sauvegarder les joueurs",
                      HomeMenuController())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class Actors:
    """ Handles Actors creation.

    Stores the actors in a class attribute,
    the keys are the actors id and the values
    are the instances of actors.

    """
    actors = {}

    def __init__(self):
        """ Defines the next menu. """
        self.next_menu = ActorsMenu()

    def __call__(self):
        """
        Calls the display and the input of a new player.
        Then the corresponding actor instance is created.
        The instance is stored in the class attribute actors
        in a dictionary and it calls the display of the
        validation of the new player creation.
        """
        view_input_new_actor()
        actor_arguments = input_actor()
        actor = Actor(actor_arguments[0],
                      actor_arguments[1],
                      actor_arguments[2],
                      actor_arguments[3],
                      actor_arguments[4])
        Actors.actors[actor.actor_id] = actor
        view_validation_new_actor(actor)
        return self.next_menu


class ImportActors:
    """ Handles the actors imports. """
    def __init__(self):
        """ The next controller is already set at ActorsMenu. """
        self.next_menu = ActorsMenu()

    def __call__(self):
        """
        It calls the display of imports.
        The imported players fulfill the class attribute Actors.actors.
        The database table is cleared after the import.
        """
        handler = DataBaseHandler()
        num_actors, actors = handler.import_actors()
        view_validation_actors_imported(actors)
        for actor in actors:
            Actors.actors[actor.actor_id] = actor
        actors_table = handler.database.table("actors")
        actors_table.truncate()
        return self.next_menu()


class ExportActors:
    """ Handles the actors exports. """
    def __init__(self, actors):
        """ Stores the actors to export in the attribute actors """
        self.actors = actors

    def __call__(self):
        """ Exports actor on by one and updates the last id"""
        handler = DataBaseHandler()
        for actor in self.actors:
            handler.export_actor(actor)
        Actor.last_actor_id = "0" * ID_WIDTH
        view_validation_actors_exported(self.actors)
        return HomeMenuController()


class ActorsRank:
    """ Handles the modification of a player's ranking. """
    def __init__(self, next_menu=ActorsMenu()):
        self.menu = Menu()
        self.view = MenuView(self.menu)
        self.next_menu = next_menu

    def __call__(self):
        actor_id = input_actor_id()
        database = DataBaseHandler()
        actor = {}
        if not database.import_actor(actor_id) and actor_id not in Actors.actors:
            view_no_actor_id()
        else:
            if actor_id in Actors.actors:
                actor = Actors.actors[actor_id]
            elif database.import_actor(actor_id):
                actor = database.import_actor(actor_id)
            view_validation_new_actor(actor)
            new_rank = input_actor_new_rank()
            actor.rank = new_rank
            Actors.actors[actor.actor_id] = actor
            view_validation_new_actor(actor)

        self.menu.add("auto", "Modifier le classement d'un autre joueur", ActorsRank(self.next_menu))
        self.menu.add("auto", "Retour", self.next_menu)

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class TournamentCreation:
    """ Handles the tournament creation. """
    def __init__(self):
        self.tournament = None
        self.last_id = "0" * ID_WIDTH

    def __call__(self):
        handler = DataBaseHandler()
        Tournament.last_tournament_id = handler.import_last_tournament_id()
        view_tournament_creation()
        tournament_arguments = tournament_inputs()
        self.tournament = Tournament(tournament_arguments[0],
                                     tournament_arguments[1],
                                     tournament_arguments[2],
                                     tournament_arguments[3])
        self.tournament.start_date = datetime.date.today()
        return TournamentPlayersMenu(self.tournament)


class TournamentPlayersMenu:
    """ Defines a menu to input the players of the tournament. """
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
        return user_choice.next_menu


class TournamentPlayers:
    """ Handles the input of the players of the tournament. """
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
            message = "Vous pouvez revenir au menu principal " \
                      "en entrant 00000000. \nVeuillez indiquer " \
                      f"l'identifiant du joueur {num_player}: "
            error_message = ""
            actor_id = input_tournament_players(message)
            bug_dont_exist = 0
            bug_already_in = 0
            while actor_id in actors_id or actor_id not in Actors.actors:
                if actor_id == "0"*ID_WIDTH:
                    next_menu = HomeMenuController()
                    return next_menu()
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
    """ Handles the course of a tournament.

    Launches the tournament, there is a kind of a loop
    between LaunchTournament and TournamentPause
    for the 4 rounds.

    """
    def __init__(self, tournament):
        self.tournament = tournament

    def __call__(self):
        if not self.tournament or self.tournament.finished:
            view_import_no_tournament()
            return HomeMenuController()
        num_round = len(self.tournament.rounds)
        if num_round == 0:
            view_launch_tournament(self.tournament)
        if num_round == 4:
            view_tournament_final(self.tournament)
            self.tournament.end_tournament()
            database = DataBaseHandler()
            database.export_finished_tournament(self.tournament)
            return HomeMenuController()
        else:
            self.tournament.init_round(num_round)
            view_round_matches(self.tournament.rounds[num_round])
            winners = input_match_results(self.tournament.rounds[num_round])
            self.tournament.register_round_results(num_round, winners)
            view_round_matches(self.tournament.rounds[num_round])
            view_players_rank(self.tournament.list_of_players)
            return TournamentPause(self.tournament)


class TournamentPause:
    """ Defines a Pause menu

    Defines a menu to give the alternative of interrupting
    or continuing the tournament

    """
    def __init__(self, tournament):
        self.tournament = tournament
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        self.menu.add("auto",
                      "Continuer et passer au tour suivant",
                      LaunchTournament(self.tournament))
        self.menu.add("auto",
                      "Changer le classement d'un joueur",
                      ActorsRank(TournamentPause(self.tournament)))
        self.menu.add("auto",
                      "Interrompre le tournoi",
                      TournamentInterruption(self.tournament))

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class TournamentInterruption:
    """
    Interrupts the tournament and load the datas in the database
    to be able to resume it.
    """
    def __init__(self, tournament):
        self.tournament = tournament
        handler = DataBaseHandler()
        handler.export_interrupted_tournament(self.tournament)

    def __call__(self):
        return Ending()


class ResumeTournament:
    """Resumes a tournament.

    It imports the datas and progress of
    the last tournament interrupt.

    """
    def __call__(self):
        handler = DataBaseHandler()
        tournament = handler.import_interrupted_tournament()
        return LaunchTournament(tournament)


class ReportMenu:
    """
    Defines a menu between the different reports
    """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        self.menu.add("auto", "Liste des acteurs", ActorsList())
        self.menu.add("auto", "Liste des tournois", TournamentsList())
        self.menu.add("auto",
                      "Rapports pour un tournoi",
                      TournamentReportInput())
        self.menu.add("auto",
                      "Retour au Menu principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class ActorsList:
    """ Defines a menu to obtain the actors lists """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        self.menu.add("auto",
                      "Trier par ordre alphabétique",
                      ActorsListAlphabetical())
        self.menu.add("auto",
                      "Trier selon leur classement",
                      ActorsListRank())
        self.menu.add("auto",
                      "Obtenir un autre rapport",
                      ReportMenu())
        self.menu.add("auto",
                      "Retour au Menu principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class ActorsListAlphabetical:
    """ Handles the list of actors in alphabetical order """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        handler = DataBaseHandler()
        num_actors, actors_list = handler.import_actors()
        report_actors_by_alpha(actors_list)
        self.menu.add("auto", "Retour au choix du tri", ActorsList())
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto",
                      "Retour au Menu principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class ActorsListRank:
    """ Handles the list of actors in rank order """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        handler = DataBaseHandler()
        num_actors, actors_list = handler.import_actors()
        report_actors_by_rank(actors_list)
        self.menu.add("auto", "Retour au choix du tri", ActorsList())
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto",
                      "Retour au Menu principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class TournamentsList:
    """ Handles the list of tournaments """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        handler = DataBaseHandler()
        tournaments = handler.import_tournaments()
        report_tournaments_list(tournaments)
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto",
                      "Retour au Menu principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class TournamentReportInput:
    """ Asks for the tournament we want to get reports from """
    def __call__(self):
        tournament_id = input_tournament_id()
        db = DataBaseHandler()
        tournament = db.find_tournament_by_id(tournament_id)
        if tournament:
            handler = TournamentReportMenu(tournament)
        else:
            report_no_tournament()
            handler = TournamentReportInput()
        return handler


class TournamentReportMenu:
    """ Handles the menu of reports of a tournament"""
    def __init__(self, tournament):
        self.tournament = tournament
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        view_tournament_reports(self.tournament)
        self.menu.add("auto",
                      "Liste des joueurs du tournoi",
                      TournamentPlayersList(self.tournament))
        self.menu.add("auto",
                      "Liste des matchs du tournoi",
                      TournamentMatchesList(self.tournament))
        self.menu.add("auto",
                      "Liste des tours du tournoi",
                      TournamentRoundsList(self.tournament))
        self.menu.add("auto",
                      "Obtenir un autre rapport",
                      ReportMenu())
        self.menu.add("auto",
                      "Retour au Menu principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class TournamentPlayersList:
    """ Displays the report of the players of a tournament """
    def __init__(self, tournament):
        self.tournament = tournament
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        self.menu.add("auto",
                      "Trier par ordre alphabétique",
                      PlayersList(self.tournament, "Alphabetical"))
        self.menu.add("auto",
                      "Trier selon leur classement",
                      PlayersList(self.tournament, "By rank"))
        self.menu.add("auto",
                      "Retour au menu rapport du tournoi",
                      TournamentReportMenu(self.tournament))
        self.menu.add("auto",
                      "Obtenir un autre rapport",
                      ReportMenu())
        self.menu.add("auto",
                      "Retour au Menu principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class PlayersList:
    """ Displays the list of the players of a tournament.

    The argument sort is equal to "By rank" or "Alphabetical"
     so, the players are ranked according to this.

    """
    def __init__(self, tournament, sort):
        self.tournament = tournament
        self.sort = sort
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        report_tournament_players(self.tournament, self.sort)
        self.menu.add("auto", "Retour au choix du tri", TournamentPlayersList(self.tournament))
        self.menu.add("auto", "Obtenir un autre rapport", ReportMenu())
        self.menu.add("auto",
                      "Retour au Menu principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class TournamentMatchesList:
    """ Displays the report of the matches of a tournament """
    def __init__(self, tournament):
        self.tournament = tournament
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        report_tournament_matches(self.tournament)
        self.menu.add("auto",
                      "Retour au menu rapport du tournoi",
                      TournamentReportMenu(self.tournament))
        self.menu.add("auto",
                      "Obtenir un autre rapport",
                      ReportMenu())
        self.menu.add("auto",
                      "Retour au Menu principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class TournamentRoundsList:
    """ Displays the report of the rounds of a tournament """
    def __init__(self, tournament):
        self.tournament = tournament
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        report_tournament_rounds(self.tournament)
        self.menu.add("auto",
                      "Retour au menu rapport du tournoi",
                      TournamentReportMenu(self.tournament))
        self.menu.add("auto",
                      "Obtenir un autre rapport",
                      ReportMenu())
        self.menu.add("auto",
                      "Retour au Menu principal",
                      HomeMenuController())
        self.menu.add("q", "Quitter", Ending())

        user_choice = self.view.get_user_choice()
        return user_choice.next_menu


class Ending:
    """ Displays the exit screen """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def __call__(self):
        print("Aurevoir")  # A modifier -> views
