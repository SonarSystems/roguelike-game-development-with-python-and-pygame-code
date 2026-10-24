# file: ember/entity.py
"""Entities: anything that occupies a grid cell and isn't part of the map."""

NORMAL_SPEED = 100   # energy gained per turn by a normal-speed creature


class Entity:
    def __init__(self, x, y, char, color, name, blocks_movement=False,
                 speed=NORMAL_SPEED, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.speed = speed      # how much energy this entity gains each turn
        self.energy = 0         # spent at ACTION_COST per action
        self.ai = ai            # None for the player and for objects

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def distance_to(self, x, y):
        """Chebyshev distance: the number of king-moves (diagonals allowed)."""
        return max(abs(self.x - x), abs(self.y - y))
