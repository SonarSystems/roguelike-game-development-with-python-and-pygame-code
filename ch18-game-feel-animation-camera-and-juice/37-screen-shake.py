import random

def shake_offset(self):
    # Squaring trauma makes small hits subtle and big hits dramatic.
    amount = MAX_SHAKE * self.trauma ** 2
    return random.uniform(-amount, amount), random.uniform(-amount, amount)
