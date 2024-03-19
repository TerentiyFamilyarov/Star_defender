import random
from collections import OrderedDict
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

# random_type_cards = random.choice(list(cards))
# random_effect = random.choice(list(cards[random_type_cards]))
# effect_value = cards[random_type_cards][random_effect]
# print(random_effect,' ', effect_value)
# keysc = []
# for key in cards:
#     keysc.append(key)
#     keysc.append(cards.values())
#
# print(keysc)


type_object = {
    "player": {
        0:"default",
        1:"IShowSpeed",
        2:"BurgerKing"
    },
    "enemy": {
        0:"default",
        1:"tiny",
        2:"fat"
    },
    "bullet": {
        0:"default"
    }
}

# for key in type_object:
#     print(key)
#     for value in type_object[key]:
#         print(type_object[key][value])
player_keys = list(type_object["player"].keys())
print(f"{type_object["player"][0]}") # default
