from chess.models.actors import Actor
from chess.models.game import Tournament
from chess.utils.conversion import str_into_date
from tinydb import TinyDB
from chess.views.flow import validation_export


class DataBaseHandler:
    def __init__(self, db):
        self.db = db
        self.players_table = db.table
        self.tournament_table = db.tournament
        self.tournament_step = None

    def export_actor(self, actor):
        dictio = actor.actor_to_dict()
        self.players_table.insert(dictio)
        chess.views.flow.validation_export(actor)

    def export_tournament(self, tournament, step):
        dictio = tournament.tournament_to_dict(step)
        self.tournament_table.insert(dictio)
        self.tournament_step = step
        chess.views.flow.validation_export(tournament)

    def import_actor(self, json):
        pass

    def import_tournament(self):
        pass


if __name__ == '__main__':
    pass
