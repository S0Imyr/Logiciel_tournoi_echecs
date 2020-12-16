ID_WIDTH = 8


class Player:
    last_id_person = "0"*8
    def __init__(self, player_id, last_name, first_name, birthdate, gender, rank):
        self.player_id = player_id
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        self.opponents = []
        self.person_id = (ID_WIDTH + 1-len(str(Player.last_person_id)))*"0"+str(int(Player.last_person_id.lstrip('0'))+1)


class Person:
    def __init__(self, person_id, last_name, first_name, birthdate, gender, role):
        self.person_id = person_id
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.gender = gender
        self.role = role
