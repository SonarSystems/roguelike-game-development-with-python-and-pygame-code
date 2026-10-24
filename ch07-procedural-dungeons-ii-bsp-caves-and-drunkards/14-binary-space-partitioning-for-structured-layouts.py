import random

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
