import pygame

from src.utility.math import Vector2


class Player:
    def __init__(self, x, y, width, height, color):
        self.position = Vector2(x, y)
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = 10

    def move(self, dx, dy):
        self.position.x += self.velocity * dx
        self.position.y += self.velocity * dy
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def render(self, window):
        pygame.draw.rect(window, self.color, self.rect)
