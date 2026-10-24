def take_damage(self, amount, engine):
    self.hp -= amount
    engine.effects.on_damage(self.entity, amount, self.entity is engine.player)
    ...
