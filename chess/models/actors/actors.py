ID_WIDTH = 8


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
