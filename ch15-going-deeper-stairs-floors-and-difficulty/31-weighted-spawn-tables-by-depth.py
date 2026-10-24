def table_for_depth(chances, depth):
    weights = {}
    for start_depth in sorted(chances):
        if start_depth > depth:
            break
        for factory, weight in chances[start_depth]:
            weights[factory] = weight
    return list(weights), list(weights.values())
