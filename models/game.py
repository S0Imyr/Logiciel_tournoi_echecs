ID_WIDTH = 8

class Tournament:
    last_tournament_id = "0"*ID_WIDTH
    def __init__(self, name, location, start_date, end_date):
        self.tournament_id = (ID_WIDTH+1-len(str(Tournament.last_tournament_id)))*"0"+str(int(Tournament.last_tournament_id.lstrip('0'))+1)
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = 4
        self.rounds = "" # La liste des instances de tours.
        self.list_of_players = "" # Liste des indices correspondant aux instances du joueur stockées en mémoire)
        self.timer_type = "" # C'est toujours un bullet, un blitz ou un coup rapide)
        self.description = "" # Les remarques générales du directeur du tournoi vont ici).

class Round:
    def __init__(self, tournament_id):
        self.tournament_id = tournament_id
        self.number = 0
        self.players = []
        self.players_rank = []

    def rank_players(self):
        pass

    def define_matches(self):
        pass

class Match:
    def __init__(self):
        self.id_match
        self.id_round
        self.id_tournament
        self.players = []

    def assign_points(self):
        pass