NB_MATCH = 4


def view_intro_home_menu():
    print("\n ### Menu Principal ### \n"
          "\n"
          "-- Que souhaitez vous réaliser ? --\n")


def view_actors_menu():
    print("\n ### Attention ### \n"
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
    view = "\n ### Nouveau joueur ### \n"
    view += "\n -- Entrez les informations demandées: --\n"
    print(view)


def view_validation_new_actor(actor):
    print(f"\n ### Le joueur suivant a bien été enregistré ### \n")
    print(actor)


def view_id_player(tournament, num=1):
    print(f"\n ### Tournoi {tournament.name}: Identification de joueur ### \n")
    print(f"-- Joueur {num} --")


def view_validation_players(players):
    print(f"\n -- Les joueurs du tournoi sont : --")
    view = ""
    for player in players:
        view += "\n" + str(player)
    print(view)


def view_launch_tournament(tournament):
    print(f"\n ### Lancement du Tournoi {tournament.name}: ### ")


def view_round_matchs(r0und):
    view = f"\n ### Matchs du Tour {r0und.round_nb + 1} " \
              f"du Tournoi {r0und.tournament_ID} : ### \n \n"
    if r0und.matchs != {}:
        if r0und.finished:
            view += f"Les matchs ont vu s'affronter : \n"
        else:
            view += f"Les matchs verront s'affronter : \n"
        for num_match in range(NB_MATCH):
            view += f"{num_match + 1}. " \
                       f"{r0und.matchs[num_match].player1.name}" \
                       f" et {r0und.matchs[num_match].player2.name} \n"
            if r0und.finished:
                if r0und.matchs[num_match].winner == 0:
                    view += f"Match nul. \n"
                if r0und.matchs[num_match].winner == 1:
                    view += f"Victoire de " \
                               f"{r0und.matchs[num_match].player1.name}. \n"
                if r0und.matchs[num_match].winner == 2:
                    view += f"Victoire de " \
                               f"{r0und.matchs[num_match].player2.name}. \n"
    print(view)


def view_players_rank(list_of_players):
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
    print("\n ### En attente de résultats: ### \n"
          "\n"
          "Lorsqu'un match est terminé, "
          "indiquez le numéro du match "
          "pour entrez les résultats")


def view_tournament_final(tournament):
    print("\n ### Fin des matchs ### \n"
          "\n"
          "-- Classement final -- \n")
    view_players_rank(tournament.list_of_players)


def view_validation_actors_imported(actors):
    print(f"\n ### Import de joueurs ### \n")
    if len(actors) == 0:
        view = "Base de donnée vide, aucun import possible"
    else:
        view = f"-- {len(actors)} joueurs importés --"
    print(view)
    for actor in actors:
        print(actor)


def view_validation_actors_exported(exported_actors):
    view = f"\n Les {len(exported_actors)} personnes ont été exportés \n"
    for actor in exported_actors:
        view += "\n" + actor.actor_id + " " + actor.first_name + " " + actor.last_name
    print(view)


def view_import_no_tournament():
    print("\n ---------------------------------- "
          "\n --- Aucun tournoi sauvegardé ! --- "
          "\n ---------------------------------- ")


def view_tournament_reports(tournament):
    print(f"\n ### Rapports du tournoi {tournament.name}. ###"
          f"\n Identifiant du tournoi: {tournament.tournament_id} \n")
