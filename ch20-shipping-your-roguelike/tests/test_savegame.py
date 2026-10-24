# file: tests/test_savegame.py
"""A saved game must load back exactly as it was."""
import pygame

from ember import entity_factories, savegame
from ember.ai import ConfusedEnemy
from ember.main import new_game


def press(engine, key):
    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=key, mod=0, unicode="", scancode=0))


def snapshot(engine):
    return [(e.name, e.x, e.y, e.fighter.hp if e.fighter else None, type(e.ai).__name__)
            for e in engine.entities]


def test_round_trip(tmp_path):
    engine = new_game(5)
    for key in [pygame.K_l] * 6 + [pygame.K_j] * 4:
        press(engine, key)
    monster = next(e for e in engine.entities if e.ai is not None)
    monster.ai = ConfusedEnemy(monster, monster.ai, 4)
    scroll = entity_factories.fireball_scroll(0, 0)
    engine.player.inventory.items.append(scroll)

    path = tmp_path / "save.json"
    savegame.save_game(engine, path)
    loaded = savegame.load_game(path)

    assert snapshot(loaded) == snapshot(engine)
    assert loaded.turn == engine.turn
    assert loaded.game_map.explored == engine.game_map.explored
    assert [i.name for i in loaded.player.inventory.items] == \
        [i.name for i in engine.player.inventory.items]
    assert loaded.player.equipment.slots["weapon"].name == "Dagger"


def test_same_seed_and_keys_replay_the_same_run():
    keys = [pygame.K_l, pygame.K_l, pygame.K_j, pygame.K_h] * 15
    runs = []
    for _ in range(2):
        engine = new_game(77)
        for key in keys:
            press(engine, key)
        runs.append(snapshot(engine))
    assert runs[0] == runs[1]


def test_loaded_game_continues_identically(tmp_path):
    keys = [pygame.K_l, pygame.K_j, pygame.K_h, pygame.K_k] * 10
    original = new_game(31)
    for key in keys[:20]:
        press(original, key)
    path = tmp_path / "save.json"
    savegame.save_game(original, path)
    loaded = savegame.load_game(path)
    for key in keys[20:]:
        press(original, key)
        press(loaded, key)
    assert snapshot(loaded) == snapshot(original)
