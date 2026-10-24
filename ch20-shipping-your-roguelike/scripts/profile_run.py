# file: scripts/profile_run.py
"""Profile one bot-played game and print the slowest functions.

Usage: python scripts/profile_run.py [seed]
"""
import cProfile
import os
import pstats
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import autoplay  # noqa: E402  (also sets up headless Pygame)

import pygame  # noqa: E402

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 2
pygame.init()
pygame.display.set_mode((1, 1))
profiler = cProfile.Profile()
profiler.enable()
result = autoplay.play_one(seed)
profiler.disable()
print(f"Seed {seed}: reached depth {result['depth']} in {result['turns']} turns")
stats = pstats.Stats(profiler)
stats.strip_dirs().sort_stats("tottime").print_stats(6)
