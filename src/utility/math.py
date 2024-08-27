import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, t):
        return Vector2(self.x * t, self.y * t)

    def __truediv__(self, t):
        return Vector2(self.x / t, self.y / t)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        return math.sqrt(self.dot(self))

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def normalise(self):
        magnitude = self.magnitude()

        if magnitude == 0:
            return

        self.x /= magnitude
        self.y /= magnitude
