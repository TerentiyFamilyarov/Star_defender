import random
import sys

from PyQt6.QtCore import QTimer, Qt, QRect, QPropertyAnimation
from PyQt6.QtGui import QPainter, QColor, QPixmap, QImage
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

W=1000
H=600
X_SIZE_PLAYER = 50
Y_SIZE_PLAYER = 50
X_SIZE_ENEMY = 40
Y_SIZE_ENEMY = 30

class MovingPlayer:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.step = 1
        self.HP_P = 3

        self.move_direction_L = 0
        self.move_direction_R = 0
        self.move_direction_U = 0
        self.move_direction_D = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(5)

        # self.animation = QPropertyAnimation(self.move, b'position')
        # self.animation.setDuration(1000)
        # self.animation.setStartValue(self.x, self.y)
        # self.animation.setEndValue(self.move())

    def move(self):
        if self.x -self.step < 0:
            self.x = 0
        elif self.move_direction_L == 1:
            self.x += -self.step
        if self.x + self.step > W-X_SIZE_PLAYER:
            self.x = W-X_SIZE_PLAYER
        elif self.move_direction_R == 1:
            self.x += self.step
        if self.y - self.step < 0:
            self.y = 0
        elif self.move_direction_U == 1:
            self.y += -self.step
        if self.y + self.step > H-Y_SIZE_PLAYER:
            self.y = H-Y_SIZE_PLAYER
        elif self.move_direction_D == 1:
            self.y += self.step





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
        if event.key() == Qt.Key.Key_W:
            self.player.move_direction_U = 1
        elif event.key() == Qt.Key.Key_S:
            self.player.move_direction_D = 1
        elif event.key() == Qt.Key.Key_A:
            self.player.move_direction_L = 1
        elif event.key() == Qt.Key.Key_D:
            self.player.move_direction_R = 1

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_W:
            self.player.move_direction_U = 0
        elif event.key() == Qt.Key.Key_S:
            self.player.move_direction_D = 0
        elif event.key() == Qt.Key.Key_A:
            self.player.move_direction_L = 0
        elif event.key() == Qt.Key.Key_D:
            self.player.move_direction_R = 0




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
