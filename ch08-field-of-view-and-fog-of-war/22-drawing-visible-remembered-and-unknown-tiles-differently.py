def darken(color, factor=0.4):
    """A dimmer version of a colour, for remembered-but-not-visible cells."""
    return tuple(int(c * factor) for c in color)
