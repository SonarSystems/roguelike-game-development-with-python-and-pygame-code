# file: ember/pathfinding.py
"""Pathfinding on the dungeon grid: A* for one route, Dijkstra maps for many."""
import heapq

NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


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


def downhill_step(field, x, y, blocked=frozenset()):
    """The neighbouring cell with the lowest value, or None if none is lower."""
    best, best_value = None, field.get((x, y), float("inf"))
    for dx, dy in NEIGHBOURS:
        nxt = (x + dx, y + dy)
        if nxt in field and nxt not in blocked and field[nxt] < best_value:
            best, best_value = nxt, field[nxt]
    return best
