ID_WIDTH = 8


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
        return f"Personne: Nom :{self.last_name}, Prénom :{self.first_name} \n" \
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
