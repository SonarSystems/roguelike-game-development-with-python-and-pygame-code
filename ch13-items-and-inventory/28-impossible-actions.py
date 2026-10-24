try:
    action.perform(self)
except Impossible as reason:
    self.log(str(reason), settings.IMPOSSIBLE)
    return          # an impossible action doesn't use up a turn
