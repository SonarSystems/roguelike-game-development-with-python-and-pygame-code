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
