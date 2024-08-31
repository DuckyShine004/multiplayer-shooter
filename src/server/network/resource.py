from src.server.application.entities.player import Player


class Resource:
    def __init__(self):
        self.data = {
            "player": None,
            "pong": False,
            "messages": [],
        }

    def initialise(self):
        self.data["player"] = Player(100, 100)

    def get_entity(self, entity_name):
        return self.data[entity_name]

    def set_entity(self, entity_name, entity):
        self.data[entity_name] = entity
