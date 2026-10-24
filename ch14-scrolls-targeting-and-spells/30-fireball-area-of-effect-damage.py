class FireballDamageConsumable(Consumable):
    """Damages every creature within a radius of the chosen cell, the user included."""

    def __init__(self, damage, radius):
        super().__init__()
        self.damage = damage
        self.radius = radius

    def get_action(self, user, engine):
        from ember.input_handlers import AreaTargetHandler
        engine.log("Select a target location for the fireball.", settings.MAGIC_BLUE)
        engine.event_handler = AreaTargetHandler(
            engine, self.radius, lambda cell: ItemAction(user, self.entity, cell))
        return None

    def activate(self, user, engine, target=None):
        if target not in engine.game_map.visible:
            raise Impossible("You can't target a place you can't see.")
        hit = [e for e in engine.entities
               if e.is_alive and e.distance_to(*target) <= self.radius]
        if not hit:
            raise Impossible("There is nothing there to burn.")
        for creature in hit:
            engine.log(f"The {creature.name} is engulfed in flames for {self.damage} damage!",
                       settings.FIRE)
            creature.fighter.take_damage(self.damage, engine)
        self.consume(user)
