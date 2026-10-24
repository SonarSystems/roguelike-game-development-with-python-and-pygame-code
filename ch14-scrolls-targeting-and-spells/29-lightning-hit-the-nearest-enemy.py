class LightningDamageConsumable(Consumable):
    """Strikes the closest visible enemy within range. No targeting needed."""

    def __init__(self, damage, maximum_range):
        super().__init__()
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, user, engine, target=None):
        best, best_distance = None, self.maximum_range + 1
        for creature in engine.entities:
            if creature is user or not creature.is_alive:
                continue
            if (creature.x, creature.y) not in engine.game_map.visible:
                continue
            distance = user.distance_to(creature.x, creature.y)
            if distance < best_distance:
                best, best_distance = creature, distance
        if best is None:
            raise Impossible("No enemy is close enough to strike.")
        engine.log(f"A bolt of lightning strikes the {best.name} for {self.damage} damage!",
                   settings.MAGIC_BLUE)
        best.fighter.take_damage(self.damage, engine)
        self.consume(user)
