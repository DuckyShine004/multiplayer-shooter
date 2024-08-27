import pygame
from src.client.client import Client


class Application:
    def __init__(self):
        self.client = Client()
        self.resources = {}
        self.is_running = True

    def run(self, window):
        clock = pygame.time.Clock()
        self.client.connect()

        while self.is_running:
            window.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()

            self.update()
            self.render(window)

            pygame.display.update()
            clock.tick(60)

        pygame.quit()

    def move_players(self):
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

    def update(self):
        self.move_players()

    def render(self, window):
        if not self.resources:
            return

        for resource in self.resources.values():
            player = resource.get_entity("player")
            player.render(window)
