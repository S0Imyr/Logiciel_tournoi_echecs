# -*- coding: utf-8 -*-


"""
This module handles the different inputs
"""


from chess.utils.conversion import str_into_date


DATE_FORMAT = ["day", "month", "year"]
ID_WIDTH = 8
NB_MATCH = 4


def prompt_number(message, mini=None, maxi=None):
    """ Asks the user to input a number.

    If the user provides an object that is not an integer,
     or an integer that is not between the mini and the maxi (included),
    then the question is asked again, with the appropriate error message.

    :param message: message to ask the input
    :param mini: if it is provided, the input number must be higher
    :param maxi: if it is provided, the input number must be lower
    :return:
    """
    response = input(message)
    response_is_not_number = True
    while response_is_not_number:
        try:
            response = int(response)
            response_is_not_number = False
        except ValueError:
            response = input("Entrée incorrecte, veuillez entrer un nombre: ")
    if mini is None and maxi is None:
        pass
    elif mini is None:
        while not int(response) <= maxi:
            response = input(f"Nombre incorrect, veuillez"
                             f" entrer inférieur à {maxi} : ")
    elif maxi is None:
        while not int(response) >= mini:
            response = input(f"Nombre incorrect, veuillez"
                             f" entrer supérieur à {mini} : ")
    else:
        while not (int(response) >= mini and int(response) <= maxi):
            response = input(f"Nombre incorrect, veuillez"
                             f" entrer un entier entre {mini} et {maxi} : ")
    return int(response)


def prompt_string(message):
    """ Asks the user to enter a character string.

    :param message: message to ask the input
    :return: input
    """
    response = input(message)
    return response


def prompt_id_num(message, length=ID_WIDTH):
    """ Asks the user to enter a identifier which is a numeric string.

    The length is the length of the identifier asked.

    :param message: message to ask the input
    :param length: the length of the identifier
    :return: input
    """
    response = input(message)
    while len(response) != length:
        response = input(f"Entrée incorrecte. Veuillez renseigner"
                         f" un identifiant contenant {length} nombres: ")
    response_is_not_number = True
    while response_is_not_number:
        try:
            int(response)
            response_is_not_number = False
        except ValueError:
            response = input(f"Entrée incorrecte. Veuillez renseigner"
                             f" un identifiant contenant {length} nombres: ")
    return response


def prompt_propositions(proposals, message_add="", integer=False):
    """ Asks the user to choose from among the proposals.

    The propositions must be in the form of a dictionary keys, options.
    The user is asked to enter the key of the desired proposal.
    If the answer is not in the dictionary keys of proposals, the request is repeated.

    :param proposals: proposals dictionary
    :param message_add: additional message to display
    :param integer: True if the input must be converted in integer
    :return: input
    """
    proposal_message = ""
    for cle, item in proposals.items():
        proposal_message += f"soit: {cle} pour {item}.\n"
    message = message_add + "\n Choisissez parmi: \n" + proposal_message
    error_message = "Votre réponse ne correspond pas. \n" \
                    "Veuillez indiquer : \n"
    error_message += proposal_message
    response = input(message)
    if integer:
        response = int(response)
    while response not in proposals:
        response = input(error_message)
        if integer:
            response = int(response)
    return response


def prompt_date(message):
    """ Prompts the user to enter a date in a given format.

    If this format is not respected, the request is repeated.

    :param message: message to ask the input
    :return: input date
    """
    date = ""
    is_not_date = True
    while is_not_date:
        response = input(message)
        is_not_slashed = True
        is_not_int = True
        is_not_yyyy = True
        date = response.split("/")
        if len(date) == len(DATE_FORMAT):
            is_not_slashed = False
            try:
                if len(date[2]) == 4:
                    is_not_yyyy = False
                    date = str_into_date(response)
                else:
                    message = "Erreur de format, veuiller écrire la date" \
                              " en respectant le format: jj/mm/aaaa: "
                is_not_int = False
            except ValueError:
                is_not_int = True
                message = "Erreur de format, veuiller écrire la date" \
                          " en respectant le format: jj/mm/aaaa: "
        else:
            message = "Erreur de format, veuiller écrire la date" \
                      " en respectant le format: jj/mm/aaaa: "
        is_not_date = is_not_int or is_not_slashed or is_not_yyyy
    return date


def input_actor():
    """ Asks player information in order to group them into a list.

    :return: actors arguments
    """
    last_name = prompt_string("Votre nom de famille : ")
    first_name = prompt_string("Votre prénom : ")
    birthdate = prompt_date("Votre date de naissance "
                            "en respectant le format: jj/mm/aaaa: ")
    gender = prompt_propositions({"F": "Féminin", "M": "Masculin"})
    rank = prompt_number("Votre classement HATP: ", mini=0)
    actor_arguments = [last_name, first_name, birthdate, gender, rank]
    return actor_arguments


def input_actor_id():
    """ Asks an actor id
    :return: the actor id input
    """
    print("Si vous n'avez pas l'identifiant du joueur, recherchez-le"
          " dans la liste des joueurs.")
    actor_id = prompt_id_num("Veuillez préciser l'identifiant du joueur: ")
    return actor_id


def input_actor_new_rank():
    """ Asks a new rank for an actor.

    :return: actor rank
    """
    rank = prompt_number("Le nouveau classement HATP: ", mini=0)
    return rank


def input_tournament_players(message):
    """ Asks a player id

    :param message: message to ask the input
    :return: the input id
    """
    actor_id = prompt_id_num(message)
    return actor_id


def tournament_inputs():
    """ Gathers the information needed to create a instance of tournament.

    :return: the tournament arguments
    """
    name = prompt_string("Nom du tournoi : ")
    location = prompt_string("Lieu du tournoi : ")
    timer = prompt_propositions({"Bu": "Bullet",
                                 "Bz": "Blitz",
                                 "Cr": "Coup rapide"},
                                message_add="Comment souhaitez vous"
                                            " contrôler le temps ?")
    description = prompt_string("Description (facultatif): ")
    tournament_arguments = [name, location, timer, description]
    return tournament_arguments


def input_match_results(r0und):
    """ Asks to fill in the results of a round

    We start by choosing a match by designating its number
    then we indicate a winner (1 or 2) or a draw by 0.

    :param r0und: the round being played
    :return: the list of the results
    """
    remaining_matchs = {}
    for num, match in r0und.matches.items():
        remaining_matchs[num+1] = f"Match {num+1}: {match.player1.name} vs {match.player2.name}"
    results = [0]*NB_MATCH
    while remaining_matchs != {}:
        num_match = prompt_propositions(remaining_matchs, integer=True)
        print(r0und.matches[num_match - 1])
        result = prompt_number("Indiquer le vainqueur"
                               " par 1 ou 2, ou inscrivez 0"
                               " pour le match nul ", 0, 2)
        results[num_match-1] = result
        del remaining_matchs[num_match]
    return results


def input_tournament_id():
    """ Asks a tournament id

    :return: the tournament id input
    """
    print("Si vous n'avez pas l'identifiant du tournoi, recherchez-le"
          " dans la liste des tournois.")
    tournament_id = prompt_id_num("Veuillez préciser l'identifiant du tournoi: ")
    return tournament_id
