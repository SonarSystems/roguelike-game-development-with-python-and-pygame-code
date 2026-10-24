def get_action(self, user, engine):
    """What happens when the player picks this item from the inventory.

    Most items are used straight away. Targeted items override this to
    switch the game into a targeting mode first, and return None.
    """
    return ItemAction(user, self.entity)
