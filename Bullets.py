from PyQt6.QtCore import QTimer, QRect

import Constants
import Player


class Shooting:
    def __init__(self, b_x=0, b_y=0):
        self.b_x = b_x
        self.b_y = b_y
        self.step = 20


    def move_bullet(self):
        self.b_x += self.step


