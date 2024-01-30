import subprocess

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

import Constants


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Star Defender")
        self.setGeometry(0, 0, Constants.W, Constants.H+100)

        layout = QVBoxLayout()

        button_start = QPushButton("Начать игру", self)
        button_start.clicked.connect(self.start_game)
        layout.addWidget(button_start)

        button_exit = QPushButton("Выход", self)
        button_exit.clicked.connect(self.close)
        layout.addWidget(button_exit)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_game(self):
        print("Игра началась")
        # Здесь можно добавить код для перехода к игровому экрану или запуска игры
        subprocess.run('main_game_2p.py')

app = QApplication([])
main_menu = MainMenu()
main_menu.show()
app.exec()