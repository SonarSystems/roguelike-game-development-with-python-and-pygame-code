import pygame
import sys

def main():
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    first_seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    pygame.init()
    pygame.display.set_mode((1, 1))
    results = [play_one(seed) for seed in range(first_seed, first_seed + runs)]

    depths = [r["depth"] for r in results]
    print(f"Runs: {runs}   Wins: {sum(r['won'] for r in results)}")
    print(f"Depth reached: mean {statistics.mean(depths):.1f}, median {statistics.median(depths)}")
    print(f"Turns survived: mean {statistics.mean(r['turns'] for r in results):.0f}")
    print("Deepest floor reached (depth: runs):")
    for depth, count in sorted(Counter(depths).items()):
        print(f"  {depth:2d}: {'#' * count} {count}")
    killers = Counter(r["killer"] for r in results if r["killer"])
    print("Killed by: " + ", ".join(f"{name} {n}" for name, n in killers.most_common()))
