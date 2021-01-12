from chess.utils.conversion import str_into_date


DATE_FORMAT = ["day", "month", "year"]
ID_WIDTH = 8
NB_MATCH = 4


def prompt_number(message, mini=None, maxi=None):
    """
    Demande à l'utilisateur à l'aide de
    message de saisir un entier.

    Si l'utilisateur fournit un objet qui n'est
    pas un entier, ou un entier qui n'est pas
    entre le min et le max (compris),
    alors la question est reposée.
    :param message:
    :param mini:
    :param maxi:
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
        proposal_message += f"soit: {cle} pour {item}.\n"
    message = "Choisissez parmi: \n" + proposal_message
    error_message = "Votre réponse ne correspond pas. \n" \
                    "Veuillez indiquer : \n"
    error_message += proposal_message
    response = input(message)
    while response not in propositions:
        response = input(error_message)
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
    """
    Demande les informations d'un joueur afin de
     les regrouper dans son instance acteur
    :return: acteur arguments
    """
    last_name = prompt_string("Votre nom de famille : ")
    first_name = prompt_string("Votre prénom : ")
    birthdate = prompt_date("Votre date de naissance "
                            "en respectant le format: jj/mm/aaaa: ")
    gender = prompt_propositions({"F": "Féminin", "M": "Masculin"})
    rank = prompt_number("Votre classement HATP: ", mini=0)
    acteur_arguments = [last_name, first_name, birthdate, gender, rank]
    return acteur_arguments


def input_tournament_players(message):
    actor_id = prompt_id_num(message)
    return actor_id


def tournament_inputs():
    """
    Recueil les informations nécessaires à la création d'un tournoi
    :return: the associated tournament arguments
    """
    name = prompt_string("Nom du tournoi : ")
    location = prompt_string("Lieu du tournoi : ")
    timer = prompt_propositions({"Bu": "Bullet",
                                 "Bz": "Blitz",
                                 "Cr": "Coup rapide"})
    description = prompt_string("description: ")
    tournament_arguments = [name, location, timer, description]
    return tournament_arguments


def input_match_results(r0und):
    """
    Demande à remplir les résultat d'un tour
    On commence par choisir un match en désignant son numéro
    puis on indique un vainqueur ou un match nul
    :param r0und: le tour en question
    :return: la liste des résultats des 4 matchs
    Exemple {0,1,1,2}, match nul pour le premier match
    Le premier joueur désigné est vainqueur pour les matchs 2 et 3.
    Le second joueur désigné est vainqueur pour le match 4.
    """
    print("En attente de résultats: \n"
          "Lorsqu'un match est terminé, "
          "indiquez le numéro du match "
          "pour entrez les résultats")
    remaining_matchs = {"1": "Match 1", "2":
                        "Match 2", "3": "Match 3", "4": "Match 4"}
    results = [0]*NB_MATCH
    while remaining_matchs != {}:
        num_match = int(prompt_propositions(remaining_matchs))
        print(r0und.matchs[num_match])
        result = prompt_number("Indiquer le vainqueur"
                               " par 1 ou 2, ou inscrivez 0"
                               " pour le match nul", 0, 2)
        results[num_match] = result
        del remaining_matchs[str(num_match)]
    return results


if __name__ == "__main__":
    """    Me = input_actor()
    print(Me)
    You = input_actor()
    print(You)"""

    prompt_propositions({"U": "Unique", "D": "Débile", "T": "Terrible"})
