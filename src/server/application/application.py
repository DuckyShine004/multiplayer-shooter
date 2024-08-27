import pygame
from src.client.client import Client


class Application:
    def __init__(self):
        self.client = Client()
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

        self.client.send(data)

    def update(self):
        self.move_players()

    def render(self, window): ...
