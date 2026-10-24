def split_space(rng, x, y, w, h, min_size, leaves):
    """Recursively cut the rectangle (x, y, w, h) in two until it is small."""
    can_split_h = h >= min_size * 2
    can_split_v = w >= min_size * 2
    if not (can_split_h or can_split_v):
        leaves.append((x, y, w, h))
        return
    if can_split_h and can_split_v:
        vertical = w > h if abs(w - h) > 4 else rng.random() < 0.5
    else:
        vertical = can_split_v
    if vertical:
        cut = rng.randint(min_size, w - min_size)
        split_space(rng, x, y, cut, h, min_size, leaves)
        split_space(rng, x + cut, y, w - cut, h, min_size, leaves)
    else:
        cut = rng.randint(min_size, h - min_size)
        split_space(rng, x, y, w, cut, min_size, leaves)
        split_space(rng, x, y + cut, w, h - cut, min_size, leaves)
