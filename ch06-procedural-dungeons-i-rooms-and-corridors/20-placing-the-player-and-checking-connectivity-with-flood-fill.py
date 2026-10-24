def reachable_from(self, x, y):
    """Flood fill: every walkable cell you can walk to from (x, y)."""
    seen = {(x, y)}
    queue = deque([(x, y)])
    while queue:
        cx, cy = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if (nx, ny) not in seen and self.is_walkable(nx, ny):
                seen.add((nx, ny))
                queue.append((nx, ny))
    return seen
