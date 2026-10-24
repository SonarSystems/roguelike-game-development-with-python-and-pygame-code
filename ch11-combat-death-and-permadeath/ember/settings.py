# file: ember/settings.py
"""Constants shared by every module: window size, grid size and colours."""

TITLE = "Ember Depths"

CELL_SIZE = 20           # each grid cell is 20x20 pixels
GRID_WIDTH = 64          # cells across
GRID_HEIGHT = 40         # cells down
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE    # 1280 pixels
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE  # 800 pixels

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
