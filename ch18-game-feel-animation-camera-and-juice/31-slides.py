def ease_out(t):
    """Fast at the start, gentle at the end: feels snappier than linear."""
    return 1 - (1 - t) ** 3
