# file: tests/conftest.py
"""Shared test setup: run Pygame without opening a window."""
import os

import pygame
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


@pytest.fixture(scope="session", autouse=True)
def headless_pygame():
    pygame.init()
    pygame.display.set_mode((1, 1))     # fonts and surfaces need a display
    yield
    pygame.quit()
