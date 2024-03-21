# -*- coding: utf-8 -*-


"""
This module handle the round logic.
"""


from operator import attrgetter
from chess.models.match import Match


NB_PLAYERS = 8
NB_MATCH = 4
MATCH_1ST_ROUND = [[1, 5], [2, 6], [3, 7], [4, 8]]
MATCH_OTHER_ROUND = [[1, 2], [3, 4], [5, 6], [7, 8]]


class Round:
    """ A round is a set in a tournament. """
    def __init__(self, round_nb, tournament_id, players):
        self.round_nb = round_nb
        self.name = f"Round {round_nb + 1}"
        self.tournament_ID = tournament_id
        self.players = players
        self.start_date = None
        self.end_date = None
        self.players_ranked = False
        self.matches = {}
        self.finished = False
        self.players_sorted = False

    def __str__(self):
        message = f"Tour {self.round_nb + 1} du tournoi {self.tournament_ID} \n"
        if self.matches != {}:
            if self.finished:
                message += "Les matchs ont vu s'affronter : \n"
            else:
                message += "Les matchs verront s'affronter : \n"
            for num_match in range(NB_MATCH):
                message += f"{num_match+1}. " \
                           f"{self.matches[num_match].player1.name}" \
                           f" et {self.matches[num_match].player2.name} \n"
                if self.finished:
                    if self.matches[num_match].winner == 0:
                        message += "Match nul. \n"
                    if self.matches[num_match].winner == 1:
                        message += f"Victoire de {self.matches[num_match].player1.name}. \n"
                    if self.matches[num_match].winner == 2:
                        message += f"Victoire de {self.matches[num_match].player2.name}. \n"
        return message

    def round_to_dict(self):
        """ Converts a round into a dictionary

        :return: the round instance converted in a dictionary.

        """
        string_attributes = ['round_nb',
                             'name',
                             'tournament_ID',
                             'players_ranked',
                             'finished',
                             'players_sorted']
        serialized_round = {}
        for attribute in string_attributes:
            serialized_round[attribute] = getattr(self, attribute)
        serialized_round['players'] = []
        for player in self.players:
            serialized_round['players'].append(player.player_to_dict())
        serialized_round['matches'] = {}
        for key, value in self.matches.items():
            serialized_round['matches'][key] = value.match_to_dict()
        serialized_round['start_date'] = str(self.start_date)
        serialized_round['end_date'] = str(self.end_date)
        return serialized_round

    def rank_players(self):
        """ Ranks players by points in the tournament (decreasingly) and then by rank.

        The method checks if the players have been ranked before.

        :return: None

        """
        if not self.players_ranked:
            sorted_players = sorted(self.players, key=attrgetter("rank"))
            sorted_players = sorted(sorted_players, key=attrgetter("points"), reverse=True)
            for rank in range(NB_PLAYERS):
                sorted_players[rank].place = rank + 1
            self.players_ranked = True

    def define_matches(self):
        """ Defines the matches of a round according to the rules of Swiss tournament
        :return: None
        """
        if self.round_nb == 0:
            for match in range(NB_MATCH):
                self.matches[match] = Match(match, self.round_nb, self.tournament_ID)
                for player in range(NB_PLAYERS):
                    if self.players[player].place == MATCH_1ST_ROUND[match][0]:
                        self.matches[match].player1 = self.players[player]
                    if self.players[player].place == MATCH_1ST_ROUND[match][1]:
                        self.matches[match].player2 = self.players[player]
        else:
            first_non_assigned = 0
            sorted_players = sorted(self.players, key=attrgetter("place"))
            player_assigned = []
            for match in range(NB_MATCH):
                while sorted_players[first_non_assigned] in player_assigned:
                    first_non_assigned += 1
                self.matches[match] = Match(match, self.round_nb, self.tournament_ID)
                self.matches[match].player1 = sorted_players[first_non_assigned]
                player_assigned.append(sorted_players[first_non_assigned])
                first_non_assigned += 1
                id_player = min(first_non_assigned, len(sorted_players)-1)
                while sorted_players[id_player].player_id\
                        in self.matches[match].player1.opponents\
                        or sorted_players[id_player]\
                        in player_assigned:
                    id_player += 1
                    if id_player >= len(sorted_players):
                        break
                id_player = min(id_player, len(sorted_players)-1)
                self.matches[match].player2 = sorted_players[id_player]
                player_assigned.append(sorted_players[id_player])
                if id_player == first_non_assigned:
                    first_non_assigned += 1

    def register_results(self, winners):
        """ Registers the results of a round.

        :param winners: 0 for a tie, 1 when the first player quoted wins and 2 when it's the second quoted.
        :return: None

        """
        for num_match in range(NB_MATCH):
            self.matches[num_match].declare_result(winners[num_match])
        self.finished = True

    def assign_points(self):
        """ Assigns the points this round, for each matches

        Players_ranked is switched to False
        :return: None

        """
        for num_match in range(NB_MATCH):
            self.matches[num_match].assign_points()
        self.players_ranked = False

    def memorize_opponents(self):
        """ For each player, appends the current opponent in the list of previous opponents.
        :return: None
        """
        for match in range(NB_MATCH):
            self.matches[match].player1.opponents.append(self.matches[match].player2.player_id)
            self.matches[match].player2.opponents.append(self.matches[match].player1.player_id)
