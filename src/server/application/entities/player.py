from src.server.application.entities.gun import Gun
from src.common.utilities.vector2 import Vector2


class Player:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2()
        self.gun = Gun()
        self.speed = 6
        self.bullets = []

    def update_gun(self, mouse_position):
        self.gun.update(self.position, mouse_position)

    def update_bullets(self):
        filtered_bullets = []

        for bullet in self.bullets:
            if bullet.get_distance() < bullet.max_distance:
                filtered_bullets.append(bullet)

        self.bullets = filtered_bullets

        for bullet in self.bullets:
            bullet.move()

    def move(self, dx, dy):
        self.velocity = Vector2(dx, dy).normalised()
        self.velocity *= self.speed
        self.position += self.velocity

    def render(self, window):
        for bullet in self.bullets:
            bullet.render(window)
