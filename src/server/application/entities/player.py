import pygame

from src.common.utilities.vector2 import Vector2


class Player:
    def __init__(self, x, y, width, height, color):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 8

    def move(self, dx, dy):
        self.velocity.x = dx
        self.velocity.y = dy
        self.velocity.normalise()
        self.velocity *= self.speed
        self.position += self.velocity
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def render(self, window):
        pygame.draw.rect(window, self.color, self.rect)
