def flee_map(game_map, threats, coefficient=-1.2):
    """Brogue's 'safety map': invert a distance map and let it settle.

    Multiplying by a negative number turns 'far from the threat' into
    'downhill'. Re-relaxing the field afterwards makes cornered
    creatures run past the threat toward the far exits instead of
    pressing into the nearest dead end.
    """
    field = {cell: d * coefficient for cell, d in dijkstra_map(game_map, threats).items()}
    changed = True
    while changed:
        changed = False
        for (x, y), value in field.items():
            best = min((field[(x + dx, y + dy)] for dx, dy in NEIGHBOURS
                        if (x + dx, y + dy) in field), default=value)
            if best + 1 < value:
                field[(x, y)] = best + 1
                changed = True
    return field
