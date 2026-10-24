# file: ember/main.py
"""Entry point: the title screen, then the game loop.

The loops are `async` so the same code runs on the desktop and in a web
browser via pygbag, which needs every loop to hand control back to the
browser once per frame (`await asyncio.sleep(0)`).
"""
import asyncio
import random
import sys

import pygame

from ember import entity_factories, settings
from ember.engine import Engine
from ember.game_world import GameWorld
from ember.input_handlers import GameOverEventHandler, NewGame
from ember.main_menu import CONTINUE, NEW_GAME, run_main_menu
from ember.render import GlyphRenderer
from ember.savegame import load_game, save_game


def new_game(seed, kind=None):
    """Start a fresh run. `kind` is accepted for compatibility but every
    floor now picks its own generator from its seed."""
    player = entity_factories.player(0, 0)
    engine = Engine(GameWorld(seed), player)
    engine.log(f"Welcome to Ember Depths. (Seed {seed})", settings.EMBER)
    engine.log("Find the stairs (>) and reach depth 10 for the Ember Crown.", settings.EMBER)
    return engine


async def play(engine, screen, glyphs, clock):
    """Run one game until the player quits or starts a new run."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit()
            engine.handle_event(event)
        dt = clock.tick(settings.FPS) / 1000.0   # seconds since the last frame
        engine.render(screen, glyphs, dt)
        pygame.display.flip()
        await asyncio.sleep(0)


async def main_async():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    glyphs = GlyphRenderer()
    seed_arg = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None

    error = None
    while True:
        choice = await run_main_menu(screen, glyphs, clock, error)
        error = None
        if choice == NEW_GAME:
            engine = new_game(seed_arg if seed_arg is not None else random.randrange(1_000_000))
        elif choice == CONTINUE:
            try:
                engine = load_game()
            except (OSError, ValueError, KeyError) as exc:
                error = f"Couldn't load the saved game: {exc}"
                continue
        else:
            break
        try:
            await play(engine, screen, glyphs, clock)
        except NewGame:
            continue                      # back to the title screen
        except SystemExit:
            # Quitting mid-run saves it; a finished run has nothing to save.
            if not isinstance(engine.event_handler, GameOverEventHandler):
                save_game(engine)
            break
    pygame.quit()


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
