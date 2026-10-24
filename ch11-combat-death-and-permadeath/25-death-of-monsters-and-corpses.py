def run_monster_turns(self):
    """The energy system: every monster gains its speed in energy and
    acts once for every ACTION_COST it has banked. Fast monsters act
    more than once per player turn; slow ones skip turns."""
    for entity in list(self.entities):
        if entity.ai is None:
            continue
        entity.energy += entity.speed
        while entity.energy >= ACTION_COST and entity.ai is not None:
            entity.energy -= ACTION_COST
            entity.ai.decide(self).perform(self)
            if not self.player.is_alive:
                return
