

def view_intro_home_menu():
    print("\n ### Menu Principal ### \n"
          "\n"
          "-- Que souhaitez vous réaliser ? --\n")


def view_tournament_creation():
    print("\n ### Création du tournoi ### \n"
          "\n"
          "-- Débutons par les informations du tournoi : --\n")


def view_tournament_players(tournament):
    print(f"\n ### Tournoi {tournament}: Type d'entrée des joueurs ### \n"
          "\n"
          "-- Maintenant comment voulez vous entrer un joueur ? --\n")


def view_new_player(tournament=None):
    message = ""
    if tournament:
        message += f"\n ### Tournoi {tournament}: Nouveau joueur ### \n "
    else:
        message += "Nouveau joueur"
    message += "\n -- Entrez les informations demandées: --\n"
    print(message)


def view_validation_new_player(actor):
    print(f"\n ### Le joueur a bien été enregistré ### \n"
          "\n")
    print(actor)


def view_id_player(tournament, num=1,):
    print(f"\n ### Tournoi {tournament}: Identification de joueur ### \n"
          "\n")
    print(f"-- Joueur {num}--")
