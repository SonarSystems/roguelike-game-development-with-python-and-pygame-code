import random

# random.Random.getstate() is (version, tuple of 625 ints, gauss_next).
"rng_state": [engine.rng.getstate()[0], list(engine.rng.getstate()[1]),
              engine.rng.getstate()[2]],
