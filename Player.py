from PyQt6.QtCore import Qt, QTimer
import Constants


class MovingPlayer:
    def __init__(self, x=0, y=0, step=5, HP_P=3):
        self.Disaster = ''
        self.x = x
        self.y = y
        self.step = step
        self.HP_P = HP_P
        self.X_SIZE_PLAYER = Constants.X_SIZE_PLAYER
        self.Y_SIZE_PLAYER = Constants.Y_SIZE_PLAYER

        self.move_direction_L1 = 0
        self.move_direction_R1 = 0
        self.move_direction_U1 = 0
        self.move_direction_D1 = 0

        if self.Disaster == 'SlowDown':
            self.step-=2
        if self.Disaster == 'UWindy':
            self.step_u = 1
            self.step_d = -1


    def move_up(self):
        self.y -= 1

    def move(self):
        # if self.x - self.step < 0:
        #     self.x = 0
        # elif self.move_direction_L1 == 1:
        #     self.x -= self.step

        # if self.x + self.step > Constants.W - self.X_SIZE_PLAYER:
        #     self.x = Constants.W - self.X_SIZE_PLAYER
        # elif self.move_direction_R1 == 1:
        #     self.x += self.step

        if self.y - self.step < 0 and self.move_direction_U1 == 1:
            self.y = 0
        elif self.move_direction_U1 == 1:
            self.y -= self.step+self.step_u

        if self.y + self.step > Constants.H - self.Y_SIZE_PLAYER and self.move_direction_D1 == 1:
            self.y = Constants.H - self.Y_SIZE_PLAYER
        elif self.move_direction_D1 == 1:
            self.y += self.step+self.step_d

    def keyPressEvent(self, event):
        if event.text() in ['A', 'a', 'Ф', 'ф']:
            self.move_direction_U1 = 1
        elif event.text() in ['D', 'd', 'В', 'в']:
            self.move_direction_D1 = 1


    def keyReleaseEvent(self, event):
        if event.text() in ['A', 'a', 'Ф', 'ф']:
            self.move_direction_U1 = 0
        elif event.text() in ['D', 'd', 'В', 'в']:
            self.move_direction_D1 = 0
