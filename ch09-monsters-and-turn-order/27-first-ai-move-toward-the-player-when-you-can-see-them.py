import random

class HostileEnemy(BaseAI):
    """Chase the player in a straight line when it can see them; wander otherwise."""

    def decide(self, engine):
        me, player = self.entity, engine.player
        # Field of view is symmetric for our purposes: if the player can
        # see this cell, the monster standing on it can see the player.
        if (me.x, me.y) in engine.game_map.visible:
            dx = (player.x > me.x) - (player.x < me.x)   # -1, 0 or 1
            dy = (player.y > me.y) - (player.y < me.y)
            return BumpAction(me, dx, dy)
        if random.random() < 0.5:
            dx, dy = random.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
            return BumpAction(me, dx, dy)
        return WaitAction(me)
