import random

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
