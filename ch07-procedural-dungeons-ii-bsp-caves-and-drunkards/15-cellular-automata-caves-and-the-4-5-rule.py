def count_walls(cells, x, y, width, height):
    """Walls in the 3x3 block centred on (x, y); off-map counts as wall."""
    total = 0
    for nx in range(x - 1, x + 2):
        for ny in range(y - 1, y + 2):
            if not (0 <= nx < width and 0 <= ny < height) or cells[nx][ny]:
                total += 1
    return total
