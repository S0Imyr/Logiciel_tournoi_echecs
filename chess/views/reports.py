from operator import attrgetter


def players_table(actors_list):
    for actor in actors_list:
        name_characters = len(actor.last_name)+len(actor.first_name)
        rank_characters = len(str(actor.rank))
        print(f"{actor.last_name} {actor.first_name}"
              + " " * (30 - name_characters) +
              f"Classement : rank {actor.rank}"
              + " " * (10 - rank_characters) +
              f"Tournoi joués : {len(actor.list_of_tournaments_played)}")


def report_actors_by_alpha(actors_list):
    sorted_actors = sorted(actors_list, key=attrgetter("first_name"))
    sorted_actors = sorted(sorted_actors, key=attrgetter("last_name"))
    players_table(sorted_actors)


def report_actors_by_rank(actors_list):
    sorted_actors = sorted(actors_list, key=attrgetter("rank"))
    players_table(sorted_actors)


def report_tournaments_list(tournaments_list):
    for tournament in tournaments_list:
        id_characters = len(tournament.tournament_id)
        name_characters = len(tournament.name)
        # dates_characters = len(tournament.start_date)+len(tournament.end_date)
        print(f"{tournament.tournament_id}"
              + " " * (10 - id_characters) +
              f"Tournoi : {tournament.name}"
              + " " * (20 - name_characters) +
              f"Du: {tournament.start_date} au: {tournament.end_date}")


def report_tournament_players(tournament, sort):
    actors_list = []
    for player in tournament.list_of_players:
        actors_list.append(player.actor)
    if sort == "Alphabetical":
        report_actors_by_alpha(actors_list)
    elif sort == "By rank":
        report_actors_by_rank(actors_list)


def report_tournament_matchs(tournament):
    print(f"### Tournoi: {tournament.name} ###")
    for r0und in tournament.rounds:
        print(f"Les matchs du tour {r0und.round_nb}: \n")
        for match in r0und.matchs.values():
            print(str(match))


def report_tournament_rounds(tournament):
    print(f"### Tournoi: {tournament.name} ###")
    for r0und in tournament.rounds:
        print(str(r0und))


def report_no_tournament():
    print("Il n'y a pas de tournoi avec cet identifiant"
          " dans la base de données")
