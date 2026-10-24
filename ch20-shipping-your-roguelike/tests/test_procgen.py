# file: tests/test_procgen.py
"""Every generator must make a connected, reproducible map."""
import pytest

from ember import settings
from ember.procgen import GENERATORS

KINDS = sorted(GENERATORS)
SEEDS = range(50)


@pytest.mark.parametrize("kind", KINDS)
def test_same_seed_gives_same_map(kind):
    first, _ = GENERATORS[kind](123, settings.MAP_WIDTH, settings.MAP_HEIGHT)
    second, _ = GENERATORS[kind](123, settings.MAP_WIDTH, settings.MAP_HEIGHT)
    assert first.floor_cells() == second.floor_cells()


@pytest.mark.parametrize("kind", KINDS)
@pytest.mark.parametrize("seed", SEEDS)
def test_every_floor_cell_is_reachable(kind, seed):
    game_map, rooms = GENERATORS[kind](seed, settings.MAP_WIDTH, settings.MAP_HEIGHT)
    start = rooms[0].center
    assert game_map.is_walkable(*start)
    assert len(game_map.reachable_from(*start)) == len(game_map.floor_cells())


@pytest.mark.parametrize("kind", KINDS)
def test_the_border_is_solid(kind):
    game_map, _ = GENERATORS[kind](7, settings.MAP_WIDTH, settings.MAP_HEIGHT)
    for x in range(game_map.width):
        assert not game_map.is_walkable(x, 0)
        assert not game_map.is_walkable(x, game_map.height - 1)
    for y in range(game_map.height):
        assert not game_map.is_walkable(0, y)
        assert not game_map.is_walkable(game_map.width - 1, y)
