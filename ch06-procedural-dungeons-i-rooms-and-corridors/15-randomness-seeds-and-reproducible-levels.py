import random
import sys

seed = int(sys.argv[1]) if len(sys.argv) > 1 else random.randrange(1_000_000)
