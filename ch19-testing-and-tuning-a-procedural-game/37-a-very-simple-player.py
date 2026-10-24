import pygame

def take_turn(engine):
    player = engine.player
    if isinstance(engine.event_handler, LevelUpEventHandler):
        press(engine, pygame.K_a)                      # always take +20 HP
        return
    if not isinstance(engine.event_handler, MainGameEventHandler):
        press(engine, pygame.K_ESCAPE)                 # close any menu
        return
    fighter = player.fighter
    potions = [i for i in player.inventory.items if i.name == "Health Potion"]
    if fighter.hp <= fighter.max_hp * 0.4 and potions:
        press(engine, pygame.K_i)
        press(engine, pygame.K_a + player.inventory.items.index(potions[0]))
        return
    crown = [i for i in player.inventory.items if i.name == "Ember Crown"]
    if crown:
        press(engine, pygame.K_i)
        press(engine, pygame.K_a + player.inventory.items.index(crown[0]))
        return
    for monster in engine.entities:                    # fight anything adjacent
        if monster.ai is not None and player.distance_to(monster.x, monster.y) == 1:
            press(engine, KEYS[(monster.x - player.x, monster.y - player.y)])
            return
    here = [e for e in engine.entities if e.is_item and (e.x, e.y) == (player.x, player.y)]
    if here and not player.inventory.is_full:
        press(engine, pygame.K_g)
        return
    gm = engine.game_map
    if gm.tiles[player.x][player.y].glyph == ">":
        press(engine, pygame.K_PERIOD, ">")
        return
    items = {(e.x, e.y) for e in engine.entities
             if e.is_item and (e.x, e.y) in gm.visible}
    stairs = {(x, y) for x, y in gm.explored if gm.tiles[x][y].glyph == ">"}
    unexplored = {c for c in gm.floor_cells() if c not in gm.explored}
    for targets in (items, stairs, unexplored):
        step = first_step(engine, targets)
        if step:
            press(engine, KEYS[step])
            return
    press(engine, pygame.K_PERIOD)                     # nothing to do: wait
