import random

# All gameplay randomness after map generation comes from here,
# so the same seed and the same keypresses replay the same run.
self.rng = random.Random(game_world.seed)
