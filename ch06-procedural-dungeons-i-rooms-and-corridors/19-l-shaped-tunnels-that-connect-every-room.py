import random

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
