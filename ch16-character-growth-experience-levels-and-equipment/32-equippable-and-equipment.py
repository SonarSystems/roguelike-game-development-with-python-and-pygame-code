class Equippable:
    """Something that can be worn or wielded in a slot."""

    def __init__(self, slot, power_bonus=0, defense_bonus=0):
        self.entity = None
        self.slot = slot              # "weapon" or "armor"
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
