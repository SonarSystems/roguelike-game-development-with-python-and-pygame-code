# file: ember/entity.py
"""Entities: anything that occupies a grid cell and isn't part of the map."""


class Entity:
    def __init__(self, x, y, char, color, name, blocks_movement=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
