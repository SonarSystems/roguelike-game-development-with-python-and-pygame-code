if actor.equipment and actor.equipment.is_equipped(item):
    actor.equipment.toggle(item, engine)     # take it off before dropping it
