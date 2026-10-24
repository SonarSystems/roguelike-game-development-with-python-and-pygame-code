class BumpAction(ActionWithDirection):
    """Move if the way is clear; attack if something is standing there."""

    def perform(self, engine):
        if engine.blocking_entity_at(*self.destination):
            return MeleeAction(self.entity, self.dx, self.dy).perform(engine)
        return MovementAction(self.entity, self.dx, self.dy).perform(engine)
