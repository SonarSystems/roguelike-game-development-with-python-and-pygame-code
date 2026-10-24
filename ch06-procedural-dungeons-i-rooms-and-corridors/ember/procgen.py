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
