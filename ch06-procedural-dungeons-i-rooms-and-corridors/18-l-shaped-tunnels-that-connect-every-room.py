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
