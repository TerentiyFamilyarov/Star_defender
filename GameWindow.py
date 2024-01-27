from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QLabel, QMainWindow

import Constants
import Player


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.initUI()



    def initUI(self):
        self.setWindowTitle('Star Defender')
        self.setGeometry(0, 0, Constants.W, Constants.H+100)
