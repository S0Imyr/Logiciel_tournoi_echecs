from chess.utils.conversion import list_to_str_space
from chess.utils.utils import get_new_id


ACTOR_ID_WIDTH = 8


class Actor:
    """
    An actor is the identity of player of the different tournaments
    """
    last_actor_id = "0" * ACTOR_ID_WIDTH

    def __init__(self, last_name, first_name, birthdate, gender, rank):
        Actor.last_actor_id = get_new_id(Actor.last_actor_id, ACTOR_ID_WIDTH)
        self.actor_id = Actor.last_actor_id
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        self.list_of_tournaments_played = []

    def __str__(self):
        return f"Personne: Nom: {self.last_name}, Prénom: {self.first_name} \n" \
               f"Identifiant: {self.actor_id}\n" \
               f"Classement: {self.rank} \n"

    def modify_rank(self, rank):
        self.rank = rank

    def actor_to_dict(self):
        """
        convert the actor into a dictionnary
        :return:
        """
        string_attributes = ['actor_id', 'last_name', 'first_name', 'gender', 'rank']
        serialized_actor = {}
        for attribute in string_attributes:
            serialized_actor[attribute] = getattr(self, attribute)
        # no_string_attributes = ['birthdate', 'tournaments']
        serialized_actor['birthdate'] = str(self.birthdate)
        serialized_actor['tournaments'] = list_to_str_space(self.list_of_tournaments_played)
        return serialized_actor


class Player:
    """
    A player mean a player in a specific tournament
    """
    def __init__(self, actor, tournament_id, player_id):
        self.actor = actor
        self.name = self.actor.first_name + " " + self.actor.last_name
        self.tournament_ID = tournament_id
        self.player_id = player_id
        self.rank = actor.rank
        self.ranking = 0
        self.points = 0
        self.place = 0
        self.opponents = []

    def __str__(self):
        return f"Nom: {self.name} \n" \
               f"Identifiant: {self.actor.actor_id}\n" \
               f"Classement: {self.rank}\n" \
               f"Dans le tournoi {self.tournament_ID}: \n" \
               f"Place: {self.place}\n" \
               f"Points: {self.points}\n" \
               f"A joué contre: {self.opponents} \n"

    def player_to_dict(self):
        """
        convert an actor into a dictionnary
        :return: dictionnary of the player serialiazed
        """
        string_attributes = ['name', 'tournament_ID', 'player_id', 'rank', 'ranking', 'points', 'place']
        serialized_player = {}
        for attribute in string_attributes:
            serialized_player[attribute] = getattr(self, attribute)
        # no_string_attributes = ['actor', 'opponents']
        serialized_player['actor'] = self.actor.actor_to_dict()
        serialized_player['opponents'] = list_to_str_space(self.opponents)
        return serialized_player
