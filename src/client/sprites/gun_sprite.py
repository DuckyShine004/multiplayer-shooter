import math
import pygame

from src.common.utilities.utility import Utility


class GunSprite:
    def __init__(self):
        self.sprite = Utility.get_gun_sprite()
        self.is_flipped = False
        self.rect = self.sprite.get_rect()
        self.theta = 0
        self.threshold = math.pi / 2

    def update(self, gun):
        self.rect.center = (gun.position.x, gun.position.y)
        self.theta = gun.theta
        self.is_flipped = self.theta > self.threshold or self.theta < -self.threshold

    def render(self, window):
        theta = math.degrees(self.theta)
        sprite = Utility.get_flipped_sprite(self.sprite, horizontal=True) if self.is_flipped else self.sprite

        rotated_sprite = pygame.transform.rotate(sprite, theta)
        window.blit(rotated_sprite, self.rect)
