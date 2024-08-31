import pygame

from src.common.utilities.vector2 import Vector2
from src.common.constants.application_constants import YELLOW


class Bullet:
    def __init__(self, source, destination):
        self.source = source
        self.position = source
        self.direction = Vector2.get_direction(source, destination)
        self.speed = 10
        self.color = YELLOW
        self.rect = pygame.Rect(source.x, source.y, 40, 40)
        self.velocity = self.get_velocity()
        self.max_distance = 500

    def get_velocity(self):
        return self.direction * self.speed

    def get_distance(self):
        return Vector2.get_distance(self.source, self.position)

    def move(self):
        self.position += self.velocity
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def render(self, window):
        pygame.draw.rect(window, self.color, self.rect)
