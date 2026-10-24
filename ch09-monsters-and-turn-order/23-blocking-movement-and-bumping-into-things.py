class MeleeAction(ActionWithDirection):
    def perform(self, engine):
        target = engine.blocking_entity_at(*self.destination)
        if target is None:
            return
        # Real combat arrives in Chapter 11; for now, just report the bump.
        engine.message = f"{self.entity.name} bumps into {target.name}."
