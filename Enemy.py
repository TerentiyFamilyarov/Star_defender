from random import random

from PyQt6.QtCore import QTimer, QRect

import Constants
import Player


class MovingEnemy:
    def __init__(self, x=1000, y=0, HP_E=3, step=2):
        self.x = Constants.W
        self.y = y
        self.step = step
        self.HP_E = HP_E

        # self.HP_E = int(self.HP_E + 0.5 * self.score)
        # self.step = self.step + 5 * self.score

        # self.player1 = Player.MovingPlayer(10, 50, 3, 5)
        # self.player2 = Player.MovingPlayer(100, Constants.H - 50, 7, 3)


    def move(self):
        self.x -= self.step


