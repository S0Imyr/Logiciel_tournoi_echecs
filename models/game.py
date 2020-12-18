from operator import attrgetter
import datetime


FIRST = 1
ID_WIDTH = 8
NB_PLAYERS = 8
NB_MATCH = 4
NB_ROUND = 4
POINTS = {"victory": 1, "draw": 0.5, "defeat": 0}
MATCH_1ST_ROUND = [[1, 5], [2, 6], [3, 7], [4, 8]]
MATCH_OTHER_ROUND = [[1, 2], [3, 4], [5, 6], [7, 8]]


class Actor:
    last_player_id = "0"*ID_WIDTH

    def __init__(self, last_name, first_name, birthdate, gender, rank):
        if Actor.last_player_id.lstrip('0') == "":
            Actor.last_player_id = str(1)
        else:
            Actor.last_player_id = str(int(Actor.last_player_id.lstrip('0')) + 1)
        self.player_id = \
            (ID_WIDTH + 1 - len(Actor.last_player_id.lstrip('0'))) * "0" \
            + Actor.last_player_id
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank


class Player:
    def __init__(self, actor):
        self.actor = actor
        self.rank = actor.rank
        self.points = 0
        self.ranking = 0
        self.opponents = []


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


class Round:
    def __init__(self, round_nb, tournament_id, players):
        self.tournament_id = tournament_id
        self.round_nb = round_nb
        self.players = players
        self.players_ranked = False
        self.matchs = {}

    def ranking_players(self):
        if not self.players_ranked:
            sorted_players = sorted(self.players, key=attrgetter("points", "rank"))
            for rank in range(NB_PLAYERS):
                sorted_players[rank].ranking = rank + 1
            self.players_ranked = True
        else:
            print("Already ranked")

    def define_matchs(self):
        if self.players_ranked:
            if self.round_nb == 1:
                for match in range(NB_MATCH):
                    self.matchs[match] = Match(match, self.round_nb, self.tournament_id)
                    for player in range(NB_PLAYERS):
                        if self.players[player].ranking == MATCH_1ST_ROUND[match][0]:
                            self.matchs[match].player1 = self.players[player]
                        if self.players[player].ranking == MATCH_1ST_ROUND[match][1]:
                            self.matchs[match].player2 = self.players[player]
            else:
                pass

        else:
            print("Caution, You need to rank players first !")

    def memorize_opponents(self):
        for match in range(NB_MATCH):
            self.matchs[match].player1.opponents = self.matchs[match].player2
            self.matchs[match].player2.opponents = self.matchs[match].player1


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
        self.number_of_rounds = NB_ROUND
        self.rounds = "" # La liste des instances de tours.
        self.list_of_players = "" # Liste des indices correspondant aux instances du joueur stockées en mémoire)
        self.timer_type = ""
        self.description = ""

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
    acteur1 = Actor("Skywalker", "Anakin", datetime.date(41, 5, 6), "M", 8)       # 2
    acteur2 = Actor("Skywalker", "Luke", datetime.date(19, 12, 7), "M", 21)       # 3
    acteur3 = Actor("Organa", "Leia", datetime.date(19, 12, 7), "F", 143)         # 8
    acteur4 = Actor("Tano", "Ahsoka", datetime.date(36, 11, 22), "F", 35)         # 5
    acteur5 = Actor("Master", "Yoda", datetime.date(896, 10, 15), "M", 3)         # 1
    acteur6 = Actor("Palpatine", "Sheev", datetime.date(84, 2, 25), "M", 27)      # 4
    acteur7 = Actor("Kashyyyk", "Chewbacca", datetime.date(200, 8, 31), "M", 112) # 7
    acteur8 = Actor("Solo", "Han", datetime.date(34, 7, 16), "M", 107)            # 6
    joueur1 = Player(acteur1)
    joueur2 = Player(acteur2)
    joueur3 = Player(acteur3)
    joueur4 = Player(acteur4)
    joueur5 = Player(acteur5)
    joueur6 = Player(acteur6)
    joueur7 = Player(acteur7)
    joueur8 = Player(acteur8)
    joueurs = [joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8]
    tour1 = Round(1, "00000001", joueurs)
    for k in range(8):
        print(joueurs[k].ranking)
    tour1.ranking_players()
    for k in range(8):
        print(joueurs[k].ranking)
    tour1.define_matchs()
    print(tour1.matchs[0].player1.actor.last_name)
    print(tour1.matchs[0].player2.actor.last_name)
    print(tour1.matchs[0].player2.opponents)
    tour1.memorize_opponents()
    print(tour1.matchs[0].player2.opponents.actor.last_name)
    """ Tri dico 
    print(sorted({"Anakin": 1, "Ahsoka": 45, "Obiwan": 58, "Plokoon": 15}.items(), key=lambda t: t[1]))
    k = list({"Anakin": 1, "Ahsoka": 45, "Obiwan": 58, "Plokoon": 15}.values())
    print(k)
    k.sort()
    print(k)
    """