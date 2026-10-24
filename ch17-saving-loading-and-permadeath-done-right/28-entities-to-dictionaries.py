def ai_to_dict(brain):
    if brain is None:
        return None
    data = {"type": type(brain).__name__}
    if isinstance(brain, ai.HostileEnemy):
        data["last_seen"] = brain.last_seen
    elif isinstance(brain, ai.ConfusedEnemy):
        data["turns"] = brain.turns_remaining
        data["previous"] = ai_to_dict(brain.previous_ai)
    return data
