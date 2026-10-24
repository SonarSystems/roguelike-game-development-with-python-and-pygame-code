class HostileEnemy(BaseAI):
    """Hunt the player with A*; head for where they were last seen."""

    def __init__(self, entity):
        super().__init__(entity)
        self.last_seen = None

    def decide(self, engine):
        me, player = self.entity, engine.player
        if self.can_see_player(engine):
            self.last_seen = (player.x, player.y)
        if self.last_seen is None:
            return self.wander()
        if me.distance_to(*self.last_seen) <= 1 and self.last_seen == (player.x, player.y):
            return BumpAction(me, player.x - me.x, player.y - me.y)   # adjacent: attack
        # Other monsters block the path, so the pack spreads out around
        # the player instead of queueing in a corridor.
        blocked = {(e.x, e.y) for e in engine.entities if e.blocks_movement and e is not me}
        path = astar(engine.game_map, (me.x, me.y), self.last_seen, blocked)
        if not path:
            return WaitAction(me)
        if path[0] == self.last_seen and self.last_seen != (player.x, player.y):
            self.last_seen = None   # reached the spot; the trail has gone cold
        nx, ny = path[0]
        return BumpAction(me, nx - me.x, ny - me.y)
