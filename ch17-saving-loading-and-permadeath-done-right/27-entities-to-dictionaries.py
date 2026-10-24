def entity_to_dict(entity):
    data = {"name": entity.name, "x": entity.x, "y": entity.y, "energy": entity.energy,
            "ai": ai_to_dict(entity.ai)}
    if entity.fighter:
        f = entity.fighter
        data["fighter"] = {"hp": f.hp, "max_hp": f.max_hp,
                           "base_power": f.base_power, "base_defense": f.base_defense}
    if entity.level:
        lv = entity.level
        data["level"] = {"current_level": lv.current_level, "current_xp": lv.current_xp}
    if entity.inventory:
        data["inventory"] = [entity_to_dict(item) for item in entity.inventory.items]
    if entity.equipment:
        items = entity.inventory.items
        data["equipped"] = [items.index(item) for item in entity.equipment.slots.values() if item]
    return data
