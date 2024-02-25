import random

cards = {
        "Slow_down": 0.9,
        "Speed_Up": 'папа',
        "Fat_player": 2
    }
use = random.choice(list(cards.keys()))
used = cards[use]
print(f"Случайный ключ: {use}")
print(f"Значение для случайного ключа: {used}")
