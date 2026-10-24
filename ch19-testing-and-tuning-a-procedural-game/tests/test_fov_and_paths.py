# file: tests/test_fov_and_paths.py
"""Field of view and pathfinding on small hand-made maps."""
from ember import tiles
from ember.fov import compute_fov
from ember.game_map import GameMap
from ember.pathfinding import astar, dijkstra_map


def open_room(width=11, height=11):
    """A room with a wall border and nothing inside."""
    game_map = GameMap(width, height)
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            game_map.set_tile(x, y, tiles.FLOOR)
    return game_map


def test_fov_sees_the_whole_open_room():
    game_map = open_room()
    visible = compute_fov(game_map.is_transparent, 5, 5, radius=10)
    for x, y in game_map.floor_cells():
        assert (x, y) in visible


def test_a_pillar_casts_a_shadow():
    game_map = open_room()
    game_map.set_tile(6, 5, tiles.WALL)          # pillar just east of the viewer
    visible = compute_fov(game_map.is_transparent, 5, 5, radius=10)
    assert (6, 5) in visible                     # you see the pillar itself...
    assert (8, 5) not in visible                 # ...but not what's behind it
    assert (5, 8) in visible                     # other directions are unaffected


def test_fov_respects_the_radius():
    game_map = open_room(31, 31)
    visible = compute_fov(game_map.is_transparent, 15, 15, radius=4)
    assert (15, 19) in visible and (15, 20) not in visible


def test_astar_finds_a_shortest_path():
    game_map = open_room()
    path = astar(game_map, (1, 1), (9, 9))
    assert path[-1] == (9, 9)
    assert len(path) == 8                        # diagonal steps: 8 moves


def test_astar_goes_around_a_wall():
    game_map = open_room()
    for y in range(1, 9):                        # wall with a gap at the bottom
        game_map.set_tile(5, y, tiles.WALL)
    path = astar(game_map, (2, 2), (8, 2))
    assert path and path[-1] == (8, 2)
    assert all(game_map.is_walkable(x, y) for x, y in path)
    assert any(y == 9 for _, y in path)          # it had to use the gap


def test_astar_returns_empty_when_unreachable():
    game_map = open_room()
    for y in range(1, 10):                       # wall with no gap
        game_map.set_tile(5, y, tiles.WALL)
    assert astar(game_map, (2, 2), (8, 2)) == []


def test_dijkstra_distances_grow_by_one():
    game_map = open_room()
    field = dijkstra_map(game_map, [(5, 5)])
    assert field[(5, 5)] == 0
    assert field[(6, 6)] == 1
    assert field[(9, 5)] == 4
