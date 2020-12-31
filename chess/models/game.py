import datetime
import constant
import actors
import match
import round


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
    list_id_players = ["00002501", "00002502", "00002503", "00002504", "00002505", "00002506", "00002507", "00002508"]
    # execute only if run as a script
    """Tests Player"""
    """
    dark_vador = Player("Skywalker", "Anakin", "16/03/1988", "M", 168)
    padawan = Player("Tano", "Ahsoka", "11/10/1982", "F", 99)
    print(dark_vador.player_id, padawan.opponents)
    """
    """Tests match"""
    """
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