import pygame

from src.common.constants.application_constants import WINDOW_HEIGHT, WINDOW_WIDTH
from src.common.utilities.utility import Utility


class ConnectionSprite:
    def __init__(self):
        self.sprites = Utility.get_connection_sprites((2, 2))
        self.font = pygame.font.SysFont("Determination Mono Web", 16)
        self.font_surface = None
        self.sprite = self.sprites[0]
        self.rect = self.sprite.get_rect()
        self.rect.center = (WINDOW_WIDTH - self.rect.width, WINDOW_HEIGHT - self.rect.height)
        self.text_rect = self.rect

    def update(self, client):
        latency = Utility.clamp(int(client.latency * 10000), 0, 999)
        sprite_index = 0
        if latency <= 100:
            sprite_index = 0
        elif latency >= 150:
            sprite_index = 2
        else:
            sprite_index = 1
        self.sprite = self.sprites[sprite_index]
        text = f"{latency} ms"
        self.font_surface = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.font_surface.get_rect()
        self.text_rect.center = self.rect.center
        self.text_rect.centery += self.rect.height - 10

    def render(self, window):
        window.blit(self.sprite, self.rect)
        window.blit(self.font_surface, self.text_rect)
