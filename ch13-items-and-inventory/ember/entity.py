# file: ember/entity.py
"""Entities: anything that occupies a grid cell and isn't part of the map."""

NORMAL_SPEED = 100   # energy gained per turn by a normal-speed creature


class Entity:
    def __init__(self, x, y, char, color, name, blocks_movement=False,
                 speed=NORMAL_SPEED, ai=None, fighter=None, render_order=1,
                 consumable=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.speed = speed      # how much energy this entity gains each turn
        self.energy = 0         # spent at ACTION_COST per action
        self.ai = ai            # None for the player, objects and corpses
        self.render_order = render_order   # higher numbers are drawn on top
        # Optional components: each one knows which entity owns it.
        self.fighter = fighter
        self.consumable = consumable      # set on items
        self.inventory = inventory        # set on things that carry items
        for component in (fighter, consumable, inventory):
            if component is not None:
                component.entity = self

    @property
    def is_alive(self):
        return self.fighter is not None and self.fighter.is_alive

    @property
    def is_item(self):
        return self.consumable is not None

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def distance_to(self, x, y):
        """Chebyshev distance: the number of king-moves (diagonals allowed)."""
        return max(abs(self.x - x), abs(self.y - y))
