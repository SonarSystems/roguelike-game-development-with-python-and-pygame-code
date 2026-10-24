class ConfusionConsumable(Consumable):
    """Confuses one target creature for a few turns."""

    def __init__(self, turns):
        super().__init__()
        self.turns = turns

    def get_action(self, user, engine):
        from ember.input_handlers import SingleTargetHandler
        engine.log("Select a target for confusion.", settings.MAGIC_BLUE)
        engine.event_handler = SingleTargetHandler(
            engine, lambda cell: ItemAction(user, self.entity, cell))
        return None

    def activate(self, user, engine, target=None):
        from ember.ai import ConfusedEnemy
        if target not in engine.game_map.visible:
            raise Impossible("You can't target a place you can't see.")
        creature = next((e for e in engine.entities
                         if e.is_alive and (e.x, e.y) == target), None)
        if creature is None:
            raise Impossible("There is no one there to confuse.")
        if creature is user:
            raise Impossible("You can't confuse yourself!")
        engine.log(f"The {creature.name} looks dazed and starts to stumble around.",
                   settings.MAGIC_BLUE)
        creature.ai = ConfusedEnemy(creature, creature.ai, self.turns)
        self.consume(user)
