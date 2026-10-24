def __init__(self, hp, defense, power):
    self.entity = None      # set by the entity that owns this component
    self.max_hp = hp
    self._hp = hp
    self.defense = defense
    self.power = power
