from operator import attrgetter
from chess.models.match import Match


NB_PLAYERS = 8
NB_MATCH = 4
MATCH_1ST_ROUND = [[1, 5], [2, 6], [3, 7], [4, 8]]
MATCH_OTHER_ROUND = [[1, 2], [3, 4], [5, 6], [7, 8]]


class Round:
    """
    A round is a set in a tournament
    """
    def __init__(self, round_nb, tournament_id, players):
        self.round_nb = round_nb
        self.tournament_id = tournament_id
        self.players = players
        self.players_ranked = False
        self.matchs = {}
        self.finished = False

    def __repr__(self):
        repr = f"Tour {self.round_nb} du tournoi {self.tournament_id} \n"
        if self.matchs != {}:
            if self.finished:
                repr += f"Les matchs ont vu s'affronter : \n"
            else:
                repr += f"Les matchs verront s'affronter : \n"
            for num_match in range(NB_MATCH):
                repr += f"{num_match+1}. {self.matchs[num_match].player1.name} et {self.matchs[num_match].player2.name} \n"
                if self.finished:
                    if self.matchs[num_match].winner == 0:
                        repr += f"Match nul. \n"
                    if self.matchs[num_match].winner == 1:
                        repr += f"Victoire de {self.matchs[num_match].player1.name}. \n"
                    if self.matchs[num_match].winner == 2:
                        repr += f"Victoire de {self.matchs[num_match].player2.name}. \n"
        return repr

    def rank_players(self):
        if not self.players_ranked:
            sorted_players = sorted(self.players, key=attrgetter("rank"))
            sorted_players = sorted(sorted_players, key=attrgetter("points"), reverse = True)
            for rank in range(NB_PLAYERS):
                sorted_players[rank].place = rank + 1
            self.players_ranked = True
        else:
            print("Already ranked")

    def define_matchs(self):
        """
        define the matchs of a round according to
         the rules of Swiss tournament
        :return:
        """
        if self.players_ranked:
            if self.round_nb == 1:
                for match in range(NB_MATCH):
                    self.matchs[match] = Match(match, self.round_nb, self.tournament_id)
                    for player in range(NB_PLAYERS):
                        if self.players[player].place == MATCH_1ST_ROUND[match][0]:
                            self.matchs[match].player1 = self.players[player]
                        if self.players[player].place == MATCH_1ST_ROUND[match][1]:
                            self.matchs[match].player2 = self.players[player]
            else:
                pass
        else:
            print("Attention, vous devez ranger les joueurs d'abord! \n")

    def memorize_opponents(self):
        """
        For each player, memorize their previous
        opponents during the previous rounds in a list
        :return: None
        """
        for match in range(NB_MATCH):
            self.matchs[match].player1.opponents.append(self.matchs[match].player2.player_id)
            self.matchs[match].player2.opponents.append(self.matchs[match].player1.player_id)
