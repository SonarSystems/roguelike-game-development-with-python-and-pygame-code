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
