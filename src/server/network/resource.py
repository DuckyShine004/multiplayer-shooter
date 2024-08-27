from src.server.application.entities.player import Player


class Resource:
    def __init__(self):
        self.data = {"player": None}

    def initialise(self):
        self.data["player"] = Player(100, 100, 100, 100, (255, 0, 0))

    def get_entity(self, entity_name):
        return self.data[entity_name]
