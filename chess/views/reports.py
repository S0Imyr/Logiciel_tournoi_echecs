# -*- coding: utf-8 -*-


"""
This module provides the different reports.
"""


from operator import attrgetter


def actors_table(actors_list):
    """ Displays a table of the given actors.

    The display follow the the order of the list.

    :param actors_list: the list of actors.
    :return: None
    """
    for actor in actors_list:
        name_characters = len(actor.last_name)+len(actor.first_name)
        rank_characters = len(str(actor.rank))
        print(f"{actor.last_name} {actor.first_name}"
              + " " * (30 - name_characters) +
              f"Classement : rank {actor.rank}"
              + " " * (10 - rank_characters) +
              f"Tournoi joués : {len(actor.list_of_tournaments_played)}")


def report_actors_by_alpha(actors_list):
    """ Displays the given actors in a table sorted alphabetically.

    The actors are sorted alphabetically and then displays in a table.

    :param actors_list: the list of actors.
    :return: None
    """
    sorted_actors = sorted(actors_list, key=attrgetter("first_name"))
    sorted_actors = sorted(sorted_actors, key=attrgetter("last_name"))
    actors_table(sorted_actors)


def report_actors_by_rank(actors_list):
    """ Displays the given actors in a table sorted by rank.

    The actors are sorted by rank and then displays in a table.

    :param actors_list: the list of actors.
    :return: None
    """
    sorted_actors = sorted(actors_list, key=attrgetter("rank"))
    actors_table(sorted_actors)


def report_tournaments_list(tournaments_list):
    """ Displays a tournaments list.

    The identifier, the name and the dates are displayed in that order.

    :param tournaments_list: the list of tournaments.
    :return: None
    """
    for tournament in tournaments_list:
        id_characters = len(tournament.tournament_id)
        name_characters = len(tournament.name)
        print(f"{tournament.tournament_id}"
              + " " * (10 - id_characters) +
              f"Tournoi : {tournament.name}"
              + " " * (20 - name_characters) +
              f"Du: {tournament.start_date} au: {tournament.end_date}")


def report_tournament_players(tournament, sort):
    """ Displays the table of the players of a given tournament in a given order.

    :param tournament:
    :param sort: sorting type
    :return: None
    """
    actors_list = []
    for player in tournament.list_of_players:
        actors_list.append(player.actor)
    if sort == "Alphabetical":
        report_actors_by_alpha(actors_list)
    elif sort == "By rank":
        report_actors_by_rank(actors_list)


def report_tournament_matches(tournament):
    """ Displays the matches of a given tournament

    :param tournament:
    :return: None
    """
    print(f"### Tournoi: {tournament.name} ###")
    for r0und in tournament.rounds:
        print(f"Les matchs du tour {r0und.round_nb + 1}: \n")
        for match in r0und.matchs.values():
            print(str(match))


def report_tournament_rounds(tournament):
    """ Displays the rounds of a given tournament

    :param tournament:
    :return: None
    """
    print(f"### Tournoi: {tournament.name} ###")
    for r0und in tournament.rounds:
        print(str(r0und))


def report_no_tournament():
    """ Displays a warning message that no tournament with this identifier was found."""
    print("Il n'y a pas de tournoi avec cet identifiant"
          " dans la base de données")


def view_tournament_reports(tournament):
    """ Displays a introducing message of the menu of the tournament reports.

    :param tournament:
    :return: None
    """
    print(f"\n ### Rapports du tournoi {tournament.name}. ###"
          f"\n Identifiant du tournoi: {tournament.tournament_id} \n")
