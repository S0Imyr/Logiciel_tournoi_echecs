NB_MATCH = 4


def view_intro_home_menu():
    print("\n ### Menu Principal ### \n"
          "\n"
          "-- Que souhaitez vous réaliser ? --\n")


def view_tournament_creation():
    print("\n ### Création du tournoi ### \n"
          "\n"
          "-- Débutons par les informations du tournoi : --\n")


def view_tournament_players(tournament):
    print(f"\n ### Tournoi {tournament.name}: Type d'entrée des joueurs ### \n"
          "\n"
          "-- Maintenant comment voulez vous entrer un joueur ? --\n")


def view_new_player(tournament=None):
    display = ""
    if tournament:
        display += f"\n ### Tournoi {tournament.name}: Nouveau joueur ### \n "
    else:
        display += "Nouveau joueur"
    display += "\n -- Entrez les informations demandées: --\n"
    print(display)


def view_validation_new_player(actor):
    print(f"\n ### Le joueur suivant a bien été enregistré ### \n")
    print(actor)


def view_id_player(tournament, num=1,):
    print(f"\n ### Tournoi {tournament.name}: Identification de joueur ### \n")
    print(f"-- Joueur {num}--")


def view_launch_tournament(tournament):
    print(f"\n ### Lancement du Tournoi {tournament.name}: ### \n"
          "\n")


def view_round_matchs(round):
    display = f"\n ### Matchs du Tour {round.round_nb} " \
              f"du Tournoi {round.tournament_id} : ### \n"
    if round.matchs != {}:
        if round.finished:
            display += f"Les matchs ont vu s'affronter : \n"
        else:
            display += f"Les matchs verront s'affronter : \n"
        for num_match in range(NB_MATCH):
            display += f"{num_match + 1}. " \
                       f"{round.matchs[num_match].player1.name}" \
                       f" et {round.matchs[num_match].player2.name} \n"
            if round.finished:
                if round.matchs[num_match].winner == 0:
                    display += f"Match nul. \n"
                if round.matchs[num_match].winner == 1:
                    display += f"Victoire de " \
                               f"{round.matchs[num_match].player1.name}. \n"
                if round.matchs[num_match].winner == 2:
                    display += f"Victoire de " \
                               f"{round.matchs[num_match].player2.name}. \n"
    print(display)
