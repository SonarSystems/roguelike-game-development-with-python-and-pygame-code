import random

def generate_level(seed, width, height, kind=None):
    """Pick a generator (randomly from the seed unless `kind` is given)."""
    if kind is None:
        kind = random.Random(seed).choice(sorted(GENERATORS))
    return GENERATORS[kind](seed, width, height)
