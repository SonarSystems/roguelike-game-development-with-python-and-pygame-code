# file: ember/consumables.py
"""Consumable items: things that are used up when you use them."""
from ember import settings
from ember.exceptions import Impossible


class Consumable:
    def __init__(self):
        self.entity = None      # the item Entity this component belongs to

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
