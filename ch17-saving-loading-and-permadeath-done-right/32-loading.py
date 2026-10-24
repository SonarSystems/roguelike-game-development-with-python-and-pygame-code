def ai_from_dict(data, entity):
    if data is None:
        return None
    brain_class = getattr(ai, data["type"])
    if brain_class is ai.ConfusedEnemy:
        return ai.ConfusedEnemy(entity, ai_from_dict(data["previous"], entity), data["turns"])
    brain = brain_class(entity)
    if "last_seen" in data and data["last_seen"] is not None:
        brain.last_seen = tuple(data["last_seen"])
    return brain
