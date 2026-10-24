# file: ember/components.py
"""Components: optional pieces of behaviour an Entity can carry."""
from ember import settings


class Fighter:
    """Hit points and combat stats. Anything that can fight or die has one."""

    def __init__(self, hp, defense, power):
        self.entity = None      # set by the entity that owns this component
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.max_hp))

    @property
    def is_alive(self):
        return self._hp > 0

    def take_damage(self, amount, engine):
        self.hp -= amount
        if not self.is_alive:
            self.die(engine)

    def heal(self, amount):
        """Restore up to `amount` HP; return how much was actually restored."""
        before = self.hp
        self.hp += amount
        return self.hp - before

    def die(self, engine):
        entity = self.entity
        if entity is engine.player:
            engine.log("You die...", settings.DEATH_RED)
            engine.on_player_death()
        else:
            engine.log(f"The {entity.name} dies.", settings.ORANGE)
        entity.char = "%"
        entity.color = settings.CORPSE_RED
        entity.blocks_movement = False
        entity.ai = None
        entity.name = f"remains of {entity.name}"
        entity.render_order = 0      # corpses are drawn underneath the living


class Inventory:
    """A bag of item entities, with a fixed number of slots."""

    def __init__(self, capacity):
        self.entity = None
        self.capacity = capacity
        self.items = []

    @property
    def is_full(self):
        return len(self.items) >= self.capacity
