import random

cards = {
            "speed_cards": {
                "Slow_down": 0.9,
                "Speed_Up": 1.2
                                            },
            "hp_cards": {
                "Fat_player": 2,
                "Tiny_player": 2
                                            }
}

random_type_cards = random.choice(list(cards))
random_effect = random.choice(list(cards[random_type_cards]))
effect_value = cards[random_type_cards][random_effect]
print(random_effect,' ', effect_value)