for _ in range(max_rooms):
    room_w = rng.randint(room_min_size, room_max_size)
    room_h = rng.randint(room_min_size, room_max_size)
    x = rng.randint(0, width - room_w - 1)
    y = rng.randint(0, height - room_h - 1)
    new_room = RectangularRoom(x, y, room_w, room_h)

    if any(new_room.intersects(other) for other in rooms):
        continue  # overlaps an existing room: try again
