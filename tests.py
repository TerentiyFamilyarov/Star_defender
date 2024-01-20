import random
import sys

from PyQt6.QtCore import QTimer, Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QPixmap, QImage
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

W=1000
H=600
STEP = 10
X_SIZE_PLAYER = 50
Y_SIZE_PLAYER = 50
Hits = 0
X_SIZE_ENEMY = 40
Y_SIZE_ENEMY = 30

class MovingPlayer:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move_left(self):
        self.x += -STEP

    def move_right(self):
        self.x += STEP

    def move_up(self):
        self.y += -STEP

    def move_down(self):
        self.y += STEP


class MovingEnemy:
    def __init__(self, x=W, y=0):
        self.x = x
        self.y = y

    def move(self):
        self.x += -5
        self.y += 0

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Star Defender')
        self.setGeometry(100, 100, W, H)

        self.player = MovingPlayer(10, H//2)
        self.enemy = MovingEnemy( W, random.randrange(0, H+1, 1) )

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(60)
        self.showMaximized()




    def update_game(self):
        # Обновление состояния объекта
        self.enemy.move()
        self.update()


    def keyPressEvent(self, event):
        if self.player.x-STEP < 0:
            self.player.x = 0
        elif event.key() == Qt.Key.Key_Left:
            self.player.move_left()

        if self.player.x+STEP > W-X_SIZE_PLAYER:
            self.player.x = W-X_SIZE_PLAYER
        elif event.key() == Qt.Key.Key_Right:
            self.player.move_right()

        if self.player.y-STEP < 0:
            self.player.y = 0
        elif event.key() == Qt.Key.Key_Up:
            self.player.move_up()

        if self.player.y+STEP > H-Y_SIZE_PLAYER:
            self.player.y = H-Y_SIZE_PLAYER
        elif event.key() == Qt.Key.Key_Down:
            self.player.move_down()




    def paintEvent(self, event, Qpixmap=None):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(0, 0, 1000, 600, QColor(153, 255, 153))  # Очищаем окно, закрашивая его зеленым

        painter.drawImage(QRect(self.player.x,self.player.y,X_SIZE_PLAYER,Y_SIZE_PLAYER), QImage('player.png'))
        painter.drawImage(QRect(self.enemy.x,self.enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY), QImage('enemy.png'))






if __name__ == '__main__':
    app = QApplication([])
    game_window = GameWindow()
    sys.exit(app.exec())
