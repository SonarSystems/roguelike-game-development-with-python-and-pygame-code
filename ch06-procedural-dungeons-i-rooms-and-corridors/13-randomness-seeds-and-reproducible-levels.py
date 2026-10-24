import random

>>> import random
>>> a = random.Random(42)
>>> b = random.Random(42)
>>> [a.randint(1, 6) for _ in range(5)]
[6, 1, 1, 6, 3]
>>> [b.randint(1, 6) for _ in range(5)]
[6, 1, 1, 6, 3]
