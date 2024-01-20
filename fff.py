import sys

from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtWidgets import QGraphicsItem, QMainWindow, QApplication

#Const
PLAYER_SIZE= 50
SCREEN_WIDTH= 1200
SCREEN_HEIGHT= 600

class Player(QGraphicsItem):
    def __init__(self):
        super().__init__()

        self.rect = QRectF(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.setPos(QPointF(SCREEN_WIDTH / 2 - PLAYER_SIZE / 2, SCREEN_HEIGHT - PLAYER_SIZE))





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Star Defender")
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.show()

# Запуск игры
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
