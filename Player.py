from PyQt6.QtCore import Qt
import Constants


class MovingPlayer:
    def __init__(self, x=0, y=0, step=5, HP_P=3, X_SIZE_PLAYER = 50, Y_SIZE_PLAYER = 50):
        self.x = x
        self.y = y
        self.step = step
        self.HP_P = HP_P
        self.X_SIZE_PLAYER = X_SIZE_PLAYER
        self.Y_SIZE_PLAYER = Y_SIZE_PLAYER

        self.move_direction_L1 = 0
        self.move_direction_R1 = 0
        self.move_direction_U1 = 0
        self.move_direction_D1 = 0

        self.move_direction_L2 = 0
        self.move_direction_R2 = 0
        self.move_direction_U2 = 0
        self.move_direction_D2 = 0

    def move(self):
        if self.x - self.step < 0:
            self.x = 0
        elif self.move_direction_L1 == 1:
            self.x -= self.step

        if self.x + self.step > Constants.W - self.X_SIZE_PLAYER:
            self.x = Constants.W - self.X_SIZE_PLAYER
        elif self.move_direction_R1 == 1:
            self.x += self.step

        if self.y - self.step < 0:
            self.y = 0
        elif self.move_direction_U1 == 1:
            self.y -= self.step

        if self.y + self.step > Constants.H - self.Y_SIZE_PLAYER:
            self.y = Constants.H - self.Y_SIZE_PLAYER
        elif self.move_direction_D1 == 1:
            self.y += self.step

    def keyPressEvent(self, event):
        if event.text() in ['A', 'a', 'Ф', 'ф']:
            self.move_direction_U1 = 1
        elif event.text() in ['D', 'd', 'В', 'в']:
            self.move_direction_D1 = 1

        if event.key() == Qt.Key.Key_Left:
            self.move_direction_U2 = 1
        elif event.key() == Qt.Key.Key_Right:
            self.move_direction_D2 = 1

    def keyReleaseEvent(self, event):
        if event.text() in ['A', 'a', 'Ф', 'ф']:
            self.move_direction_U1 = 0
        elif event.text() in ['D', 'd', 'В', 'в']:
            self.move_direction_D1 = 0

        if event.key() == Qt.Key.Key_Left:
            self.move_direction_U2 = 0
        elif event.key() == Qt.Key.Key_Right:
            self.move_direction_D2 = 0