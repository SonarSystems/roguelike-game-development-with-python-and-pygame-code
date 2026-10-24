def dijkstra_map(game_map, goals):
    """Distance (in steps) from every walkable cell to the nearest goal.

    Returns a dict {(x, y): distance}. Cells that can't reach any goal
    are left out.
    """
    distances = {goal: 0 for goal in goals}
    frontier = list(goals)
    while frontier:
        next_frontier = []
        for x, y in frontier:
            for dx, dy in NEIGHBOURS:
                nxt = (x + dx, y + dy)
                if nxt not in distances and game_map.is_walkable(*nxt):
                    distances[nxt] = distances[(x, y)] + 1
                    next_frontier.append(nxt)
        frontier = next_frontier
    return distances
