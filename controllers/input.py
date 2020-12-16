def prompt_number(message, min=None, max=None):
    """Demande à l'utilisateur à l'aide de
    message de saisir un entier.

    Si l'utilisateur fournit un objet qui n'est
    pas un entier, ou un entier qui n'est pas
    entre le min et le max (non compris),
    alors la question est reposée.
    """

    response = input(message)
    response_is_not_number = True
    while response_is_not_number:
        try:
            response = int(response)
            response_is_not_number = False
        except ValueError:
            response = input("Entrée incorrecte, veuillez entrer un nombre : ")
            continue

    max_is_not_number = True
    while max_is_not_number:
        try:
            max = int(max)
            max_is_not_number = False
        except ValueError:
            print("Entrée incorrecte, veuillez entrer un maximum qui est un nombre : ")
            continue
    min_is_not_number = True
    while min_is_not_number:
        try:
            min = int(min)
            min_is_not_number = False
        except ValueError:
            print("Entrée incorrecte, veuillez entrer un maximum qui est un nombre : ")
            continue

    while not (int(response) >= min and int(response) <= max):
        response = input(f"Nombre incorrect, veuillez entrer un entier entre {min} et {max} : ")
    return int(response)


def prompt_string(message):
    """Demande à l'utilisateur à l'aide de
    message de saisir une chaine de caractère.
    """

def prompt_date(message):
    """Demande à l'utilisateur à l'aide de
    message de saisir une date
    """