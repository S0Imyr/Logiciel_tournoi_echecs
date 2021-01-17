from operator import attrgetter


def report_actors_by_alpha(actorslist):
    sorted_actors = sorted(actorslist, key=attrgetter("first_name"))
    sorted_actors = sorted(sorted_actors, key=attrgetter("last_name"))
    for actor in sorted_actors:
        print(f"{actor.last_name} {actor.first_name}: "
              f"Nombre de tournoi joués : {len(actor.tournaments)}")


def report_actors_by_rank():
    pass


def report_tournaments_list():
    pass


def report_tournament_players():
    pass


def report_tournament_matchs():
    pass


def report_tournament_rounds():
    pass
