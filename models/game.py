

class Tournament:
    def __init__(self):
        self.id_tournament
        self.name = ""
        self.location = ""
        self.start_date = ""
        self.end_date = ""
        self.number_of_rounds = 4
        self.rounds = ""        # La liste des instances de tours.
        self.players = ""       # Liste des indices correspondant aux instances du joueur stockées en mémoire)
        self.timer = ""         # C'est toujours un bullet, un blitz ou un coup rapide)
        self.description = ""   # Les remarques générales du directeur du tournoi vont ici).

class Round:
    def __init__(self):
        self.id_round
        self.tournament_id
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