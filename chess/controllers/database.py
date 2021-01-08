from chess.models.actors import Actor
from chess.models.game import Tournament
from tinydb import TinyDB


db_actors = TinyDB('db_actors.json')
actors_table = db_actors.table("actors")
actors_table.truncate()	# clear the table first


def serialize_actors(actors):
    serialized_actors = []
    for actor in actors:
        serialized_actor = {
            'actor_id': actor.actor_id,
            'last_name': actor.last_name,
            'first_name': actor.first_name,
            'birthdate': actor.birthdate,
            'gender': actor.gender,
            'rank': actor.rank,
            'tournaments': actor.tournaments
        }
        serialized_actors.append(serialized_actor)
    actors_table.insert_multiple(serialized_actors)


def import_actors():
    serialized_actors = actors_table.all()
    for actor in serialized_actors:
        actor_id = actor['actor_id']
        last_name = actor['last_name']
        first_name = actor['first_name']
        birthdate = actor['birthdate']
        gender = actor['gender']
        rank = actor['rank']
        tournaments = actor['tournaments']
        actor = Actor(last_name, first_name, birthdate, gender, rank)
        actor.actor_id = actor_id
        actor.tournaments = tournaments
    return len(serialized_actors)


db_tournament = TinyDB('db_tournament')
tournament_table = db_tournament.table("tournament")
tournament_table.truncate()	# clear the table first


def serialize_tournament(tournament):
    serialized_tournament = {
        'tournament_id': tournament.tournament_id,
        'name': tournament.name,
        'location': tournament.location,
        'start_date': tournament.start_date,
        'end_date': tournament.end_date,
        'timer_type': tournament.timer_type,
        'description': tournament.description,
        'number_of_rounds': tournament.number_of_rounds,
        'rounds': tournament.rounds,
        'list_of_players': tournament.list_of_players,
        'players_assigned': tournament.players_assigned
    }
    tournament_table.insert(serialized_tournament)
