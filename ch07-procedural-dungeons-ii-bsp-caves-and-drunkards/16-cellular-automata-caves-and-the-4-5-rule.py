import random

def generate_cave(seed, width, height, wall_chance=0.45, steps=5):
    rng = random.Random(seed)
    # True = wall. Start from noise, keeping a solid border.
    cells = [[x in (0, width - 1) or y in (0, height - 1) or rng.random() < wall_chance
              for y in range(height)] for x in range(width)]
    for _ in range(steps):
        # The 4-5 rule: a cell becomes wall if 5 or more of the 9 cells
        # in its 3x3 block (itself included) are walls.
        cells = [[count_walls(cells, x, y, width, height) >= 5
                  for y in range(height)] for x in range(width)]
    game_map = GameMap(width, height)
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            if not cells[x][y]:
                game_map.set_tile(x, y, tiles.FLOOR)
    region = keep_largest_region(game_map)
    start = min(region, key=lambda c: (c[0] - width // 2) ** 2 + (c[1] - height // 2) ** 2)
    return game_map, [RectangularRoom(start[0] - 1, start[1] - 1, 2, 2)]
