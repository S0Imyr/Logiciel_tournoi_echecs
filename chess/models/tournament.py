# -*- coding: utf-8 -*-


"""
Handles the tournament logic
"""


import datetime

from chess.utils.utils import get_new_id

from chess.models.actors import Player
from chess.models.round import Round


TOURNAMENT_ID_WIDTH = 8
NB_ROUND = 4
NB_PLAYERS = 8
NB_MATCH = 4


class Tournament:
    """ The class Tournament is the central piece of the models. """
    last_tournament_id = "0" * TOURNAMENT_ID_WIDTH

    def __init__(self, name, location, timer_type, description):
        Tournament.last_tournament_id = get_new_id(Tournament.last_tournament_id, TOURNAMENT_ID_WIDTH)
        self.tournament_id = Tournament.last_tournament_id
        self.name = name
        self.location = location
        self.start_date = None
        self.end_date = None
        self.timer_type = timer_type
        self.description = description
        self.number_of_rounds = NB_ROUND
        self.rounds = []
        self.list_of_players = []
        self.players_assigned = False
        self.finished = False

    def define_players(self, actors):
        """ Defines the list of identifier of the players who join the tournament.

        :param actors:
        :return: None
        """
        for num_player in range(NB_PLAYERS):
            self.list_of_players.append(Player(actors[num_player],
                                               self.tournament_id,
                                               num_player))

    def init_round(self, num_round):
        """ Launches the round number "num_round".

        :param num_round: number of the round played
        :return: None
        """
        tour = Round(num_round, self.tournament_id, self.list_of_players)
        tour.start_date = datetime.date.today()
        tour.rank_players()
        tour.define_matches()
        self.rounds.append(tour)

    def register_round_results(self, num_round, winner):
        """ Registers the results of the round.

        :param num_round: the round number.
        :param winner: the list of the winners.
        :return: None.

        """
        self.rounds[num_round].register_results(winner)
        self.rounds[num_round].assign_points()
        self.rounds[num_round].finished = True
        self.rounds[num_round].memorize_opponents()
        self.rounds[num_round].rank_players()
        self.rounds[num_round].end_date = datetime.date.today()

    def tournament_to_dict(self):
        """ Converts the tournament into a dictionary

        :return: dictionary of the tournament instance.

        """
        string_attributes = ['tournament_id',
                             'name',
                             'location',
                             'timer_type',
                             'description',
                             'number_of_rounds',
                             'players_assigned']
        serialized_tournament = {}
        for attribute in string_attributes:
            serialized_tournament[attribute] = getattr(self, attribute)
        serialized_tournament['rounds'] = []
        for r0und in self.rounds:
            serialized_tournament['rounds'].append(r0und.round_to_dict())
        serialized_tournament['list_of_players'] = []
        for player in self.list_of_players:
            serialized_tournament['list_of_players'].append(player.player_to_dict())
        serialized_tournament['start_date'] = str(self.start_date)
        serialized_tournament['end_date'] = str(self.end_date)
        return serialized_tournament

    def end_tournament(self):
        """ Handles the end of the tournament.

        Adds the tournament_id to the players list of tournaments.
        Defines the attribute finished and the end date of the tournament.

        """
        for player in self.list_of_players:
            player.actor.list_of_tournaments_played.append(self.tournament_id)
        self.finished = True
        self.end_date = datetime.date.today()
