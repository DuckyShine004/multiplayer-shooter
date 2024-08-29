import pygame

from src.server.network.resource import Resource
from src.common.managers.gui_manager import GUIManager
from src.common.constants.application_constants import FPS, BACKGROUND_COLOR
from src.client.client import Client


class Application:
    def __init__(self):
        self.client = Client()
        self.gui_manager = GUIManager()
        self.resources = {}

    def initialise(self):
        self.gui_manager.initialise()

    def run(self, window):
        clock = pygame.time.Clock()
        is_running = True
        self.client.connect()
        self.client.wait_for_id_from_server()

        while is_running:
            delta_time = clock.tick(FPS) / 1000.0
            window.fill(BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                self.gui_manager.process_events(self.client, event)

            self.update(delta_time)
            self.render(window)

            pygame.display.update()

        pygame.quit()

    def move_player(self):
        keys = pygame.key.get_pressed()
        data = {"type": "move", "dx": 0, "dy": 0}

        if keys[pygame.K_a]:
            data["dx"] = -1
        if keys[pygame.K_d]:
            data["dx"] = 1
        if keys[pygame.K_w]:
            data["dy"] = -1
        if keys[pygame.K_s]:
            data["dy"] = 1

        self.client.send(data)
        self.resources = self.client.get_resources()

    def update(self, delta_time):
        self.move_player()
        self.gui_manager.update(self.client, delta_time)

    def render(self, window):
        if not self.resources:
            return

        resource = next(iter(self.resources.values()))

        if not isinstance(resource, Resource):
            return

        for resource in self.resources.values():
            player = resource.get_entity("player")
            player.render(window)

        self.gui_manager.render(window)
