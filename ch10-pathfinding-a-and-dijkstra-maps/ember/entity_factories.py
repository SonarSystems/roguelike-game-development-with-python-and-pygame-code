# file: ember/entity_factories.py
"""Recipes for every kind of creature. Each call builds a brand-new Entity."""
from ember import settings
from ember.ai import CowardlyEnemy, HostileEnemy
from ember.entity import Entity


def player(x, y):
    return Entity(x, y, "@", settings.EMBER, "Player", blocks_movement=True)


def _monster(x, y, char, color, name, speed, ai_class=HostileEnemy):
    monster = Entity(x, y, char, color, name, blocks_movement=True, speed=speed)
    monster.ai = ai_class(monster)
    return monster


def rat(x, y):
    return _monster(x, y, "r", (180, 140, 110), "Giant Rat", speed=200)   # twice as fast


def goblin(x, y):
    return _monster(x, y, "g", (90, 200, 90), "Goblin", speed=100)


def troll(x, y):
    return _monster(x, y, "T", (60, 140, 60), "Troll", speed=50)          # half speed


def imp(x, y):
    return _monster(x, y, "i", (230, 90, 200), "Imp", speed=100, ai_class=CowardlyEnemy)
