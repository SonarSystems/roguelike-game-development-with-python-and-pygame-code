# file: scripts/autoplay.py
"""A simple bot that plays Ember Depths headlessly, many times, and reports statistics.

It plays through the same Engine and input handlers a human uses, by sending
real key events, so it tests the whole game, not a copy of it.

Usage: python scripts/autoplay.py [runs] [first_seed]
"""
import os
import statistics
import sys
from collections import Counter, deque

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402

from ember.input_handlers import (GameOverEventHandler, LevelUpEventHandler,  # noqa: E402
                                  MainGameEventHandler)
from ember.main import new_game  # noqa: E402

KEYS = {(0, -1): pygame.K_k, (0, 1): pygame.K_j, (-1, 0): pygame.K_h, (1, 0): pygame.K_l,
        (-1, -1): pygame.K_y, (1, -1): pygame.K_u, (-1, 1): pygame.K_b, (1, 1): pygame.K_n}
MAX_TURNS = 3000


def press(engine, key, unicode=""):
    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=key, mod=0, unicode=unicode,
                                           scancode=0))


def first_step(engine, targets):
    """Breadth-first search to the nearest target; return the first move."""
    gm, p = engine.game_map, engine.player
    start = (p.x, p.y)
    previous = {start: None}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        if cell in targets and cell != start:
            while previous[cell] != start:
                cell = previous[cell]
            return cell[0] - start[0], cell[1] - start[1]
        for d in KEYS:
            nxt = (cell[0] + d[0], cell[1] + d[1])
            if nxt not in previous and gm.is_walkable(*nxt):
                previous[nxt] = cell
                queue.append(nxt)
    return None


def take_turn(engine):
    player = engine.player
    if isinstance(engine.event_handler, LevelUpEventHandler):
        press(engine, pygame.K_a)                      # always take +20 HP
        return
    if not isinstance(engine.event_handler, MainGameEventHandler):
        press(engine, pygame.K_ESCAPE)                 # close any menu
        return
    fighter = player.fighter
    potions = [i for i in player.inventory.items if i.name == "Health Potion"]
    if fighter.hp <= fighter.max_hp * 0.4 and potions:
        press(engine, pygame.K_i)
        press(engine, pygame.K_a + player.inventory.items.index(potions[0]))
        return
    crown = [i for i in player.inventory.items if i.name == "Ember Crown"]
    if crown:
        press(engine, pygame.K_i)
        press(engine, pygame.K_a + player.inventory.items.index(crown[0]))
        return
    for monster in engine.entities:                    # fight anything adjacent
        if monster.ai is not None and player.distance_to(monster.x, monster.y) == 1:
            press(engine, KEYS[(monster.x - player.x, monster.y - player.y)])
            return
    here = [e for e in engine.entities if e.is_item and (e.x, e.y) == (player.x, player.y)]
    if here and not player.inventory.is_full:
        press(engine, pygame.K_g)
        return
    gm = engine.game_map
    if gm.tiles[player.x][player.y].glyph == ">":
        press(engine, pygame.K_PERIOD, ">")
        return
    items = {(e.x, e.y) for e in engine.entities
             if e.is_item and (e.x, e.y) in gm.visible}
    stairs = {(x, y) for x, y in gm.explored if gm.tiles[x][y].glyph == ">"}
    unexplored = {c for c in gm.floor_cells() if c not in gm.explored}
    for targets in (items, stairs, unexplored):
        step = first_step(engine, targets)
        if step:
            press(engine, KEYS[step])
            return
    press(engine, pygame.K_PERIOD)                     # nothing to do: wait


def play_one(seed):
    engine = new_game(seed)
    while engine.turn < MAX_TURNS and not isinstance(engine.event_handler, GameOverEventHandler):
        before = engine.turn, len(engine.player.inventory.items), type(engine.event_handler)
        take_turn(engine)
        if (engine.turn, len(engine.player.inventory.items), type(engine.event_handler)) == before:
            press(engine, pygame.K_PERIOD)             # guarantee progress
    won = type(engine.event_handler).__name__ == "VictoryEventHandler"
    killer = engine.message_log.messages[-2].plain_text.split(" attacks")[0] \
        if not won and engine.player.fighter.hp == 0 else None
    return {"seed": seed, "depth": engine.game_world.depth, "turns": engine.turn,
            "level": engine.player.level.current_level, "won": won, "killer": killer}


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


if __name__ == "__main__":
    main()
