def add_xp(self, amount, engine):
    if amount <= 0:
        return
    self.current_xp += amount
    engine.log(f"You gain {amount} experience points.")
    if self.requires_level_up:
        engine.log(f"You advance to level {self.current_level + 1}!", settings.LEVEL_UP)
