# file: ember/procgen.py
"""Procedural generation: building a new dungeon level from a seed."""
import random

from ember import tiles
from ember.game_map import GameMap


class RectangularRoom:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self):
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    def inner_cells(self):
        """Every floor cell inside the room (the outer ring stays wall)."""
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                yield x, y

    def intersects(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1
                and self.y1 <= other.y2 and self.y2 >= other.y1)


def tunnel_between(rng, start, end):
    """Yield the cells of an L-shaped tunnel from start to end."""
    x1, y1 = start
    x2, y2 = end
    if rng.random() < 0.5:
        corner = (x2, y1)   # horizontal first, then vertical
    else:
        corner = (x1, y2)   # vertical first, then horizontal
    for (ax, ay), (bx, by) in ((start, corner), (corner, end)):
        step_x = 1 if bx >= ax else -1
        step_y = 1 if by >= ay else -1
        for x in range(ax, bx + step_x, step_x):
            for y in range(ay, by + step_y, step_y):
                yield x, y


def generate_rooms_and_corridors(seed, width, height, max_rooms=30,
                                 room_min_size=6, room_max_size=12):
    """Return (game_map, rooms). The same seed always gives the same map."""
    rng = random.Random(seed)
    game_map = GameMap(width, height)
    rooms = []

    for _ in range(max_rooms):
        room_w = rng.randint(room_min_size, room_max_size)
        room_h = rng.randint(room_min_size, room_max_size)
        x = rng.randint(0, width - room_w - 1)
        y = rng.randint(0, height - room_h - 1)
        new_room = RectangularRoom(x, y, room_w, room_h)

        if any(new_room.intersects(other) for other in rooms):
            continue  # overlaps an existing room: try again

        for cx, cy in new_room.inner_cells():
            game_map.set_tile(cx, cy, tiles.FLOOR)
        if rooms:  # connect to the previous room
            for cx, cy in tunnel_between(rng, rooms[-1].center, new_room.center):
                game_map.set_tile(cx, cy, tiles.FLOOR)
        rooms.append(new_room)

    return game_map, rooms


# ----------------------------------------
# Binary space partitioning (BSP)
# ----------------------------------------
def split_space(rng, x, y, w, h, min_size, leaves):
    """Recursively cut the rectangle (x, y, w, h) in two until it is small."""
    can_split_h = h >= min_size * 2
    can_split_v = w >= min_size * 2
    if not (can_split_h or can_split_v):
        leaves.append((x, y, w, h))
        return
    if can_split_h and can_split_v:
        vertical = w > h if abs(w - h) > 4 else rng.random() < 0.5
    else:
        vertical = can_split_v
    if vertical:
        cut = rng.randint(min_size, w - min_size)
        split_space(rng, x, y, cut, h, min_size, leaves)
        split_space(rng, x + cut, y, w - cut, h, min_size, leaves)
    else:
        cut = rng.randint(min_size, h - min_size)
        split_space(rng, x, y, w, cut, min_size, leaves)
        split_space(rng, x, y + cut, w, h - cut, min_size, leaves)


def generate_bsp(seed, width, height, min_leaf=10):
    rng = random.Random(seed)
    game_map = GameMap(width, height)
    leaves = []
    split_space(rng, 0, 0, width, height, min_leaf, leaves)
    rooms = []
    for lx, ly, lw, lh in leaves:
        room_w = rng.randint(max(4, lw // 2), lw - 2)
        room_h = rng.randint(max(4, lh // 2), lh - 2)
        room_x = lx + rng.randint(0, lw - room_w - 1)
        room_y = ly + rng.randint(0, lh - room_h - 1)
        room = RectangularRoom(room_x, room_y, room_w, room_h)
        for cx, cy in room.inner_cells():
            game_map.set_tile(cx, cy, tiles.FLOOR)
        rooms.append(room)
    # Leaves come out in tree order, so neighbours in the list are
    # neighbours in space: joining each to the next gives short corridors.
    for a, b in zip(rooms, rooms[1:]):
        for cx, cy in tunnel_between(rng, a.center, b.center):
            game_map.set_tile(cx, cy, tiles.FLOOR)
    return game_map, rooms


# ----------------------------------------
# Cellular automata caves
# ----------------------------------------
def count_walls(cells, x, y, width, height):
    """Walls in the 3x3 block centred on (x, y); off-map counts as wall."""
    total = 0
    for nx in range(x - 1, x + 2):
        for ny in range(y - 1, y + 2):
            if not (0 <= nx < width and 0 <= ny < height) or cells[nx][ny]:
                total += 1
    return total


def keep_largest_region(game_map):
    """Fill every floor pocket except the biggest one, so the cave is connected."""
    unvisited = set(game_map.floor_cells())
    best = set()
    while unvisited:
        region = game_map.reachable_from(*next(iter(unvisited)))
        unvisited -= region
        if len(region) > len(best):
            best = region
    for x, y in game_map.floor_cells():
        if (x, y) not in best:
            game_map.set_tile(x, y, tiles.WALL)
    return best


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


# ----------------------------------------
# Drunkard's walk
# ----------------------------------------
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


GENERATORS = {
    "rooms": generate_rooms_and_corridors,
    "bsp": generate_bsp,
    "cave": generate_cave,
    "drunkard": generate_drunkard,
}


def generate_level(seed, width, height, kind=None):
    """Pick a generator (randomly from the seed unless `kind` is given)."""
    if kind is None:
        kind = random.Random(seed).choice(sorted(GENERATORS))
    return GENERATORS[kind](seed, width, height)
