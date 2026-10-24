# file: ember/consumables.py
"""Consumable items: things that are used up when you use them."""
from ember import settings
from ember.actions import ItemAction
from ember.exceptions import Impossible


class Consumable:
    def __init__(self):
        self.entity = None      # the item Entity this component belongs to

    def get_action(self, user, engine):
        """What happens when the player picks this item from the inventory.

        Most items are used straight away. Targeted items override this to
        switch the game into a targeting mode first, and return None.
        """
        return ItemAction(user, self.entity)

    def activate(self, user, engine, target=None):
        """Apply the effect. Raise Impossible if it can't be used now."""
        raise NotImplementedError()

    def consume(self, user):
        """Remove the used item from its owner's inventory."""
        user.inventory.items.remove(self.entity)


class HealingConsumable(Consumable):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def activate(self, user, engine, target=None):
        recovered = user.fighter.heal(self.amount)
        if recovered == 0:
            raise Impossible("Your health is already full.")
        engine.log(f"You drink the {self.entity.name} and recover {recovered} HP.",
                   settings.HEALED_GREEN)
        self.consume(user)


class LightningDamageConsumable(Consumable):
    """Strikes the closest visible enemy within range. No targeting needed."""

    def __init__(self, damage, maximum_range):
        super().__init__()
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, user, engine, target=None):
        best, best_distance = None, self.maximum_range + 1
        for creature in engine.entities:
            if creature is user or not creature.is_alive:
                continue
            if (creature.x, creature.y) not in engine.game_map.visible:
                continue
            distance = user.distance_to(creature.x, creature.y)
            if distance < best_distance:
                best, best_distance = creature, distance
        if best is None:
            raise Impossible("No enemy is close enough to strike.")
        engine.log(f"A bolt of lightning strikes the {best.name} for {self.damage} damage!",
                   settings.MAGIC_BLUE)
        best.fighter.take_damage(self.damage, engine)
        self.consume(user)


class ConfusionConsumable(Consumable):
    """Confuses one target creature for a few turns."""

    def __init__(self, turns):
        super().__init__()
        self.turns = turns

    def get_action(self, user, engine):
        from ember.input_handlers import SingleTargetHandler
        engine.log("Select a target for confusion.", settings.MAGIC_BLUE)
        engine.event_handler = SingleTargetHandler(
            engine, lambda cell: ItemAction(user, self.entity, cell))
        return None

    def activate(self, user, engine, target=None):
        from ember.ai import ConfusedEnemy
        if target not in engine.game_map.visible:
            raise Impossible("You can't target a place you can't see.")
        creature = next((e for e in engine.entities
                         if e.is_alive and (e.x, e.y) == target), None)
        if creature is None:
            raise Impossible("There is no one there to confuse.")
        if creature is user:
            raise Impossible("You can't confuse yourself!")
        engine.log(f"The {creature.name} looks dazed and starts to stumble around.",
                   settings.MAGIC_BLUE)
        creature.ai = ConfusedEnemy(creature, creature.ai, self.turns)
        self.consume(user)


class FireballDamageConsumable(Consumable):
    """Damages every creature within a radius of the chosen cell, the user included."""

    def __init__(self, damage, radius):
        super().__init__()
        self.damage = damage
        self.radius = radius

    def get_action(self, user, engine):
        from ember.input_handlers import AreaTargetHandler
        engine.log("Select a target location for the fireball.", settings.MAGIC_BLUE)
        engine.event_handler = AreaTargetHandler(
            engine, self.radius, lambda cell: ItemAction(user, self.entity, cell))
        return None

    def activate(self, user, engine, target=None):
        if target not in engine.game_map.visible:
            raise Impossible("You can't target a place you can't see.")
        hit = [e for e in engine.entities
               if e.is_alive and e.distance_to(*target) <= self.radius]
        if not hit:
            raise Impossible("There is nothing there to burn.")
        for creature in hit:
            engine.log(f"The {creature.name} is engulfed in flames for {self.damage} damage!",
                       settings.FIRE)
            creature.fighter.take_damage(self.damage, engine)
        self.consume(user)
