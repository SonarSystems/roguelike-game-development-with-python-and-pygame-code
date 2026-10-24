# file: ember/components.py
"""Components: optional pieces of behaviour an Entity can carry."""
from ember import settings


class Fighter:
    """Hit points and combat stats. Anything that can fight or die has one."""

    def __init__(self, hp, base_defense, base_power):
        self.entity = None      # set by the entity that owns this component
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.max_hp))

    # Equipment adds to the base stats, so they are computed, not stored.
    @property
    def power(self):
        equipment = self.entity.equipment if self.entity else None
        return self.base_power + (equipment.power_bonus if equipment else 0)

    @property
    def defense(self):
        equipment = self.entity.equipment if self.entity else None
        return self.base_defense + (equipment.defense_bonus if equipment else 0)

    @property
    def is_alive(self):
        return self._hp > 0

    def take_damage(self, amount, engine):
        engine.effects.on_damage(self.entity, amount, self.entity is engine.player)
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
            if entity.level is not None:
                engine.player.level.add_xp(entity.level.xp_given, engine)
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


class Level:
    """Experience and character level.

    The player collects XP; monsters only use `xp_given`, the reward for
    killing them.
    """

    def __init__(self, level=1, xp_given=0, base_xp=200, xp_factor=150):
        self.entity = None
        self.current_level = level
        self.current_xp = 0
        self.xp_given = xp_given
        self.base_xp = base_xp
        self.xp_factor = xp_factor

    @property
    def xp_to_next_level(self):
        return self.base_xp + self.current_level * self.xp_factor

    @property
    def requires_level_up(self):
        return self.current_xp >= self.xp_to_next_level

    def add_xp(self, amount, engine):
        if amount <= 0:
            return
        self.current_xp += amount
        engine.log(f"You gain {amount} experience points.")
        if self.requires_level_up:
            engine.log(f"You advance to level {self.current_level + 1}!", settings.LEVEL_UP)

    def increase_level(self):
        self.current_xp -= self.xp_to_next_level
        self.current_level += 1

    def increase_max_hp(self, amount=20):
        fighter = self.entity.fighter
        fighter.max_hp += amount
        fighter.hp += amount
        self.increase_level()

    def increase_power(self, amount=1):
        self.entity.fighter.base_power += amount
        self.increase_level()

    def increase_defense(self, amount=1):
        self.entity.fighter.base_defense += amount
        self.increase_level()


class Equippable:
    """Something that can be worn or wielded in a slot."""

    def __init__(self, slot, power_bonus=0, defense_bonus=0):
        self.entity = None
        self.slot = slot              # "weapon" or "armor"
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus


class Equipment:
    """What a creature has equipped: one item per slot."""

    def __init__(self):
        self.entity = None
        self.slots = {"weapon": None, "armor": None}

    @property
    def power_bonus(self):
        return sum(item.equippable.power_bonus for item in self.slots.values() if item)

    @property
    def defense_bonus(self):
        return sum(item.equippable.defense_bonus for item in self.slots.values() if item)

    def is_equipped(self, item):
        return item in self.slots.values()

    def toggle(self, item, engine):
        """Equip the item, replacing whatever was in its slot, or remove it."""
        slot = item.equippable.slot
        current = self.slots[slot]
        if current is item:
            self.slots[slot] = None
            engine.log(f"You remove the {item.name}.")
            return
        if current is not None:
            engine.log(f"You remove the {current.name}.")
        self.slots[slot] = item
        engine.log(f"You equip the {item.name}.")
