def flee_map(game_map, threats, coefficient=-1.2):
    """Brogue's 'safety map': invert a distance map and let it settle.

    Multiplying by a negative number turns 'far from the threat' into
    'downhill'. Re-relaxing the field afterwards makes cornered
    creatures run past the threat toward the far exits instead of
    pressing into the nearest dead end.

    The relaxation is one Dijkstra pass: every cell starts with its
    inverted value, and the lowest cells are settled first, each one
    offering its neighbours "my value + 1". Earlier versions swept the
    whole map again and again until nothing changed, which was fine on
    small maps and far too slow on large ones (see Chapter 19).
    """
    field = {cell: d * coefficient for cell, d in dijkstra_map(game_map, threats).items()}
    heap = [(value, cell) for cell, value in field.items()]
    heapq.heapify(heap)
    while heap:
        value, (x, y) = heapq.heappop(heap)
        if value > field[(x, y)]:
            continue                       # an outdated heap entry
        for dx, dy in NEIGHBOURS:
            nxt = (x + dx, y + dy)
            if nxt in field and value + 1 < field[nxt]:
                field[nxt] = value + 1
                heapq.heappush(heap, (value + 1, nxt))
    return field
