# file: ember/settings.py
"""Constants shared by every module: window size, grid size and colours."""

TITLE = "Ember Depths"

CELL_SIZE = 20           # each grid cell is 20x20 pixels
GRID_WIDTH = 64          # cells across
GRID_HEIGHT = 40         # cells down
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE    # 1280 pixels
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE  # 800 pixels

# Screen layout: the map fills the top, the panel the bottom rows.
MAP_WIDTH = GRID_WIDTH
MAP_HEIGHT = 32
PANEL_Y = MAP_HEIGHT          # first row of the bottom panel
BAR_WIDTH = 20                # health bar width, in cells
LOG_X = BAR_WIDTH + 3         # message log starts here
LOG_LINES = 6

FPS = 60
FONT_SIZE = 26

BLACK = (10, 10, 14)
WHITE = (235, 235, 235)
EMBER = (255, 170, 60)

# Message and status colours
DEATH_RED = (220, 50, 50)
CORPSE_RED = (140, 30, 30)
ORANGE = (255, 150, 70)
PLAYER_ATTACK = (230, 230, 230)
ENEMY_ATTACK = (255, 180, 180)
BAR_FILLED = (190, 50, 40)
BAR_EMPTY = (70, 25, 25)
PANEL_BG = (18, 16, 20)
TOOLTIP = (200, 200, 140)
