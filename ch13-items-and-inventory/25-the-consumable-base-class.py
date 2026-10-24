class Consumable:
    def __init__(self):
        self.entity = None      # the item Entity this component belongs to

    def activate(self, user, engine, target=None):
        """Apply the effect. Raise Impossible if it can't be used now."""
        raise NotImplementedError()

    def consume(self, user):
        """Remove the used item from its owner's inventory."""
        user.inventory.items.remove(self.entity)
