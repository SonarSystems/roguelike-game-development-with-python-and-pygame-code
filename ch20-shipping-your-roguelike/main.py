# file: main.py
"""Top-level launcher. pygbag requires a main.py in the project folder, and
PyInstaller needs a plain script to start from; both use this one."""
import asyncio

# pygbag decides which packages to load in the browser by scanning *this*
# file's imports. Without this line it never loads pygame-ce, and the first
# use of a pygame constant fails with AttributeError (see Chapter 20).
import pygame  # noqa: F401

from ember.main import main_async

asyncio.run(main_async())
