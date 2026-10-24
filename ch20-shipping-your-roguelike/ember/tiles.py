# file: ember/tiles.py
"""Tile types: what each kind of map square looks like and how it behaves."""
from dataclasses import dataclass


@dataclass(frozen=True)
class TileType:
    name: str
    glyph: str           # the character drawn for this tile
    color: tuple         # foreground colour of the glyph
    background: tuple    # colour filled behind the glyph
    walkable: bool       # can creatures stand here?
    transparent: bool    # can light and sight pass through?


FLOOR = TileType("floor", ".", (110, 100, 90), (24, 22, 26), walkable=True, transparent=True)
WALL = TileType("wall", "#", (170, 150, 130), (48, 40, 38), walkable=False, transparent=False)
DOWN_STAIRS = TileType("down stairs", ">", (255, 200, 90), (24, 22, 26), walkable=True, transparent=True)
