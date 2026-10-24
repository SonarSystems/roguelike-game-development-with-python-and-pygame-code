class ItemAction(Action):
    """Use an item from the inventory, optionally on a target cell."""

    def __init__(self, entity, item, target=None):
        super().__init__(entity)
        self.item = item
        self.target = target

    def perform(self, engine):
        self.item.consumable.activate(self.entity, engine, self.target)
