# -*- coding: utf-8 -*-


"""
This module provides the different messages to display.
"""


NB_MATCH = 4


def view_intro_home_menu():
    """ Displays an introduction to the home menu. """
    print("\n ### Menu Principal ### \n"
          "\n"
          "-- Que souhaitez vous réaliser ? --\n")


def view_actors_menu():
    """ Displays a warning message before the actors menu. """
    print("\n ### Attention ### \n"
          "Si des joueurs doivent être importés, commencer par cela.")


def view_input_new_actor():
    """ Displays a message introducing a player input coming. """
    view = "\n ### Nouveau joueur ### \n"
    view += "\n -- Entrez les informations demandées: --\n"
    print(view)


def view_tournament_creation():
    """ Displays a message warning of the creation of the tournament. """
    print("\n ### Création du tournoi ### \n"
          "\n"
          "-- Débutons par les informations du tournoi : --\n")


def view_tournament_players(tournament):
    """ Displays a warning message before the players input. """
    print(f"\n ### Tournoi {tournament.name}: Type d'entrée des joueurs ### \n"
          "\n"
          "-- Attention --\n"
          "pour ajouter des joueurs, "
          "vous devez les avoir enregistrer "
          "depuis le menu principal, \n"
          "puis donner l'identifiant au joueur "
          "pour qu'il le redonne au lancement du tournoi.\n")


def view_validation_new_actor(actor):
    """ Displays a message indicating a player is registered in the tournament. """
    print("\n ### Le joueur suivant a bien été enregistré ### \n")
    print(actor)


def view_id_player(tournament, num=1):
    """ Displays a message introducing the input of the given player of the tournament. """
    print(f"\n ### Tournoi {tournament.name}: Identification de joueur ### \n")
    print(f"-- Joueur {num} --")


def view_validation_players(players):
    """ Displays the list of the tournament players. """
    print("\n -- Les joueurs du tournoi sont : --")
    view = ""
    for player in players:
        view += "\n" + str(player)
    print(view)


def view_launch_tournament(tournament):
    """ Displays a message indicating the start of the tournament. """
    print(f"\n ### Lancement du Tournoi {tournament.name}: ### ")


def view_round_matches(r0und):
    """ Displays the list of the matches of a given round.

    The display is different depending on whether the matches are over or not.
    If the match are all over, the results are displayed too.

    """
    view = f"\n ### Matchs du Tour {r0und.round_nb + 1} " \
           f"du Tournoi {r0und.tournament_ID} : ### \n \n"
    if r0und.matches != {}:
        if r0und.finished:
            view += "Les matchs ont vu s'affronter : \n"
        else:
            view += "Les matchs verront s'affronter : \n"
        for num_match in range(NB_MATCH):
            view += f"{num_match + 1}. " \
                       f"{r0und.matches[num_match].player1.name}" \
                       f" et {r0und.matches[num_match].player2.name} \n"
            if r0und.finished:
                if r0und.matches[num_match].winner == 0:
                    view += "Match nul. \n"
                if r0und.matches[num_match].winner == 1:
                    view += f"Victoire de " \
                               f"{r0und.matches[num_match].player1.name}. \n"
                if r0und.matches[num_match].winner == 2:
                    view += f"Victoire de " \
                               f"{r0und.matches[num_match].player2.name}. \n"
    print(view)


def view_players_rank(list_of_players):
    """ Displays the updated tournament ranking. """
    for rank in range(1, len(list_of_players) + 1):
        view = ""
        for player in list_of_players:
            if rank == 1:
                if player.place == rank:
                    view += f"1er : {player.name}" \
                            + " " * (20 - len(player.name)) \
                            + f"{player.points}"
            else:
                if player.place == rank:
                    view += f"{rank}eme: {player.name}" \
                            + " " * (20 - len(player.name)) \
                            + f"{player.points}"
        print(view)


def view_wait_match_results():
    """ Displays a waiting message until all match results are given. """
    print("\n ### En attente de résultats: ### \n"
          "\n"
          "Lorsqu'un match est terminé, "
          "indiquez le numéro du match "
          "pour entrez les résultats")


def view_tournament_final(tournament):
    """ Displays a message to indicate the end of the tournament and its ranking.

    :param tournament: the tournament that ends
    :return: None
    """
    print("\n ### Fin des matchs ### \n"
          "\n"
          "-- Classement final -- \n")
    view_players_rank(tournament.list_of_players)


def view_validation_actors_imported(actors):
    """ Displays the information about imports.

    If the list of actors is empty, it's indicated.
    If some players are imported, the number of players is displayed
    and then the players imported.

    :param actors: the list of imported actors
    :return: None

    """
    print("\n ### Import de joueurs ### \n")
    if len(actors) == 0:
        view = "Base de donnée vide, aucun import possible"
    else:
        view = f"-- {len(actors)} joueurs importés --"
    print(view)
    for actor in actors:
        print(actor)


def view_validation_actors_exported(exported_actors):
    """ Displays the information about exports.

    It displays the number of exported actors.
    Then it displays the identifier and the name of each exported actor.

    :param exported_actors: the list of exported actors
    :return: None
    """
    view = f"\n Les {len(exported_actors)} personnes ont été exportés \n"
    for actor in exported_actors:
        view += "\n" + actor.actor_id + " " + actor.first_name + " " + actor.last_name
    print(view)


def view_no_actor_id():
    """ Displays a message alerting that no player with this identifier was found. """
    print("Il n'y a pas de joueurs avec cet identitifant")


def view_import_no_tournament():
    """ Displays a message alerting that no tournament has been imported. """
    print("\n ---------------------------------- "
          "\n --- Aucun tournoi sauvegardé ! --- "
          "\n ---------------------------------- ")
