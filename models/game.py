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
    """
    An actor is the identity of player of the different tournaments
    """
    last_actor_id = "0"*ID_WIDTH

    def __init__(self, last_name, first_name, birthdate, gender, rank):
        if Actor.last_actor_id.lstrip('0') == "":
            Actor.last_actor_id = str(1)
        else:
            Actor.last_actor_id = str(int(Actor.last_actor_id.lstrip('0')) + 1)
        self.actor_id = \
            (ID_WIDTH + 1 - len(Actor.last_actor_id.lstrip('0'))) * "0" \
            + Actor.last_actor_id
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank

    def __repr__(self):
        return f"Personne: nom({self.last_name}), prénom({self.first_name}) \n" \
               f"Identifiant: {self.actor_id}\n" \
               f"Classement: {self.rank} \n"


class Player:
    """
    A player mean a player in a specific tournament
    """
    def __init__(self, actor, tournament_id, player_id):
        self.actor = actor
        self.name = self.actor.first_name + " " + self.actor.last_name
        self.tournament_id = tournament_id
        self.player_id = player_id
        self.rank = actor.rank
        self.ranking = 0
        self.points = 0
        self.place = 0
        self.opponents = []

    def __repr__(self):
        return f"Nom: {self.actor.last_name}, Prénom: {self.actor.first_name} \n" \
               f"Identifiant: {self.actor.actor_id}\n" \
               f"Classement: {self.rank}\n" \
               f"Dans le tournoi {self.tournament_id}: \n" \
               f"Rang: {self.ranking}\n" \
               f"Points: {self.points}\n" \
               f"A joué contre: {self.opponents} \n"


class Match:
    """
    A Match is one of the 4 duel in a round
    """
    def __init__(self, match_nb, round_nb, tournament_id):
        self.match_nb = match_nb
        self.round_nb = round_nb
        self.tournament_id = tournament_id
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
        if self.points_assigned:
            print("Already assigned")
        else:
            if self.winner == 0:
                self.player1.points = POINTS["draw"]
                self.player2.points = POINTS["draw"]
            elif self.winner == 1:
                self.player1.points = POINTS["victory"]
                self.player2.points = POINTS["defeat"]
            elif self.winner == 2:
                self.player1.points = POINTS["defeat"]
                self.player2.points = POINTS["victory"]
            self.points_assigned = True


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

    def rank_players(self):
        """
        Sort the player by points and if they are draw player, by rank
        :return:
        """
        if not self.players_ranked:
            sorted_players = sorted(self.players, key=attrgetter("points", "rank"))
            for position in range(NB_PLAYERS):
                sorted_players[position].place = position + 1
            self.players_ranked = True
        else:
            print("Already ranked")

    def memorize_opponents(self):
        """
        For each player, memorize their previous
        opponents during the previous rounds
        :return: None
        """
        for match in range(NB_MATCH):
            self.matchs[match].player1.opponents = self.matchs[match].player2
            self.matchs[match].player2.opponents = self.matchs[match].player1


class Tournament:
    """
    A Tournament
    """
    last_tournament_id = "0"*ID_WIDTH

    def __init__(self, name, location):
        self.tournament_id = \
            (ID_WIDTH + 1 - len(str(Tournament.last_tournament_id)))*"0"\
            + str(int(Tournament.last_tournament_id.lstrip('0'))+1)
        self.name = name
        self.location = location
        self.start_date = None
        self.end_date = None
        self.timer_type = ""
        self.description = ""
        self.number_of_rounds = NB_ROUND
        self.rounds = [] # La liste des instances de tours.
        self.list_of_players = [] # Liste des indices correspondant aux instances du joueur stockées en mémoire)
        self.players_assigned = False

    def start_tournament(self):
        """
        Launch the Tournament
        :return:
        """
        '''controllers.input.define_players'''
        acteur1 = Actor("Skywalker", "Anakin", datetime.date(41, 5, 6), "M", 8)  # 2
        acteur2 = Actor("Skywalker", "Luke", datetime.date(19, 12, 7), "M", 21)  # 3
        acteur3 = Actor("Organa", "Leia", datetime.date(19, 12, 7), "F", 143)  # 8
        acteur4 = Actor("Tano", "Ahsoka", datetime.date(36, 11, 22), "F", 35)  # 5
        acteur5 = Actor("Master", "Yoda", datetime.date(896, 10, 15), "M", 3)  # 1
        acteur6 = Actor("Palpatine", "Sheev", datetime.date(84, 2, 25), "M", 27)  # 4
        acteur7 = Actor("Kashyyyk", "Chewbacca", datetime.date(200, 8, 31), "M", 112)  # 7
        acteur8 = Actor("Solo", "Han", datetime.date(34, 7, 16), "M", 107)  # 6
        joueur1 = Player(acteur1, 5, 1)
        joueur2 = Player(acteur2, 5, 2)
        joueur3 = Player(acteur3, 5, 3)
        joueur4 = Player(acteur4, 5, 4)
        joueur5 = Player(acteur5, 5, 5)
        joueur6 = Player(acteur6, 5, 6)
        joueur7 = Player(acteur7, 5, 7)
        joueur8 = Player(acteur8, 5, 8)
        joueurs = [joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8]
        '''controllers.input.define_players'''

        tour1 = Round(1, self.tournament_id, joueurs)
        tour1.define_matchs()

        '''Annonce des matchs'''

        '''controllers et views : Entrées des résultats -> Choix du match -> Entrée 0(nul) ou le numéro du gagnant : 1 ou 2'''
        tour1.matchs[0].declare_result(1)
        tour1.matchs[1].declare_result(2)
        tour1.matchs[2].declare_result(0)
        tour1.matchs[3].declare_result(1)
        tour1.finished = True
        '''for k in range(NB_PLAYERS):
            Tour1.matchs[k].assign_points()'''
        pass


