# file: ember/main.py
"""Entry point: build the game, then run the loop."""
import random
import sys

import pygame

from ember import entity_factories, settings
from ember.engine import Engine
from ember.input_handlers import NewGame
from ember.procgen import generate_level
from ember.render import GlyphRenderer
from ember.spawner import spawn_monsters

MONSTERS_PER_LEVEL = 14


def new_game(seed, kind=None):
    game_map, rooms = generate_level(seed, settings.MAP_WIDTH, settings.MAP_HEIGHT, kind)
    start = rooms[0].center
    player = entity_factories.player(*start)
    monsters = spawn_monsters(seed, game_map, start, MONSTERS_PER_LEVEL)
    engine = Engine(game_map, player, monsters + [player])
    engine.log(f"Welcome to Ember Depths. (Seed {seed})", settings.EMBER)
    return engine


def main():
    # python -m ember [seed] [rooms|bsp|cave|drunkard]
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else random.randrange(1_000_000)
    kind = sys.argv[2] if len(sys.argv) > 2 else None

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
                try:
                    engine.handle_event(event)
                except NewGame:
                    seed = random.randrange(1_000_000)
                    engine = new_game(seed, kind)
            engine.render(screen, glyphs)
            pygame.display.flip()
            clock.tick(settings.FPS)
    except SystemExit:
        pygame.quit()


if __name__ == "__main__":
    main()
