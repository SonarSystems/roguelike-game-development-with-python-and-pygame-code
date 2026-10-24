# file: ember/ai.py
"""Monster brains. Each AI decides which Action its entity takes this turn."""
import random

from ember.actions import BumpAction, MovementAction, WaitAction
from ember.pathfinding import astar, downhill_step, flee_map


class BaseAI:
    def __init__(self, entity):
        self.entity = entity

    def decide(self, engine):
        """Return the Action this entity should perform."""
        raise NotImplementedError()

    def can_see_player(self, engine):
        # Field of view is symmetric for our purposes: if the player can
        # see this cell, the monster standing on it can see the player.
        return (self.entity.x, self.entity.y) in engine.game_map.visible

    def wander(self):
        if random.random() < 0.5:
            dx, dy = random.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
            return MovementAction(self.entity, dx, dy)
        return WaitAction(self.entity)


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


class ConfusedEnemy(BaseAI):
    """Stagger in random directions for a few turns, then go back to the old AI.

    It still uses BumpAction, so a confused monster can hit anything it
    stumbles into, including other monsters.
    """

    DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))

    def __init__(self, entity, previous_ai, turns_remaining):
        super().__init__(entity)
        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def decide(self, engine):
        if self.turns_remaining <= 0:
            engine.log(f"The {self.entity.name} is no longer confused.")
            self.entity.ai = self.previous_ai
            return WaitAction(self.entity)
        self.turns_remaining -= 1
        dx, dy = random.choice(self.DIRECTIONS)
        return BumpAction(self.entity, dx, dy)
