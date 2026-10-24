# file: ember/entity_factories.py
"""Recipes for every kind of creature and item. Each call builds a brand-new Entity."""
from ember import settings
from ember.ai import CowardlyEnemy, HostileEnemy
from ember.components import Equipment, Equippable, Fighter, Inventory, Level
from ember.consumables import (ConfusionConsumable, FireballDamageConsumable,
                               HealingConsumable, LightningDamageConsumable)
from ember.entity import Entity


def player(x, y):
    hero = Entity(x, y, "@", settings.EMBER, "Player", blocks_movement=True,
                  fighter=Fighter(hp=30, base_defense=1, base_power=2), render_order=2,
                  inventory=Inventory(capacity=26), level=Level(), equipment=Equipment())
    # Every adventurer starts with a dagger and leather armour, already equipped.
    for item in (dagger(0, 0), leather_armor(0, 0)):
        hero.inventory.items.append(item)
        hero.equipment.slots[item.equippable.slot] = item
    return hero


def _monster(x, y, char, color, name, speed, fighter, xp, ai_class=HostileEnemy):
    monster = Entity(x, y, char, color, name, blocks_movement=True, speed=speed,
                     fighter=fighter, level=Level(xp_given=xp))
    monster.ai = ai_class(monster)
    return monster


def rat(x, y):
    return _monster(x, y, "r", (180, 140, 110), "Giant Rat", speed=200,
                    fighter=Fighter(hp=4, base_defense=0, base_power=2), xp=20)


def goblin(x, y):
    return _monster(x, y, "g", (90, 200, 90), "Goblin", speed=100,
                    fighter=Fighter(hp=10, base_defense=0, base_power=4), xp=35)


def troll(x, y):
    return _monster(x, y, "T", (60, 140, 60), "Troll", speed=50,
                    fighter=Fighter(hp=24, base_defense=2, base_power=8), xp=100)


def imp(x, y):
    return _monster(x, y, "i", (230, 90, 200), "Imp", speed=100,
                    fighter=Fighter(hp=6, base_defense=1, base_power=2), xp=25,
                    ai_class=CowardlyEnemy)


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


# -------- equipment
def dagger(x, y):
    return Entity(x, y, "/", (190, 190, 210), "Dagger",
                  equippable=Equippable("weapon", power_bonus=2))


def sword(x, y):
    return Entity(x, y, "/", (220, 220, 255), "Sword",
                  equippable=Equippable("weapon", power_bonus=4))


def leather_armor(x, y):
    return Entity(x, y, "[", (160, 110, 60), "Leather Armor",
                  equippable=Equippable("armor", defense_bonus=1))


def chain_mail(x, y):
    return Entity(x, y, "[", (190, 190, 190), "Chain Mail",
                  equippable=Equippable("armor", defense_bonus=3))
