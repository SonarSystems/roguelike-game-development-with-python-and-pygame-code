def distance_to(self, x, y):
    """Chebyshev distance: the number of king-moves (diagonals allowed)."""
    return max(abs(self.x - x), abs(self.y - y))
