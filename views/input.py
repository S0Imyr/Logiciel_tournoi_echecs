import datetime


DATE_FORMAT = ["day", "month", "year"]


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


def prompt_yes_or_no(message):
    """Demande à l'utilisateur à l'aide de
    message de saisir O pour oui ou N pour non.
    """
    pass

def prompt_string(message):
    """Demande à l'utilisateur à l'aide de
    message de saisir une chaine de caractère.
    """
    pass

def prompt_date(message):
    """Demande à l'utilisateur à l'aide de
    message de saisir une date
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
            try :
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
    return datetime.date(year,month,day)

if __name__ == "__main__":
    date = prompt_date("Entrer votre date de naissance: ")
    print(date)