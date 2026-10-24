def troll(x, y):
    return _monster(x, y, "T", (60, 140, 60), "Troll", speed=50,
                    fighter=Fighter(hp=24, base_defense=2, base_power=6), xp=100)
