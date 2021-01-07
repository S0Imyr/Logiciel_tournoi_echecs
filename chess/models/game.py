import datetime
from chess.models.actors import Actor, Player
from chess.models.round import Round


ID_WIDTH = 8
NB_ROUND = 4
NB_PLAYERS = 8
NB_MATCH = 4


class Tournament:
    """
    A Tournament
    """
    last_tournament_id = "0"*ID_WIDTH

    def __init__(self, name, location, start_date, timer, description):
        if Tournament.last_tournament_id.lstrip('0') == "":
            Tournament.last_tournament_id = str(1)
        else:
            Tournament.last_tournament_id = \
                str(int(Tournament.last_tournament_id.lstrip('0')) + 1)
        self.tournament_id = \
            (ID_WIDTH + 1 - len(Tournament.last_tournament_id.lstrip('0')))\
            *"0"+ Tournament.last_tournament_id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = None
        self.timer_type = timer
        self.description = description
        self.number_of_rounds = NB_ROUND
        self.rounds = [] # La liste des instances de tours.
        self.list_of_players = [] # Liste des indices correspondant aux instances du joueur stockées en mémoire)
        self.players_assigned = False

    def start_round(self, num_round):
        """
        Launch the Tournament
        :return:
        """
        tour = Round(num_round, self.tournament_id, self.list_of_players)
        self.rounds.append(tour)
        tour.define_matchs()

        '''Annonce des matchs'''
    def register_round_results(self, num_round, winners):
        '''controllers et views : Entrées des résultats -> Choix du match -> Entrée 0(nul) ou le numéro du gagnant : 1 ou 2'''
        for num_match in range(NB_MATCH):
            self.rounds[num_round].matchs[num_match].declare_result(winners[num_match])
        self.rounds[num_round].finished = True

    def assign_points(self, winners):
        for k in range(NB_PLAYERS):
            tour1.matchs[k].assign_points()



if __name__ == "__main__":

    # execute only if run as a script

    """Tests Player
    dark_vador = Actor("Skywalker", "Anakin", "16/03/1988", "M", 168)
    print(dark_vador)
    """

    """Tests match
    match1 = match("1", "1", "00000001", dark_vador.player_id, padawan.player_id)
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
    acteur5 = Actor("Yoda", "Maître", datetime.date(896, 10, 15), "M", 3)         # 1
    acteur6 = Actor("Palpatine", "Sheev", datetime.date(84, 2, 25), "M", 27)      # 4
    acteur7 = Actor("Kashyyyk", "Chewbacca", datetime.date(200, 8, 31), "M", 112) # 7
    acteur8 = Actor("Solo", "Han", datetime.date(34, 7, 16), "M", 107)            # 6
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


    '''controllers.input.define_players'''

    tour1 = Round(1, "00000001", joueurs)
    # self.rounds.append(tour1)


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


    '''controllers et views : Attribution des points et annonce des résultats'''
    tour1.matchs[0].assign_points()
    tour1.matchs[1].assign_points()
    tour1.matchs[2].assign_points()
    tour1.matchs[3].assign_points()
    tour1.finished = True


    print(tour1)
    tour1.memorize_opponents()

    for k in range(8):
        print(joueurs[k])

    ''' Tour 2 '''

    tour2 = Round(2, "00000001", joueurs)
    # self.rounds.append(tour2)
    tour2.rank_players()
    tour2.define_matchs()
    print(tour2)

    tour2.matchs[0].declare_result(2)
    tour2.matchs[1].declare_result(2)
    tour2.matchs[2].declare_result(1)
    tour2.matchs[3].declare_result(0)

    tour2.matchs[0].assign_points()
    tour2.matchs[1].assign_points()
    tour2.matchs[2].assign_points()
    tour2.matchs[3].assign_points()
    tour2.finished = True

    print(tour2)

    tour2.memorize_opponents()

    for k in range(8):
        print(joueurs[k])


    ''' Tour 3 '''

    tour3 = Round(3, "00000001", joueurs)
    # self.rounds.append(tour3)
    tour3.rank_players()
    tour3.define_matchs()
    print(tour3)

    tour3.matchs[0].declare_result(0)
    tour3.matchs[1].declare_result(2)
    tour3.matchs[2].declare_result(2)
    tour3.matchs[3].declare_result(1)

    tour3.matchs[0].assign_points()
    tour3.matchs[1].assign_points()
    tour3.matchs[2].assign_points()
    tour3.matchs[3].assign_points()
    tour3.finished = True

    print(tour3)

    tour3.memorize_opponents()

    for k in range(8):
        print(joueurs[k])

    ''' Tour 3 '''

    tour4 = Round(4, "00000001", joueurs)
    # self.rounds.append(tour4)
    tour4.rank_players()
    tour4.define_matchs()
    print(tour4)

    tour4.matchs[0].declare_result(1)
    tour4.matchs[1].declare_result(2)
    tour4.matchs[2].declare_result(0)
    tour4.matchs[3].declare_result(1)

    tour4.matchs[0].assign_points()
    tour4.matchs[1].assign_points()
    tour4.matchs[2].assign_points()
    tour4.matchs[3].assign_points()
    tour4.finished = True

    print(tour4)

    tour4.memorize_opponents()



    for k in range(8):
        print(joueurs[k])
    print(acteur1)