# file: ember/main.py
"""Entry point: build the game, then run the loop."""
import random
import sys

import pygame

from ember import entity_factories, settings
from ember.engine import Engine
from ember.game_world import GameWorld
from ember.input_handlers import NewGame
from ember.render import GlyphRenderer


def new_game(seed, kind=None):
    """Start a fresh run. `kind` is accepted for compatibility but every
    floor now picks its own generator from its seed."""
    player = entity_factories.player(0, 0)
    engine = Engine(GameWorld(seed), player)
    engine.log(f"Welcome to Ember Depths. (Seed {seed})", settings.EMBER)
    engine.log("Find the stairs (>) and reach depth 10 for the Ember Crown.", settings.EMBER)
    return engine


def main():
    # python -m ember [seed]
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else random.randrange(1_000_000)

    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    glyphs = GlyphRenderer()
    engine = new_game(seed)

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit()
                try:
                    engine.handle_event(event)
                except NewGame:
                    seed = random.randrange(1_000_000)
                    engine = new_game(seed)
            engine.render(screen, glyphs)
            pygame.display.flip()
            clock.tick(settings.FPS)
    except SystemExit:
        pygame.quit()


if __name__ == "__main__":
    main()