if __name__ == "__main__":
    # execute only if run as a script

    """Tests Round"""
    acteur1 = Actor("Skywalker", "Anakin", datetime.date(41, 5, 6), "M", 8)       # 2
    acteur2 = Actor("Skywalker", "Luke", datetime.date(19, 12, 7), "M", 21)       # 3
    acteur3 = Actor("Organa", "Leia", datetime.date(19, 12, 7), "F", 143)         # 8
    acteur4 = Actor("Tano", "Ahsoka", datetime.date(36, 11, 22), "F", 35)         # 5
    acteur5 = Actor("Yoda", "Maître", datetime.date(896, 10, 15), "M", 3)         # 1
    acteur6 = Actor("Palpatine", "Sheev", datetime.date(84, 2, 25), "M", 27)      # 4
    acteur7 = Actor("Kashyyyk", "Chewbacca", datetime.date(200, 8, 31), "M", 112) # 7
    acteur8 = Actor("Solo", "Han", datetime.date(34, 7, 16), "M", 107)            # 6
    joueur1 = Player(acteur1, "00000001", 1)
    joueur2 = Player(acteur2, "00000001", 2)
    joueur3 = Player(acteur3, "00000001", 3)
    joueur4 = Player(acteur4, "00000001", 4)
    joueur5 = Player(acteur5, "00000001", 5)
    joueur6 = Player(acteur6, "00000001", 6)
    joueur7 = Player(acteur7, "00000001", 7)
    joueur8 = Player(acteur8, "00000001", 8)
    joueurs = [joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8]
    '''controllers.input.define_players'''

    tour1 = Round(1, "00000001", joueurs)

    ''' Test si pas de rangement des joueurs'''
    print(tour1)
    tour1.define_matchs()

    '''Rangement et définition des matchs'''
    tour1.rank_players()
    tour1.define_matchs()

    '''Annonce des matchs'''
    print(tour1)

    '''controllers et views : Entrées des résultats -> Choix du match -> Entrée 0(nul) ou le numéro du gagnant : 1 ou 2'''
    tour1.matchs[0].declare_result(1)
    tour1.matchs[1].declare_result(2)
    tour1.matchs[2].declare_result(0)
    tour1.matchs[3].declare_result(1)
    tour1.finished = True
    '''controllers et views : Attribution des points et annonce des résultats'''
    tour1.matchs[0].assign_points()
    tour1.matchs[1].assign_points()
    tour1.matchs[2].assign_points()
    tour1.matchs[3].assign_points()

    print(tour1)

    for k in range(NB_PLAYERS):
        print(joueurs[k])

    # tour1.memorize_opponents()
    """ Tri dico 
    print(sorted({"Anakin": 1, "Ahsoka": 45, "Obiwan": 58, "Plokoon": 15}.items(), key=lambda t: t[1]))
    k = list({"Anakin": 1, "Ahsoka": 45, "Obiwan": 58, "Plokoon": 15}.values())
    print(k)
    k.sort()
    print(k)
    """
"""
    acteur1 = Actor("Skywalker", "Anakin", datetime.date(41, 5, 6), "M", 8)  # 2
    acteur2 = Actor("Skywalker", "Luke", datetime.date(19, 12, 7), "M", 21)  # 3
    acteur3 = Actor("Organa", "Leia", datetime.date(19, 12, 7), "F", 143)  # 8
    acteur4 = Actor("Tano", "Ahsoka", datetime.date(36, 11, 22), "F", 35)  # 5
    acteur5 = Actor("Master", "Yoda", datetime.date(896, 10, 15), "M", 3)  # 1
    acteur6 = Actor("Palpatine", "Sheev", datetime.date(84, 2, 25), "M", 27)  # 4
    acteur7 = Actor("Kashyyyk", "Chewbacca", datetime.date(200, 8, 31), "M", 112)  # 7
    acteur8 = Actor("Solo", "Han", datetime.date(34, 7, 16), "M", 107)  # 6
    Player1 = Player(acteur1)
    Player2 = Player(acteur2)
    Player3 = Player(acteur3)
    Player4 = Player(acteur4)
    Player5 = Player(acteur5)
    Player6 = Player(acteur6)
    Player7 = Player(acteur7)
    Player8 = Player(acteur8)
    self.list_of_players = [Player1, Player2, Player3, Player4, Player5, Player6, Player7, Player8]
"""