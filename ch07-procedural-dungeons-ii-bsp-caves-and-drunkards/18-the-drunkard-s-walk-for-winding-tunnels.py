import random

def generate_drunkard(seed, width, height, floor_fraction=0.4):
    rng = random.Random(seed)
    game_map = GameMap(width, height)
    x, y = width // 2, height // 2
    target = int((width - 2) * (height - 2) * floor_fraction)
    carved = 0
    while carved < target:
        if not game_map.tiles[x][y].walkable:
            game_map.set_tile(x, y, tiles.FLOOR)
            carved += 1
        dx, dy = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        # Stay off the outer border so the map stays enclosed.
        x = min(max(1, x + dx), width - 2)
        y = min(max(1, y + dy), height - 2)
    centre = (width // 2, height // 2)
    return game_map, [RectangularRoom(centre[0] - 1, centre[1] - 1, 2, 2)]
