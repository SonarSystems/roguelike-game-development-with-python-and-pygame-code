# file: ember/fov.py
"""Field of view by recursive shadowcasting.

The area around the viewer is split into eight triangular octants. Each
octant is scanned row by row moving outward. A run of opaque cells casts
a shadow: the scan of the rows behind it continues only through the
gaps, which we track as a range of slopes. When a row starts a new
shadow, we recurse to scan the still-lit part beyond it and then carry
on with the rest of the row.
"""

# Each octant maps the scan's local (dx, dy) onto the map's (x, y) axes:
# x = ox + dx * xx + dy * xy,  y = oy + dx * yx + dy * yy
OCTANTS = (
    (1, 0, 0, 1), (0, 1, 1, 0), (0, -1, 1, 0), (-1, 0, 0, 1),
    (-1, 0, 0, -1), (0, -1, -1, 0), (0, 1, -1, 0), (1, 0, 0, -1),
)


def compute_fov(is_transparent, origin_x, origin_y, radius):
    """Return the set of (x, y) cells visible from the origin.

    `is_transparent(x, y)` must return False for walls and for cells
    outside the map.
    """
    visible = {(origin_x, origin_y)}
    for xx, xy, yx, yy in OCTANTS:
        _cast_light(is_transparent, visible, origin_x, origin_y, radius,
                    1, 1.0, 0.0, xx, xy, yx, yy)
    return visible


def _cast_light(is_transparent, visible, ox, oy, radius, row, start_slope, end_slope,
                xx, xy, yx, yy):
    if start_slope < end_slope:
        return
    radius_sq = radius * radius
    for distance in range(row, radius + 1):
        blocked = False
        next_start = start_slope
        dy = -distance
        for dx in range(-distance, 1):
            # Slopes of the cell's left and right edges, seen from the origin.
            left_slope = (dx - 0.5) / (dy + 0.5)
            right_slope = (dx + 0.5) / (dy - 0.5)
            if start_slope < right_slope:
                continue            # cell is before the lit range
            if end_slope > left_slope:
                break               # cell is past the lit range
            x = ox + dx * xx + dy * xy
            y = oy + dx * yx + dy * yy
            if dx * dx + dy * dy <= radius_sq:
                visible.add((x, y))
            if blocked:
                if not is_transparent(x, y):
                    next_start = right_slope      # still in shadow
                    continue
                blocked = False                   # shadow ends: resume
                start_slope = next_start
            elif not is_transparent(x, y) and distance < radius:
                blocked = True                    # shadow starts here
                _cast_light(is_transparent, visible, ox, oy, radius, distance + 1,
                            start_slope, left_slope, xx, xy, yx, yy)
                next_start = right_slope
        if blocked:
            break
