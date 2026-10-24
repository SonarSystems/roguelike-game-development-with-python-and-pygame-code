def entity_from_dict(data):
    name = data["name"]
    is_corpse = name.startswith(CORPSE_PREFIX)
    factory = FACTORY_BY_NAME[name[len(CORPSE_PREFIX):] if is_corpse else name]
    entity = factory(data["x"], data["y"])
    entity.energy = data["energy"]
    if "fighter" in data:
        for key, value in data["fighter"].items():
            setattr(entity.fighter, key, value)
    if "level" in data:
        for key, value in data["level"].items():
            setattr(entity.level, key, value)
    if "inventory" in data:
        entity.inventory.items = [entity_from_dict(item) for item in data["inventory"]]
        entity.equipment.slots = {"weapon": None, "armor": None}
        for index in data["equipped"]:
            item = entity.inventory.items[index]
            entity.equipment.slots[item.equippable.slot] = item
    if is_corpse:
        from ember import settings
        entity.char, entity.color, entity.name = "%", settings.CORPSE_RED, name
        entity.blocks_movement, entity.render_order = False, 0
    entity.ai = ai_from_dict(data["ai"], entity)
    return entity
