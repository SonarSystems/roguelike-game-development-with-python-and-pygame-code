# file: ember/main.py
"""Entry point: build the game, then run the loop."""
import random
import sys

import pygame

from ember import settings
from ember.engine import Engine
from ember.entity import Entity
from ember.procgen import GENERATORS, generate_level
from ember.render import GlyphRenderer

MAP_HEIGHT = settings.GRID_HEIGHT - 2   # leave two rows for the status line
KINDS = sorted(GENERATORS)


def new_game(seed, kind):
    game_map, rooms = generate_level(seed, settings.GRID_WIDTH, MAP_HEIGHT, kind)
    start_x, start_y = rooms[0].center
    assert len(game_map.reachable_from(start_x, start_y)) == len(game_map.floor_cells())
    player = Entity(start_x, start_y, "@", settings.EMBER, "Player", blocks_movement=True)
    return Engine(game_map, player, [player])


def main():
    # python -m ember [seed] [rooms|bsp|cave|drunkard]
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else random.randrange(1_000_000)
    kind = sys.argv[2] if len(sys.argv) > 2 else "rooms"

    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    glyphs = GlyphRenderer()
    engine = new_game(seed, kind)

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    seed = random.randrange(1_000_000)       # R: new seed
                    engine = new_game(seed, kind)
                    continue
                if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                    kind = KINDS[(KINDS.index(kind) + 1) % len(KINDS)]  # G: next generator
                    engine = new_game(seed, kind)
                    continue
                engine.handle_event(event)
            engine.render(screen, glyphs)
            glyphs.draw_text(screen, f"Seed: {seed}   Generator: {kind}   (R new seed, G next generator)",
                             14, settings.GRID_HEIGHT - 1, settings.WHITE)
            pygame.display.flip()
            clock.tick(settings.FPS)
    except SystemExit:
        pygame.quit()


if __name__ == "__main__":
    main()
