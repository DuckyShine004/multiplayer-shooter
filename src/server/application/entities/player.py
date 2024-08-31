from src.common.utilities.vector2 import Vector2


class Player:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2()
        self.speed = 6
        self.bullets = []

    def update_bullets(self):
        filtered_bullets = []

        for bullet in self.bullets:
            if bullet.get_distance() < bullet.max_distance:
                filtered_bullets.append(bullet)

        self.bullets = filtered_bullets

        for bullet in self.bullets:
            bullet.move()

    def move(self, dx, dy):
        self.velocity.x = dx
        self.velocity.y = dy
        self.velocity.normalise()
        self.velocity *= self.speed
        self.position += self.velocity

    def render(self, window):
        for bullet in self.bullets:
            bullet.render(window)
