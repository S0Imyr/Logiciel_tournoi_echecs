import datetime

from chess.utils.utils import get_new_id

from chess.models.actors import Actor, Player
from chess.models.round import Round


TOURNAMENT_ID_WIDTH = 8
NB_ROUND = 4
NB_PLAYERS = 8
NB_MATCH = 4


class Tournament:
    """
    the class Tournament is the central piece of the models
    """
    last_tournament_id = "0" * TOURNAMENT_ID_WIDTH

    def __init__(self, name, location, timer_type, description):
        Tournament.last_tournament_id = get_new_id(Tournament.last_tournament_id, TOURNAMENT_ID_WIDTH)
        self.tournament_id = Tournament.last_tournament_id
        self.name = name
        self.location = location
        self.start_date = None
        self.end_date = None
        self.timer_type = timer_type
        self.description = description
        self.number_of_rounds = NB_ROUND
        self.rounds = []
        self.list_of_players = []
        self.players_assigned = False

    def define_players(self, actors):
        """
        define the list of id of the players
        :param actors:
        :return: None
        """
        if len(actors) != NB_PLAYERS:
            print("Il n'y a pas assez de joueurs")              ###
        else:
            for num_player in range(NB_PLAYERS):
                self.list_of_players.append(Player(actors[num_player],
                                                   self.tournament_id,
                                                   num_player))

    def init_round(self, num_round):
        """
        Launch the round number "num_round"
        :param num_round: number of the round played
        :return: None
        """
        tour = Round(num_round, self.tournament_id, self.list_of_players)
        tour.rank_players()                     # Rangement des joueurs
        tour.define_matchs()                    # Désignation des matchs
        self.rounds.append(tour)

    def register_round_results(self, num_round, winner):
        """
        register the results
        :param winner:
        :param num_round:
        :return:
        """
        self.rounds[num_round].register_results(winner)
        self.rounds[num_round].assign_points()
        self.rounds[num_round].finished = True
        self.rounds[num_round].memorize_opponents()
        self.rounds[num_round].rank_players()

    def tournament_to_dict(self):
        """
        convert the tournament into a dictionnary
        :return: dictionnary of the class tournament
        """
        string_attributes = ['tournament_id',
                             'name',
                             'location',
                             'timer_type',
                             'description',
                             'number_of_rounds',
                             'players_assigned']
        serialized_tournament = {}
        for attribute in string_attributes:
            serialized_tournament[attribute] = getattr(self, attribute)
        # no_string_attributes = ['start_date', 'end_date' (None / date), 'rounds', 'list_of_players' (list)]
        serialized_tournament['rounds'] = []
        for r0und in self.rounds:
            serialized_tournament['rounds'].append(r0und.round_to_dict())
        serialized_tournament['list_of_players'] = []
        for player in self.list_of_players:
            serialized_tournament['list_of_players'].append(player.player_to_dict())
        serialized_tournament['start_date'] = str(self.start_date)
        serialized_tournament['end_date'] = str(self.end_date)
        return serialized_tournament


if __name__ == "__main__":

    # execute only if run as a script

    acteur1 = Actor("Skywalker", "Anakin", datetime.date(41, 5, 6), "M", 8)       # 2
    acteur2 = Actor("Skywalker", "Luke", datetime.date(19, 12, 7), "M", 21)       # 3
    acteur3 = Actor("Organa", "Leia", datetime.date(19, 12, 7), "F", 143)         # 8
    acteur4 = Actor("Tano", "Ahsoka", datetime.date(36, 11, 22), "F", 35)         # 5
    acteur5 = Actor("Yoda", "Maître", datetime.date(896, 10, 15), "M", 3)         # 1
    acteur6 = Actor("Palpatine", "Sheev", datetime.date(84, 2, 25), "M", 27)      # 4
    acteur7 = Actor("Kashyyyk", "Chewbacca", datetime.date(200, 8, 31), "M", 112) # 7
    acteur8 = Actor("Solo", "Han", datetime.date(34, 7, 16), "M", 107)            # 6
    acteurs = [acteur1, acteur2, acteur3, acteur4, acteur5, acteur6, acteur7, acteur8]

    """joueur1 = Player(acteur1, "00000001", 1)
    joueur2 = Player(acteur2, "00000001", 2)
    joueur3 = Player(acteur3, "00000001", 3)
    joueur4 = Player(acteur4, "00000001", 4)
    joueur5 = Player(acteur5, "00000001", 5)
    joueur6 = Player(acteur6, "00000001", 6)
    joueur7 = Player(acteur7, "00000001", 7)
    joueur8 = Player(acteur8, "00000001", 8)
    joueurs = [joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8]"""

    tournoi = Tournament(name="Star Wars Chess", location="In a galaxy far far away", timer_type="Bz", description="Rien")
    tournoi.start_date = datetime.date.today()
    tournoi.define_players(acteurs)
    print(tournoi.list_of_players)
    """ Tour 1"""
    tournoi.init_round(0)
    print(tournoi.rounds)

    gagnants1 = [0, 1, 2, 0]
    tournoi.register_round_results(0, gagnants1)
    print(tournoi.rounds[0])
    print(tournoi.list_of_players)

    """ Tour 2"""
    tournoi.init_round(1)
    print(tournoi.rounds)

    gagnants2 = [1, 2, 2, 1]
    tournoi.register_round_results(1, gagnants2)
    print(tournoi.rounds[1])
    print(tournoi.list_of_players)

    """ Tour 3"""
    tournoi.init_round(2)
    print(tournoi.rounds)

    gagnants3 = [1, 1, 0, 2]
    tournoi.register_round_results(2, gagnants3)
    print(tournoi.rounds[2])
    print(tournoi.list_of_players)

    """ Tour 4"""
    tournoi.init_round(3)
    print(tournoi.rounds)

    gagnants4 = [2, 2, 1, 0]
    tournoi.register_round_results(3, gagnants4)
    print(tournoi.rounds[3])
    print(tournoi.list_of_players)

    print("\n ###  Vars Tournoi ### \n")
    print(vars(tournoi))

    print("\n ###  serialized Tournoi  ### \n")
    dico = tournoi.tournament_to_dict()
    print(dico)

"""
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
    print(acteur1)"""