class EquipAction(Action):
    """Equip or remove an item from the inventory. Changing gear takes a turn."""

    def __init__(self, entity, item):
        super().__init__(entity)
        self.item = item

    def perform(self, engine):
        self.entity.equipment.toggle(self.item, engine)
