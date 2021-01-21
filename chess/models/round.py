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
        self.tournament_ID = tournament_id
        self.players = players
        self.players_ranked = False
        self.matchs = {}
        self.finished = False
        self.players_sorted = False

    def __str__(self):
        message = f"Tour {self.round_nb + 1} du tournoi {self.tournament_ID} \n"
        if self.matchs != {}:
            if self.finished:
                message += "Les matchs ont vu s'affronter : \n"
            else:
                message += "Les matchs verront s'affronter : \n"
            for num_match in range(NB_MATCH):
                message += f"{num_match+1}. " \
                           f"{self.matchs[num_match].player1.name}" \
                           f" et {self.matchs[num_match].player2.name} \n"
                if self.finished:
                    if self.matchs[num_match].winner == 0:
                        message += "Match nul. \n"
                    if self.matchs[num_match].winner == 1:
                        message += f"Victoire de {self.matchs[num_match].player1.name}. \n"
                    if self.matchs[num_match].winner == 2:
                        message += f"Victoire de {self.matchs[num_match].player2.name}. \n"
        return message

    def round_to_dict(self):
        """
        Convert a round into a dictionary
        :return:
        """
        string_attributes = ['round_nb',
                             'tournament_ID',
                             'players_ranked',
                             'finished',
                             'players_sorted']
        serialized_round = {}
        for attribute in string_attributes:
            serialized_round[attribute] = getattr(self, attribute)
        # no_string_attributes = ['players' (list), 'matchs' (dict)]
        serialized_round['players'] = []
        for player in self.players:
            serialized_round['players'].append(player.player_to_dict())
        serialized_round['matchs'] = {}
        for key, value in self.matchs.items():
            serialized_round['matchs'][key] = value.match_to_dict()
        return serialized_round

    def rank_players(self):
        """
        Rank players by points in the tournament (decreasingly)
        and by rank
        the method checks if the players have been ranked before
        :return: None
        """
        if not self.players_ranked:
            sorted_players = sorted(self.players, key=attrgetter("rank"))
            sorted_players = sorted(sorted_players, key=attrgetter("points"), reverse=True)
            for rank in range(NB_PLAYERS):
                sorted_players[rank].place = rank + 1
            self.players_ranked = True

    def define_matchs(self):
        """
        define the matchs of a round according to
         the rules of Swiss tournament
        :return:
        """
        if self.round_nb == 0:
            for match in range(NB_MATCH):
                self.matchs[match] = Match(match, self.round_nb, self.tournament_ID)
                for player in range(NB_PLAYERS):
                    if self.players[player].place == MATCH_1ST_ROUND[match][0]:
                        self.matchs[match].player1 = self.players[player]
                    if self.players[player].place == MATCH_1ST_ROUND[match][1]:
                        self.matchs[match].player2 = self.players[player]
        else:
            first_non_assigned = 0
            sorted_players = sorted(self.players, key=attrgetter("place"))
            player_assigned = []
            for match in range(NB_MATCH):
                while sorted_players[first_non_assigned] in player_assigned:
                    first_non_assigned += 1
                self.matchs[match] = Match(match, self.round_nb, self.tournament_ID)
                self.matchs[match].player1 = sorted_players[first_non_assigned]
                player_assigned.append(sorted_players[first_non_assigned])
                first_non_assigned += 1
                id_player = min(first_non_assigned, len(sorted_players)-1)
                while sorted_players[id_player].player_id\
                        in self.matchs[match].player1.opponents\
                        or sorted_players[id_player]\
                        in player_assigned:
                    id_player += 1
                    if id_player >= len(sorted_players):
                        break
                id_player = min(id_player, len(sorted_players)-1)
                self.matchs[match].player2 = sorted_players[id_player]
                player_assigned.append(sorted_players[id_player])
                if id_player == first_non_assigned:
                    first_non_assigned += 1

    def register_results(self, winners):
        """
        register the results of a round
        :param winners: 0 for a tie, 1 when the first player quoted wins
         and 2 when it's the second quoted.
        :return: None
        """
        for num_match in range(NB_MATCH):
            self.matchs[num_match].declare_result(winners[num_match])
        self.finished = True

    def assign_points(self):
        """
        Assign the points this round, for each matchs
        players_ranked is switched to False
        :return: None
        """
        for num_match in range(NB_MATCH):
            self.matchs[num_match].assign_points()
        self.players_ranked = False

    def memorize_opponents(self):
        """
        For each player, append the current opponent
        in the list of previous opponent of the player.
        :return: None
        """
        for match in range(NB_MATCH):
            self.matchs[match].player1.opponents.append(self.matchs[match].player2.player_id)
            self.matchs[match].player2.opponents.append(self.matchs[match].player1.player_id)


if __name__ == '__main__':
    import datetime
    from chess.models.actors import Actor, Player
    """ Données """

    acteur1 = Actor("Skywalker", "Anakin", datetime.date(41, 5, 6), "M", 8)
    acteur2 = Actor("Skywalker", "Luke", datetime.date(19, 12, 7), "M", 21)
    acteur3 = Actor("Organa", "Leia", datetime.date(19, 12, 7), "F", 143)
    acteur4 = Actor("Tano", "Ahsoka", datetime.date(36, 11, 22), "F", 35)
    acteur5 = Actor("Yoda", "Maître", datetime.date(896, 10, 15), "M", 3)
    acteur6 = Actor("Palpatine", "Sheev", datetime.date(84, 2, 25), "M", 27)
    acteur7 = Actor("Kashyyyk", "Chewbacca", datetime.date(200, 8, 31), "M", 112)
    acteur8 = Actor("Solo", "Han", datetime.date(34, 7, 16), "M", 107)
    acteurs = [acteur1, acteur2, acteur3, acteur4, acteur5, acteur6, acteur7, acteur8]

    joueur1 = Player(acteur1, "00000001", 1)
    joueur2 = Player(acteur2, "00000001", 2)
    joueur3 = Player(acteur3, "00000001", 3)
    joueur4 = Player(acteur4, "00000001", 4)
    joueur5 = Player(acteur5, "00000001", 5)
    joueur6 = Player(acteur6, "00000001", 6)
    joueur7 = Player(acteur7, "00000001", 7)
    joueur8 = Player(acteur8, "00000001", 8)
    joueurs = [joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8]

    """ Lancement partie : """
    tour1 = Round(0, "00000001", joueurs)

    tour1.define_matchs()
    tour1.rank_players()
    tour1.define_matchs()
    tour1.register_results([0, 1, 2, 0])
    tour1.assign_points()
    tour1.finished = True
    tour1.memorize_opponents()
    tour1.rank_players()

    print(tour1.matchs)
    print(tour1.players)
