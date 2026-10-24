# file: ember/exceptions.py
"""Exceptions used for game flow rather than for errors."""


class Impossible(Exception):
    """An action can't be performed. The message is shown to the player,
    and no time passes."""
