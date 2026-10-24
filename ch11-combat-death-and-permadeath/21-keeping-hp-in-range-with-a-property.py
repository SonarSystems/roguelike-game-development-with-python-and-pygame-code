@property
def hp(self):
    return self._hp

@hp.setter
def hp(self, value):
    self._hp = max(0, min(value, self.max_hp))
