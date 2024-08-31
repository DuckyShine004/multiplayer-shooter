import pygame

from src.common.utilities.vector2 import Vector2


class Gun:
    def __init__(self):
        self.position = Vector2()
        self.theta = 0

    def update(self, position, mouse_position):
        radius = 15
        mouse_position = Vector2(*mouse_position)
        direction = Vector2.get_direction(position, mouse_position)
        self.theta = Vector2.get_theta(position, mouse_position)
        self.position = position + (direction * radius)
