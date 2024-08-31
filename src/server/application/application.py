import pygame

from src.client.sprites.player_sprite import PlayerSprite
from src.server.network.resource import Resource
from src.common.managers.gui_manager import GUIManager
from src.common.constants.application_constants import FPS, BACKGROUND_COLOR
from src.client.client import Client


class Application:
    def __init__(self):
        self.client = Client()
        self.gui_manager = GUIManager()
        self.event = None
        self.can_shoot = True
        self.resources = {}
        self.players = {}

    def initialise(self):
        self.gui_manager.initialise()

    def connect_client(self):
        print("CLIENT: Waiting for id from server")

        self.client.connect()
        self.client.wait_for_id_from_server()

        while self.client.id == -1:
            pass

        print(f"CLIENT: id is {self.client.id}")

    def run(self, window):
        clock = pygame.time.Clock()
        is_running = True
        self.connect_client()

        while is_running:
            delta_time = clock.tick(FPS) / 1000.0
            window.fill(BACKGROUND_COLOR)

            for event in pygame.event.get():
                self.event = event

                if event.type == pygame.QUIT:
                    is_running = False

                self.gui_manager.process_events(self.client, event)

            self.update(delta_time)
            self.render(window)

            pygame.display.update()

        pygame.quit()

    def move(self):
        keys = pygame.key.get_pressed()
        data = {"type": "move", "dx": 0, "dy": 0}

        if self.gui_manager.is_chat_hidden():
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

    # Add support for holding down mouse button soon
    def shoot(self):
        if not self.gui_manager.is_chat_hidden():
            return

        if not self.resources:
            return

        resource = next(iter(self.resources.values()))

        if not isinstance(resource, Resource):
            return

        if pygame.mouse.get_pressed()[0]:
            if self.can_shoot:
                self.can_shoot = False
                data = {"type": "shoot"}
                resource = self.resources[self.client.id]
                player = resource.get_entity("player")
                data["source"] = (player.position.x, player.position.y)
                data["destination"] = pygame.mouse.get_pos()
                self.client.send(data)
                self.resources = self.client.get_resources()
        else:
            if not self.can_shoot:
                self.can_shoot = True

    def update_sprites(self):
        if not self.resources:
            return

        resource = next(iter(self.resources.values()))

        if not isinstance(resource, Resource):
            return

        for resource_id, resource in self.resources.items():
            player = resource.get_entity("player")

            if resource_id not in self.players:
                self.players[resource_id] = PlayerSprite(resource_id)

            self.players[resource_id].update(player)

    def update(self, delta_time):
        self.move()
        self.shoot()
        self.update_sprites()
        self.gui_manager.update(self.client, delta_time)

    def render(self, window):
        if not self.resources:
            return

        resource = next(iter(self.resources.values()))

        if not isinstance(resource, Resource):
            return

        for player in self.players.values():
            player.render(window)

        for resource in self.resources.values():
            player = resource.get_entity("player")
            player.render(window)

        self.gui_manager.render(window)
