# file: ember/camera.py
"""The camera: which part of a big map is on screen."""
from ember import settings


class Camera:
    def __init__(self, width=settings.VIEW_WIDTH, height=settings.VIEW_HEIGHT,
                 cell_size=settings.CELL_SIZE):
        self.width = width            # view size, in cells
        self.height = height
        self.cell_size = cell_size
        self.x = 0.0                  # world cell at the view's top-left corner;
        self.y = 0.0                  # floats, so the view can scroll smoothly

    def follow(self, target_x, target_y, map_width, map_height):
        """Centre on (target_x, target_y) without showing past the map's edges."""
        self.x = min(max(0.0, target_x - self.width / 2 + 0.5), max(0, map_width - self.width))
        self.y = min(max(0.0, target_y - self.height / 2 + 0.5), max(0, map_height - self.height))

    def to_pixels(self, world_x, world_y):
        """Screen pixel position of a (possibly fractional) world cell."""
        return (world_x - self.x) * self.cell_size, (world_y - self.y) * self.cell_size

    def screen_to_world(self, px, py):
        """Which world cell is under screen pixel (px, py)?"""
        return int(px // self.cell_size + self.x), int(py // self.cell_size + self.y)
