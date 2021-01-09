from chess.models.actors import Actor
from chess.models.game import Tournament
from chess.utils.conversion import str_to_date
from tinydb import TinyDB


def export_actor(actor):
    db = TinyDB('db.json')
    actors_table = db.table('actors')
    dictio = actor.actor_to_dict()
    actors_table.insert(dictio)


def export_tournament(tournament, step):
    pass


def import_actors():
    db = TinyDB('db.json')
    actors_table = db.table('actors')
    serialized_actors = actors_table.all()
    actors = []
    for value in serialized_actors:
        actor = Actor(value['last_name'],
                      value['first_name'],
                      str_to_date(value['birthdate']),
                      value['gender'],
                      value['rank'])
        actor.dict_to_actor(value)
        actors.append(actor)
    return len(serialized_actors), actors


def import_tournament():
    pass




if __name__ == '__main__':
    import datetime
    from chess.models.actors import Actor, Player

    TinyDB('db.json').table('actors').truncate()
    acteur1 = Actor("Skywalker", "Anakin", datetime.date(41, 5, 6), "M", 8)

    export_actor(acteur1)
    # print(vars(acteur1))
    acteurs = import_actors()
    print(acteurs[1])
    # joueur1 = Player(acteur1, "00000001", 1)
    # print(vars(joueur1))

    pass
