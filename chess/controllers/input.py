import datetime
from chess.models.actors import Actor
from chess.models.game import Tournament

DATE_FORMAT = ["day", "month", "year"]
ID_WIDTH = 8


def prompt_number(message, min=None, max=None):
    """
    Demande à l'utilisateur à l'aide de
    message de saisir un entier.

    Si l'utilisateur fournit un objet qui n'est
    pas un entier, ou un entier qui n'est pas
    entre le min et le max (non compris),
    alors la question est reposée.
    :param message:
    :param min:
    :param max:
    :return:
    """
    response = input(message)
    response_is_not_number = True
    while response_is_not_number:
        try:
            response = int(response)
            response_is_not_number = False
        except ValueError:
            response = input("Entrée incorrecte, veuillez entrer un nombre : ")

    if min is None and max is None:
        pass
    elif min is None:
        while not int(response) < max:
            response = input(f"Nombre incorrect, veuillez"
                             f" entrer inférieur à {max} : ")
    elif max is None:
        while not int(response) > min:
            response = input(f"Nombre incorrect, veuillez"
                             f" entrer supérieur à {min} : ")
    else:
        while not (int(response) > min and int(response) < max):
            response = input(f"Nombre incorrect, veuillez"
                             f" entrer un entier entre {min} et {max} : ")
    return int(response)


def prompt_string(message):
    """
    Demande à l'utilisateur de saisir une chaine de caractère.
    Renvoie la chaîne avec majuscule
    :param message:
    :return: input
    """
    response = input(message)
    response = response.capitalize()
    return response


def prompt_id_num(message, length=ID_WIDTH):
    """
    Demande à l'utilisateur de saisir un identifiant
    qui est une chaîne de caractère numérique
    de longueur length
    :param message: message à montrer
    :param length: la longueur de l'identifiant
    :return:
    """
    response = input(message)
    while len(response) != length:
        response = input(f"Entrée incorrecte. Veuillez renseigner un identifiant contenant {length} nombres: ")
    response_is_not_number = True
    while response_is_not_number:
        try:
            int(response)
            response_is_not_number = False
        except ValueError:
            response = input(f"Entrée incorrecte. Veuillez renseigner un identifiant contenant {length} nombres: ")
    return response


def prompt_propositions(propositions):
    """
    Demande à l'utilisateur de spécifier un genre.
    Si la réponse n'est pas M ou F, la demande
    est refaite.
    :param propositions: dictionnaire des possibilités
    :return: input
    """
    proposal_message = ""
    for cle, item in propositions.items():
        proposal_message += f"soit :{cle} pour {item}.\n"
    message = "Choisissez parmi: \n" + proposal_message
    error_message = "Votre réponse ne correspond pas. \n" \
                    "Veuillez indiquer : \n"
    error_message += proposal_message

    response = input(message)

    while response not in propositions:
        input(error_message)
    return response


def prompt_date(message):
    """
    Demande à l'utilisateur à l'aide de
    message de saisir une date selon un format.
    Si ce format n'est pas respecté, la demande
    est refaite.
    :param message:
    :return: input date
    """
    day = 1
    month = 1
    year = 0
    response_is_not_date = True
    while response_is_not_date:
        response = input(message)
        response_is_not_slashed = True
        response_is_not_int = True
        response_is_not_yyyy = True
        date = response.split("/")
        if len(date) == len(DATE_FORMAT):
            response_is_not_slashed = False
            try:
                day = int(date[0])
                month = int(date[1])
                if len(date[2]) == 4:
                    response_is_not_yyyy = False
                    year = int(date[2])
                else:
                    message = "Erreur de format, veuiller écrire la date en respectant le format: jj/mm/aaaa: "
                response_is_not_int = False
            except ValueError:
                response_is_not_int = True
                message = "Erreur de format, veuiller écrire la date en respectant le format: jj/mm/aaaa: "
        else:
            message = "Erreur de format, veuiller écrire la date en respectant le format: jj/mm/aaaa: "
        response_is_not_date = response_is_not_int or response_is_not_slashed or response_is_not_yyyy
    return datetime.date(year, month, day)


def input_actor():
    """
    Demande les informations d'un joueur afin de
     les regrouper dans son instance acteur
    :return: instance d'acteur
    """
    last_name = prompt_string("Votre nom de famille : ")
    first_name = prompt_string("Votre prénom : ")
    birthdate = prompt_date("Votre date de naissance en respectant le format: jj/mm/aaaa: ")
    gender = prompt_propositions({"F": "Féminin", "M": "Masculin"})
    rank = prompt_number("Votre classement HATP: ", min=0)
    acteur = Actor(last_name, first_name, birthdate, gender, rank)
    return acteur


def tournament_inputs():
    """
    Recueil les informations nécessaires à la création d'un tournoi
    :return: instance de tournoi avec les informations
    """
    name = prompt_string("Nom du tournoi : ")
    location = prompt_string("Lieu du tournoi : ")
    date = datetime.date.today()
    timer = prompt_propositions({"Bu": "Bullet", "Bz": "Blitz", "Cr": "Coup rapide"})
    description = prompt_string("description: ")
    tournoi = Tournament(name, location, date, timer, description)
    return tournoi


def define_tournament_player(tournament, num_player):
    """
    Définit les joueurs d'un tournoi en demandant leur identifiant
    :return: instance de l'acteur
    """
    actor_id = prompt_id_num(f"Veuillez indiquer l'identifiant du joueur {num_player}: ")
    while actor_id not in Actors:  ######
        actor_id = prompt_id_num(f"Identifiant inconnu. Veuillez réessayer l'identifiant du {num_player}: ")
    tournament.list_of_players.append(Actor[actor_id])


if __name__ == "__main__":
    Me = input_actor()
    print(Me)
    You = input_actor()
    print(You)
