# -*- coding: utf-8 -*-


"""
This module handle the match logic.
"""


POINTS = {"victory": 1, "draw": 0.5, "defeat": 0}


class Match:
    """ A Match is one of the 4 duel in a round. """
    def __init__(self, match_nb, round_nb, tournament_id):
        self.match_nb = match_nb
        self.round_nb = round_nb
        self.tournament_ID = tournament_id
        self.player1 = None
        self.player2 = None
        self.winner = None
        self.finished = False
        self.points_assigned = False

    def __str__(self):
        display = f"Match {self.match_nb + 1}: \n" \
              f"1: {self.player1.name} vs 2:{self.player2.name}\n"
        winner = "Aucun"
        if self.finished:
            if self.winner == 1:
                winner = self.player1.name
            if self.winner == 2:
                winner = self.player2.name
            display += f"Le match a été remporté par {winner} \n"
        return display

    def declare_result(self, num_player):
        """ Declares the winner by assigning the winner's number to the winner attribute

        :param num_player: 1 for the first quoted, 2 for the second, 0 when it's a tie game.
        :return: None

        """
        if self.finished:
            print("Already registered")
        else:
            self.winner = num_player
            self.finished = True

    def assign_points(self):
        """ Assigns points to the players.

        The function test if points are already assign, and then assigns the points

        :return: None
        """
        if self.winner is None:
            print("Attention, aucun joueur n'a été déclaré vainqueur")
        if self.winner == 0:
            self.player1.points += POINTS["draw"]
            self.player2.points += POINTS["draw"]
        elif self.winner == 1:
            self.player1.points += POINTS["victory"]
            self.player2.points += POINTS["defeat"]
        elif self.winner == 2:
            self.player1.points += POINTS["defeat"]
            self.player2.points += POINTS["victory"]
        self.points_assigned = True

    def match_to_dict(self):
        """ Converts a match into a dictionary.

        :return: the dictionary of the match instance.

        """
        string_attributes = ['match_nb',
                             'round_nb',
                             'tournament_ID',
                             'winner',
                             'finished',
                             'points_assigned']
        serialized_match = {}
        for attribute in string_attributes:
            serialized_match[attribute] = getattr(self, attribute)
        # no_string_attributes = ['player1', 'player2']
        serialized_match['player1'] = self.player1.player_to_dict()
        serialized_match['player2'] = self.player2.player_to_dict()
        return serialized_match
