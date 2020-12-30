POINTS = {"victory": 1, "draw": 0.5, "defeat": 0}


class Match:
    def __init__(self, match_nb, round_nb, tournament_id):
        self.match_nb = match_nb
        self.round_nb = round_nb
        self.tournament_id = tournament_id
        self.player1 = None
        self.player2 = None
        self.players_points = [0, 0]
        self.winner = None
        self.finished = False
        self.points_assigned = False

    def declare_result(self, num_player):
        if self.finished:
            print("Already registered")
        else:
            if num_player is not None:
                self.winner = num_player
                self.finished = True

    def assign_points(self):
        if self.points_assigned:
            print("Already assigned")
        else:
            if self.winner is None:
                self.players_points = [POINTS["draw"], POINTS["draw"]]
            elif self.winner == 1:
                self.players_points = [POINTS["victory"], POINTS["defeat"]]
            elif self.winner == 2:
                self.players_points = [POINTS["defeat"], POINTS["victory"]]
            self.points_assigned = True
            self.player1.points += self.players_points[0]
            self.player2.points += self.players_points[1]
