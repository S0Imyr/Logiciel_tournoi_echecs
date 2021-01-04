import datetime
from chess.models.actors import Actor

DATE_FORMAT = ["day", "month", "year"]


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


def prompt_gender(message):
    """
    Demande à l'utilisateur de spécifier un genre.
    Si la réponse n'est pas M ou F, la demande
    est refaite.
    :param message:
    :return: input
    """
    response = input(message)
    while response != "M" and response != "F":
        input("Votre réponse ne correspond pas. \n"
              "Veuillez indiquer 'F' pour Féminin "
              "ou 'M' pour Masculin :")
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
    print("Inscription d'un joueur: \n")
    print("Renseigner les informations suivantes: \n")
    last_name = prompt_string("Votre nom de famille : ")
    first_name = prompt_string("Votre prénom : ")
    birthdate = prompt_date("Votre date de naissance en respectant le format: jj/mm/aaaa: ")
    gender = prompt_gender("Votre genre en écrivant F pour féminin ou M pour Masculin: ")
    rank = prompt_number("Votre classement HATP: ", min=0)
    acteur = Actor(last_name, first_name, birthdate, gender, rank)
    return acteur

if __name__ == "__main__":
    Me = input_actor()
    print(Me)
    You = input_actor()
    print(You)
