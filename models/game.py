ID_WIDTH = 8
POINTS = {"victory": 1, "draw": 0.5, "defeat": 0}


class Player:
    last_player_id = "0"*ID_WIDTH

    def __init__(self, last_name, first_name, birthdate, gender, rank):
        if Player.last_player_id.lstrip('0') == "":
            Player.last_player_id = str(1)
        else:
            Player.last_player_id = str(int(Player.last_player_id.lstrip('0'))+1)
        self.player_id =\
            (ID_WIDTH + 1 - len(Player.last_player_id.lstrip('0')))*"0"\
            + Player.last_player_id
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        self.opponents = []


class Match:
    def __init__(self, match_nb, round_nb, tournament_id, player1, player2):
        self.match_nb = match_nb
        self.round_nb = round_nb
        self.tournament_id = tournament_id
        self.players = [player1, player2]
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


class Round:
    def __init__(self, round_nb, tournament_id, players, players_points, players_rank):
        self.tournament_id = tournament_id
        self.round_nb = round_nb
        self.players = players
        self.players_points = players_points
        self.players_rank = players_rank

    def rank_players(self):
        pass

    def define_matches(self):
        pass


class Tournament:
    last_tournament_id = "0"*ID_WIDTH

    def __init__(self, name, location, start_date, end_date):
        self.tournament_id = \
            (ID_WIDTH + 1 - len(str(Tournament.last_tournament_id)))*"0"\
            + str(int(Tournament.last_tournament_id.lstrip('0'))+1)
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = 4
        self.rounds = "" # La liste des instances de tours.
        self.list_of_players = "" # Liste des indices correspondant aux instances du joueur stockées en mémoire)
        self.timer_type = "" # C'est toujours un bullet, un blitz ou un coup rapide)
        self.description = "" # Les remarques générales du directeur du tournoi vont ici).

    def start_tournament(self):
        pass


if __name__ == "__main__":
    list_id_players = ["00002501", "00002502", "00002503", "00002504", "00002505", "00002506", "00002507", "00002508"]
    # execute only if run as a script
    """Tests Player"""
    """
    dark_vador = Player("Skywalker", "Anakin", "16/03/1988", "M", 168)
    padawan = Player("Tano", "Ahsoka", "11/10/1982", "F", 99)
    print(dark_vador.player_id, padawan.opponents)
    """
    """Tests Match"""
    """
    match1 = Match("1", "1", "00000001", dark_vador.player_id, padawan.player_id)
    print(match1.winner)
    match1.declare_result(1)
    print(match1.winner)
    print(match1.players_points)
    match1.assign_points()
    print(match1.players_points)
    match1.assign_points()
    print(match1.players_points)
    """
    """Tests Round"""