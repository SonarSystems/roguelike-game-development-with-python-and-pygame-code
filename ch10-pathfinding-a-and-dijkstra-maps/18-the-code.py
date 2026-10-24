def astar(game_map, start, goal, blocked=frozenset()):
    """Return the list of cells from start (exclusive) to goal (inclusive),
    or [] if the goal can't be reached. `blocked` cells are avoided
    unless they are the goal itself."""
    def heuristic(cell):
        # Chebyshev distance: exact when diagonal steps cost the same as straight ones.
        return max(abs(cell[0] - goal[0]), abs(cell[1] - goal[1]))

    open_heap = [(heuristic(start), 0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    while open_heap:
        _, cost, current = heapq.heappop(open_heap)
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        if cost > cost_so_far[current]:
            continue                       # an outdated heap entry
        for dx, dy in NEIGHBOURS:
            nxt = (current[0] + dx, current[1] + dy)
            if not game_map.is_walkable(*nxt):
                continue
            if nxt in blocked and nxt != goal:
                continue
            new_cost = cost + 1
            if new_cost < cost_so_far.get(nxt, float("inf")):
                cost_so_far[nxt] = new_cost
                came_from[nxt] = current
                heapq.heappush(open_heap, (new_cost + heuristic(nxt), new_cost, nxt))
    return []
