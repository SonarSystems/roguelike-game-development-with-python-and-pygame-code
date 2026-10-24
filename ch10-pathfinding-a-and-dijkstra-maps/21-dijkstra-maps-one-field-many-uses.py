def downhill_step(field, x, y, blocked=frozenset()):
    """The neighbouring cell with the lowest value, or None if none is lower."""
    best, best_value = None, field.get((x, y), float("inf"))
    for dx, dy in NEIGHBOURS:
        nxt = (x + dx, y + dy)
        if nxt in field and nxt not in blocked and field[nxt] < best_value:
            best, best_value = nxt, field[nxt]
    return best
