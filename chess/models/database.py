from tinydb import TinyDB, Query

from chess.models.actors import Actor, Player
from chess.models.match import Match
from chess.models.round import Round
from chess.models.game import Tournament

from chess.utils.conversion import str_to_date, \
    str_space_to_list, str_space_to_int_list

from chess.utils.utils import get_last_id


ID_WIDTH = 8


def deserialize_actor(serialized_actor):
    """
    Transforms a dictionary containing the values of an actor instance
     into the corresponding actor instance.
    :param serialized_actor: structured dictionary.
    :return: instance of actor.
    """
    actor = Actor(serialized_actor['last_name'],
                  serialized_actor['first_name'],
                  str_to_date(serialized_actor['birthdate']),
                  serialized_actor['gender'],
                  serialized_actor['rank'])
    actor.actor_id = serialized_actor['actor_id']
    actor.list_of_tournaments_played = str_space_to_list(serialized_actor['tournaments'])
    return actor


def deserialize_player(serialized_player):
    """
    Transforms a dictionary containing the values of a player instance
     into the corresponding player instance.
    :param serialized_player: structured dictionary.
    :return: instance of player.
    """
    actor = deserialize_actor(serialized_player['actor'])
    player = Player(actor,
                    serialized_player['tournament_ID'],
                    serialized_player['player_id'])
    string_attribute = ['name', 'rank', 'ranking', 'points', 'place']
    for key in string_attribute:
        setattr(player, key, serialized_player[key])
    player.opponents = str_space_to_int_list(serialized_player['opponents'])
    return player


def deserialize_match(serialized_match):
    """
    Transforms a dictionary containing the values of a match instance
     into the corresponding match instance.
    :param serialized_match: structured dictionary.
    :return: instance of match.
    """
    match = Match(serialized_match['match_nb'],
                  serialized_match['round_nb'],
                  serialized_match['tournament_ID'])
    player1 = deserialize_player(serialized_match['player1'])
    setattr(match, 'player1', player1)
    player2 = deserialize_player(serialized_match['player2'])
    setattr(match, 'player2', player2)
    string_attribute = ['winner', 'finished', 'points_assigned']
    for attribute in string_attribute:
        setattr(match, attribute, serialized_match[attribute])
    return match


def deserialize_round(serialized_round):
    """
    Transforms a dictionary containing the values of a round instance
     into the corresponding round instance.
    :param serialized_round: structured dictionary.
    :return: instance of round.
    """
    deserialized_players = []
    for player in serialized_round['players']:
        deserialized_players.append(deserialize_player(player))
    r0und = Round(serialized_round['round_nb'],
                  serialized_round['tournament_ID'],
                  deserialized_players)

    string_attribute = ['players_ranked', 'finished', 'players_sorted']
    for attribute in string_attribute:
        setattr(r0und, attribute, serialized_round[attribute])

    matchs = {}
    for match_nb, match in serialized_round['matchs'].items():
        matchs[int(match_nb)] = deserialize_match(match)
    setattr(r0und, 'matchs', matchs)
    return r0und


def deserialize_tournament(serialized_tournament):
    """
    Transforms a dictionary containing the values of a tournament instance
     into the corresponding tournament instance.
    :param serialized_tournament: structured dictionary.
    :return: instance of tournament.
    """
    tour = Tournament(serialized_tournament['name'],
                      serialized_tournament['location'],
                      serialized_tournament['timer_type'],
                      serialized_tournament['description'])
    string_attributes = ['tournament_id',
                         'number_of_rounds',
                         'players_assigned']
    for attribute in string_attributes:
        setattr(tour, attribute, serialized_tournament[attribute])

    tour.start_date = str_to_date(serialized_tournament['start_date'])
    tour.end_date = str_to_date(serialized_tournament['end_date'])

    tour.rounds = []
    for r0und in serialized_tournament['rounds']:
        tour.rounds.append(deserialize_round(r0und))
    tour.list_of_players = []
    for player in serialized_tournament['list_of_players']:
        tour.list_of_players.append(deserialize_player(player))
    return tour


