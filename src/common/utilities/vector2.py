import math


class Vector2:
    def __init__(self, x=0.0, y=0.0):
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

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def get_tuple(self):
        return (self.x, self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        return math.sqrt(self.dot(self))

    def normalise(self):
        magnitude = self.magnitude()

        if magnitude == 0:
            return

        self.x /= magnitude
        self.y /= magnitude

    def normalised(self):
        magnitude = self.magnitude()

        if magnitude == 0:
            return self

        return Vector2(self.x / magnitude, self.y / magnitude)

    @staticmethod
    def get_direction(a, b):
        return (b - a).normalised()

    @staticmethod
    def get_distance(a, b):
        return (b - a).magnitude()
