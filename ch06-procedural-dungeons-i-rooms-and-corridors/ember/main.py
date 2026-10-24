# file: ember/main.py
"""Entry point: build the game, then run the loop."""
import random
import sys

import pygame

from ember import settings
from ember.engine import Engine
from ember.entity import Entity
from ember.procgen import generate_rooms_and_corridors
from ember.render import GlyphRenderer

MAP_HEIGHT = settings.GRID_HEIGHT - 2   # leave two rows for the status line


def new_game(seed):
    game_map, rooms = generate_rooms_and_corridors(seed, settings.GRID_WIDTH, MAP_HEIGHT)
    start_x, start_y = rooms[0].center
    # Sanity check: every floor cell must be reachable from the start.
    assert len(game_map.reachable_from(start_x, start_y)) == len(game_map.floor_cells())
    player = Entity(start_x, start_y, "@", settings.EMBER, "Player", blocks_movement=True)
    return Engine(game_map, player, [player])


def main():
    # Run with `python -m ember 1234` to replay a particular dungeon.
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else random.randrange(1_000_000)

    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(f"{settings.TITLE} (seed {seed})")
    clock = pygame.time.Clock()
    glyphs = GlyphRenderer()
    engine = new_game(seed)

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    seed = random.randrange(1_000_000)   # R: roll a new dungeon
                    pygame.display.set_caption(f"{settings.TITLE} (seed {seed})")
                    engine = new_game(seed)
                    continue
                engine.handle_event(event)
            engine.render(screen, glyphs)
            glyphs.draw_text(screen, f"Seed: {seed}   (R for a new dungeon)", 20,
                             settings.GRID_HEIGHT - 1, settings.WHITE)
            pygame.display.flip()
            clock.tick(settings.FPS)
    except SystemExit:
        pygame.quit()


if __name__ == "__main__":
    main()
