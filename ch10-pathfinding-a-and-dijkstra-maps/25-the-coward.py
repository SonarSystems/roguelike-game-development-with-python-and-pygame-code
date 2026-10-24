class CowardlyEnemy(BaseAI):
    """Run away from the player along a Dijkstra flee map when they get close."""

    def __init__(self, entity, panic_distance=6):
        super().__init__(entity)
        self.panic_distance = panic_distance

    def decide(self, engine):
        me, player = self.entity, engine.player
        if not self.can_see_player(engine) or me.distance_to(player.x, player.y) > self.panic_distance:
            return self.wander()
        field = flee_map(engine.game_map, [(player.x, player.y)])
        blocked = {(e.x, e.y) for e in engine.entities if e.blocks_movement and e is not me}
        step = downhill_step(field, me.x, me.y, blocked)
        if step is None:
            return WaitAction(me)   # cornered
        return MovementAction(me, step[0] - me.x, step[1] - me.y)
