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
