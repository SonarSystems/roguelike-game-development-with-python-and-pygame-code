# file: ember/entity_factories.py
"""Recipes for every kind of creature. Each call builds a brand-new Entity."""
from ember import settings
from ember.ai import CowardlyEnemy, HostileEnemy
from ember.components import Fighter, Inventory
from ember.consumables import (ConfusionConsumable, FireballDamageConsumable,
                               HealingConsumable, LightningDamageConsumable)
from ember.entity import Entity


def player(x, y):
    return Entity(x, y, "@", settings.EMBER, "Player", blocks_movement=True,
                  fighter=Fighter(hp=30, defense=1, power=5), render_order=2,
                  inventory=Inventory(capacity=26))


def _monster(x, y, char, color, name, speed, fighter, ai_class=HostileEnemy):
    monster = Entity(x, y, char, color, name, blocks_movement=True, speed=speed,
                     fighter=fighter)
    monster.ai = ai_class(monster)
    return monster


def rat(x, y):
    return _monster(x, y, "r", (180, 140, 110), "Giant Rat", speed=200,
                    fighter=Fighter(hp=4, defense=0, power=2))       # fast but fragile


def goblin(x, y):
    return _monster(x, y, "g", (90, 200, 90), "Goblin", speed=100,
                    fighter=Fighter(hp=10, defense=0, power=4))


def troll(x, y):
    return _monster(x, y, "T", (60, 140, 60), "Troll", speed=50,
                    fighter=Fighter(hp=24, defense=2, power=8))       # slow, hits hard


def imp(x, y):
    return _monster(x, y, "i", (230, 90, 200), "Imp", speed=100,
                    fighter=Fighter(hp=6, defense=1, power=2), ai_class=CowardlyEnemy)


# -------- items
def health_potion(x, y):
    return Entity(x, y, "!", (230, 60, 200), "Health Potion",
                  consumable=HealingConsumable(amount=8))


def lightning_scroll(x, y):
    return Entity(x, y, "~", (255, 255, 120), "Lightning Scroll",
                  consumable=LightningDamageConsumable(damage=20, maximum_range=5))


def confusion_scroll(x, y):
    return Entity(x, y, "~", (200, 120, 255), "Confusion Scroll",
                  consumable=ConfusionConsumable(turns=10))


def fireball_scroll(x, y):
    return Entity(x, y, "~", (255, 90, 30), "Fireball Scroll",
                  consumable=FireballDamageConsumable(damage=12, radius=3))
