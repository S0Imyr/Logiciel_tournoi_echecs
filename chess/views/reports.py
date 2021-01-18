from operator import attrgetter


def players_table(actors_list):
    for actor in actors_list:
        name_characters = len(actor.last_name)+len(actor.first_name)
        rank_characters = len(str(actor.rank))
        print(f"{actor.last_name} {actor.first_name}"
              + " " * (30 - name_characters) +
              f"Classement : rank {actor.rank}"
              + " " * (10 - rank_characters) +
              f"Tournoi joués : {len(actor.tournaments)}")


def tournaments_table(tournaments_list):
    for tournament in tournaments_list:
        id_characters = len(tournament.tournament_id)
        #dates_characters = len(tournament.start_date)+len(tournament.end_date)
        print(f"Tournoi: {tournament.tournament_id}"
              + " " * (10 - id_characters) +
              f"Du: {tournament.start_date} au: {tournament.end_date}")


def report_actors_by_alpha(actors_list):
    sorted_actors = sorted(actors_list, key=attrgetter("first_name"))
    sorted_actors = sorted(sorted_actors, key=attrgetter("last_name"))
    players_table(sorted_actors)


def report_actors_by_rank(actors_list):
    sorted_actors = sorted(actors_list, key=attrgetter("rank"))
    players_table(sorted_actors)


def report_tournaments_list():
    pass


def report_tournament_players():
    pass


def report_tournament_matchs():
    pass


def report_tournament_rounds():
    pass


def report_no_tournament():
    print("Il n'y a pas de tournoi avec cet identifiant"
          " dans la base de données")