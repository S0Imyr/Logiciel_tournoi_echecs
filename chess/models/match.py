from chess.utils.conversion import list_to_str_space, str_to_date


POINTS = {"victory": 1, "draw": 0.5, "defeat": 0}


class Match:
    """
    A Match is one of the 4 duel in a round
    """
    def __init__(self, match_nb, round_nb, tournament_id):
        self.match_nb = match_nb
        self.round_nb = round_nb
        self.tournament_ID = tournament_id
        self.player1 = None
        self.player2 = None
        self.winner = None
        self.finished = False
        self.points_assigned = False

    def __repr__(self):
        repr = f"Match {self.match_nb + 1}: \n" \
              f"1: {self.player1.name} vs 2:{self.player2.name}\n"
        winner = "Aucun"
        if self.finished:
            if self.winner == 1:
                winner = self.player1.name
            if self.winner == 2:
                winner = self.player2.name
            repr += f"Le match a été remporté par {winner} \n"
        return repr

    def declare_result(self, num_player):
        """
        Declare the winner by assigning the winner's number
         to the winner attribute
        :param num_player: 1 for the first quoted, 2 for the second.
         0 when it's a draw game
        :return: None
        """
        if self.finished:
            print("Already registered")
        else:
            self.winner = num_player
            self.finished = True

    def assign_points(self):
        """
        Assign points to the players
        The function test if points are already assign, and then
        assign the points
        :return:
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
        """
        convert a match into a dictionnary
        :return: a dictionnary
        """
        string_attributes = ['match_nb',
                             'round_nb',
                             'tournament_id',
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


if __name__ == "__main__":
    from chess.models.actors import Actor, Player
    import datetime
    """ Données """
    acteur1 = Actor("Skywalker",
                    "Anakin",
                    datetime.date(41, 5, 6),
                    "M", 8)
    acteur2 = Actor("Skywalker",
                    "Luke",
                    datetime.date(19, 12, 7),
                    "M",
                    21)

    joueur1 = Player(acteur1, "00000001", 1)
    joueur2 = Player(acteur2, "00000001", 2)

    joueurs = [joueur1, joueur2]

    match = Match(2, 3, "00000002")
    match.player1 = joueur1
    match.player2 = joueur2
    match.declare_result(1)
    match.assign_points()

    print("\n Info match : \n")
    print(match)

    """ serialize """
    serie = match.match_to_dict()
    print("\n Test série: \n")
    print(serie)


    print("\n Début deserialize: \n")
    match = Match(serie['match_nb'],
                  serie['round_nb'],
                  serie['tournament_id'])
    print("Donnée Match: ", serie['match_nb'])
    print("Donnée Player 1: ", serie['player1'])
    print("Donnée Player 2: ", serie['player2'])
    print("fin de deserialize: \n")
    match.dict_to_match(serie)
    print("Match: ", match.match_nb)
    print("Player 1", match.player1)
    print("Player 2:", match.player2)
    print("Joueur 1", match.player1.actor)
    print("Joueur 2:", match.player2.actor)


    print(match)