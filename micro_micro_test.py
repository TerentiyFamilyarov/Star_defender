# import random
# import sys
# from typing import Dict
#
# from PyQt6.QtWidgets import QPushButton, QApplication
#
#
# # from collections import OrderedDict
# # cards = {
# #             "speed_cards": {
# #                 "Slow_down": 0.9,
# #                 "Speed_Up": 1.2
# #                                             },
# #             "hp_cards": {
# #                 "Fat_player": 2,
# #                 "Tiny_player": 2
# #                                             }
# # }
# #
# # # random_type_cards = random.choice(list(cards))
# # # random_effect = random.choice(list(cards[random_type_cards]))
# # # effect_value = cards[random_type_cards][random_effect]
# # # print(random_effect,' ', effect_value)
# # # keysc = []
# # # for key in cards:
# # #     keysc.append(key)
# # #     keysc.append(cards.values())
# # #
# # # print(keysc)
# #
# #
# # type_object = {
# #     "player": {
# #         0:"default",
# #         1:"IShowSpeed",
# #         2:"BurgerKing"
# #     },
# #     "enemy": {
# #         0:"default",
# #         1:"tiny",
# #         2:"fat"
# #     },
# #     "bullet": {
# #         0:"default"
# #     }
# # }
# #
# # # for key in type_object:
# # #     print(key)
# # #     for value in type_object[key]:
# # #         print(type_object[key][value])
# # player_keys = list(type_object["player"].keys())
# # print(f"{type_object["player"][0]}") # default
# # def random_effect():
# #     robject = [
# #         "player",
# #         "enemy",
# #         "bullet"
# #     ]
# #     chobject = random.choice(robject)
# #     if chobject == "player":
# #         effects = [
# #             "step",
# #             "speed_shoot",
# #             "HP_O",
# #             "size",
# #             "damage",
# #             "soap_koef"
# #         ]
# #     else:
# #         effects = [
# #             "step",
# #             "HP_O",
# #             "size",
# #             "damage",
# #         ]
# #     effect = random.choice(effects)
# #     return chobject, effect
# # chosen_object, effect = random_effect()
# # print(chosen_object,effect)
# class Card(QPushButton):
#     def __init__(self):
#         super().__init__()
#         self.modifications()
#         self.setGeometry(0, 0, self.x_size, self.y_size)
#         self.txt_chosen_object_1, self.txt_effect_1, self.chosen_object_1, self.effect_1 = self.random_effect()
#         self.effect_power_1 = random.randint(0, 6)
#         self.setText(f"{self.txt_chosen_object_1} {self.txt_effect_1} + {self.effect_power_1}%")
#         self.setStyleSheet("text-align: top"
#                            "")
#         self.clicked.connect(self.close)
#
#
#     def modifications(self, x_size=200, y_size=500):
#         self.x_size = x_size
#         self.y_size = y_size
#         self.max_x_size = x_size
#         self.max_y_size = y_size
#
#     def random_effect(self):
#         robject = {
#             "Player": "player",
#             "Enemies": "enemy",
#             "Bullets": "bullet"
#         }
#         chobject = random.choice(list(robject.keys()))
#         if chobject == "player":
#             effects = {
#                 "Speed": "step",
#                 "Speed shoot": "speed_shoot",
#                 "Hp": "HP_O",
#                 "Size": "x_size",
#                 "Damage": "damage",
#                 "Soap Coefficient":"soap_koef"
#             }
#         else:
#             effects = {
#                 "Speed": "step",
#                 "Speed shoot": "speed_shoot",
#                 "Hp": "HP_O",
#                 "Size": "x_size",
#                 "Damage": "damage",
#             }
#         effect = random.choice(list(effects.keys()))
#         obj = getattr(self, robject[chobject])
#         setattr(obj, effects[effect], getattr(obj, effects[effect]) + 1)
#         return chobject, effect, robject[chobject], effects[effect]
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     game_window = Card()
#     game_window.show()
#     sys.exit(app.exec())