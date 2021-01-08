from tinydb import TinyDB


db_actors = TinyDB('db_actors.json')
actors_table = db_actors.table("actors")
actors_table.truncate()	# clear the table first


class ExportActors:
    """

    """
    def __init__(self, actors):
        self.actors = actors

    def serialize_actors(self):
        serialized_actors = []
        for actor in self.actors:
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


db_tournament = TinyDB('db_tournament')
tournament_table = db_tournament.table("tournament")
tournament_table.truncate()	# clear the table first


class ExportTournament:
    """

    """
    def __init__(self, tournament):
        self.tournament = tournament

    def serialize_tournament(self):
        serialized_tournament = {
            'tournament_id': self.tournament.tournament_id,
            'name': self.tournament.name,
            'location': self.tournament.location,
            'start_date': self.tournament.start_date,
            'end_date': self.tournament.end_date,
            'timer_type': self.tournament.timer_type,
            'description': self.tournament.description,
            'number_of_rounds': self.tournament.number_of_rounds,
            'rounds': self.tournament.rounds,
            'list_of_players': self.tournament.list_of_players,
            'players_assigned': self.tournament.players_assigned
        }
        tournament_table.insert(serialized_tournament)
