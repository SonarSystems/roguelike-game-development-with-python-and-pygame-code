@dataclass(frozen=True)
class TileType:
    name: str
    glyph: str           # the character drawn for this tile
    color: tuple         # foreground colour of the glyph
    background: tuple    # colour filled behind the glyph
    walkable: bool       # can creatures stand here?
    transparent: bool    # can light and sight pass through?