class DataBaseHandler:
    def __init__(self):
        self.database = TinyDB('db.json')

    def export_actor(self, actor):
        """
        Transfers an instance of actor in a table of the database
        the instance of actor is transformed in a dictionary first.
        :param actor: instance of actor
        :return: None
        """
        actors_table = self.database.table('actors')
        query = Query()
        dictio = actor.actor_to_dict()
        if actors_table.search(query.actor_id == actor.actor_id):
            actors_table.update(dictio, query.actor_id == actor.actor_id)
        else:
            actors_table.insert(dictio)

    def import_actor(self, identifier):
        actors = self.database.table('actors')
        query = Query()
        if actors.search(query.actor_id == identifier):
            actor_dict = actors.search(query.actor_id == identifier)[0]
            actor = deserialize_actor(actor_dict)
        else:
            actor = {}
        return actor

    def import_actors(self):
        """
        Imports a list of actors instances transformed in a dictionnary,
        the dictionary is converted in the list of the corresponding
        instances of actors.
        :return: the number of actors imported and
         the list of actors instances
        """
        actors_table = self.database.table('actors')
        serialized_actors = actors_table.all()
        actors = []
        for value in serialized_actors:
            actor = deserialize_actor(value)
            actors.append(actor)
        return len(serialized_actors), actors

    def export_interrupted_tournament(self, tournament):
        """
        Transfers an instance of tournament in a table of the database,
        the instance of tournament is transformed in a dictionary first.
        :param tournament: instance of tournament
        :return: None
        """
        tournament_table = self.database.table('interrupted_tournament')
        tournament_table.truncate()
        dictio = tournament.tournament_to_dict()
        tournament_table.insert(dictio)

    def import_interrupted_tournament(self):
        """
        Imports a list of one tournament transformed in a dictionary,
        it is converted in  the corresponding instance of tournament.
        :return: the instance of tournament.
        """
        tournament_table = self.database.table('interrupted_tournament')
        list_serialized_tournament = tournament_table.all()
        if not list_serialized_tournament:
            return []
        serialized_tournament = list_serialized_tournament[0]
        tournament = deserialize_tournament(serialized_tournament)
        return tournament

    def export_tournament(self, tournament):
        """
        Transfers an instance of tournament in a table of the database,
        the instance of tournament is transformed in a dictionnary first.
        :param tournament: instance of tournament
        :return: None
        """
        tournaments_table = self.database.table('tournament')
        dictio = tournament.tournament_to_dict()
        query = Query()
        if tournaments_table.search(query.tournament_id == tournament.tournament_id):
            tournaments_table.update(dictio, query.tournament_id == tournament.tournament_id)
        else:
            tournaments_table.insert(dictio)

    def export_finished_tournament(self, tournament):
        """
        Exports actor instances of players and the tournament when finished
        :param tournament: the finihed tournament, ready to be exported
        :return: None
        """
        self.export_tournament(tournament)
        for player in tournament.list_of_players:
            self.export_actor(player.actor)

    def find_tournament_by_id(self, identifier):
        """
        Finds the tournament in the database by entering its identifier
        :param identifier: the identifier of the searched tournament
        :return: instance of the tournament searched
        """
        tournaments = self.database.table('tournament')
        query = Query()
        if tournaments.search(query.tournament_id == identifier):
            tournament_dict = tournaments.search(query.tournament_id == identifier)[0]
            tournament = deserialize_tournament(tournament_dict)
        else:
            tournament = {}
        return tournament

    def export_last_tournament_id(self):
        list_of_id = []
        for tournament in self.database.table('tournament').all():
            for key, value in tournament.items():
                if key == "tournament_id":
                    list_of_id.append(value)
        last_id = get_last_id(list_of_id, ID_WIDTH)
        return last_id

    def import_tournaments(self):
        """
        Imports a list of tournaments instances from the database
        :return: list of tournaments instances
        """
        tournaments_table = self.database.table('tournament')
        serialized_tournaments = tournaments_table.all()
        tournaments = []
        for value in serialized_tournaments:
            tournament = deserialize_tournament(value)
            tournaments.append(tournament)
        return tournaments
