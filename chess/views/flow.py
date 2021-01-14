NB_MATCH = 4


def view_intro_home_menu():
    print("\n ### Menu Principal ### \n"
          "\n"
          "-- Que souhaitez vous réaliser ? --\n"
          "\n"
          "Si des joueurs doivent être importés, commencer par cela.")


def view_tournament_creation():
    print("\n ### Création du tournoi ### \n"
          "\n"
          "-- Débutons par les informations du tournoi : --\n")


def view_tournament_players(tournament):
    print(f"\n ### Tournoi {tournament.name}: Type d'entrée des joueurs ### \n"
          "\n"
          
          "-- Attention --\n"
          
          "pour ajouter des joueurs, "
          "vous devez les avoir enregistrer "
          "depuis le menu principal, \n"
          "puis donner l'identifiant au joueur "
          "pour qu'il le redonne au lancement du tournoi.\n")


def view_input_new_actor():
    display = "\n ### Nouveau joueur ### \n"
    display += "\n -- Entrez les informations demandées: --\n"
    print(display)


def view_validation_new_actor(actor):
    print(f"\n ### Le joueur suivant a bien été enregistré ### \n")
    print(actor)


def view_id_player(tournament, num=1):
    print(f"\n ### Tournoi {tournament.name}: Identification de joueur ### \n")
    print(f"-- Joueur {num} --")


def view_validation_players(players):
    print(f"-- Les joueurs du tournoi sont : --")
    message = ""
    for player in players:
        message += "\n" + str(player)
    print(message)


def view_launch_tournament(tournament):
    print(f"\n ### Lancement du Tournoi {tournament.name}: ### ")


def view_round_matchs(r0und):
    display = f"\n ### Matchs du Tour {r0und.round_nb + 1} " \
              f"du Tournoi {r0und.tournament_id} : ### \n \n"
    if r0und.matchs != {}:
        if r0und.finished:
            display += f"Les matchs ont vu s'affronter : \n"
        else:
            display += f"Les matchs verront s'affronter : \n"
        for num_match in range(NB_MATCH):
            display += f"{num_match + 1}. " \
                       f"{r0und.matchs[num_match].player1.name}" \
                       f" et {r0und.matchs[num_match].player2.name} \n"
            if r0und.finished:
                if r0und.matchs[num_match].winner == 0:
                    display += f"Match nul. \n"
                if r0und.matchs[num_match].winner == 1:
                    display += f"Victoire de " \
                               f"{r0und.matchs[num_match].player1.name}. \n"
                if r0und.matchs[num_match].winner == 2:
                    display += f"Victoire de " \
                               f"{r0und.matchs[num_match].player2.name}. \n"
    print(display)


def input_match_results():
    print("### En attente de résultats: ### \n"
          "\n"
          "Lorsqu'un match est terminé, "
          "indiquez le numéro du match "
          "pour entrez les résultats")


def view_tournament_final(tournament):
    message = " ### Fin des matchs ### \n" \
              "\n" \
              "-- Classement final -- \n"
    for player in tournament.list_of_players:
        if player.place == 1:
            message += f"1er: +{player}"
        else:
            for rank in range(2, len(tournament.list_of_players)):
                message += f"{rank}eme: +{player}"
    print(message)


def view_validation_actors_imported(actors):
    print(f"\n ### Import de joueurs ### \n")
    if len(actors) == 0:
        message = "Base de donnée vide, aucun import possible"
    else:
        message = f"-- {len(actors)} joueurs importés --"
    print(message)
    for actor in actors:
        print(actor)


def view_validation_actors_exported(exported_actors):
    message = "Les personnes suivantes ont été exportés \n"
    for actor in exported_actors:
        message += "\n" + actor
    print(message)


def view_import_no_tournament():
    print(" ---------------------------------- "
          "\n --- Aucun tournoi sauvegardé ! --- "
          "\n ---------------------------------- ")
