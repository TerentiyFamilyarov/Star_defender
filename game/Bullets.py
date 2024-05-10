import random
from math import sin

from PyQt6.QtCore import QTimer, QPointF, Qt, QRectF
from PyQt6.QtGui import QColor, QBrush, QPen
from PyQt6.QtWidgets import QGraphicsRectItem

# bullets = [ (name,         damage, step, speed_shoot, size_x, size_y, color) ]
bullets = [
            ('Default',      1,      13,        0,           10,     4,     QColor(0, 255, 0)),
            ('Tiny',         0.5,    9,         -100,        13,     3,     QColor(255, 111, 0)),
            ('Fat',          2,      9,         +100,        10,     7,     QColor(255, 111, 111)),
        ]
damage = []
step = []
speed_shoot = []
size_x = []
size_y = []
color = []
for i in range(len(bullets)):
    damage.append(bullets[i][1])
    step.append(bullets[i][2])
    speed_shoot.append(bullets[i][3])
    size_x.append(bullets[i][4])
    size_y.append(bullets[i][5])
    color.append(bullets[i][6])
array_bullets = []
timer = QTimer()
timer.timeout.connect(timer.stop)




class Bullet(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        # self.setRect()
        self.setPen(QPen(Qt.PenStyle.NoPen))
        # self.setBrush(brush)
        self.timer = QTimer()
        self.move_direction_L = 0
        self.move_direction_R = 0
        self.move_direction_U = 0
        self.move_direction_D = 0
        # self.shoot = 0
        self.speed_l = 0
        self.speed_r = 0
        self.speed_u = 0
        self.speed_d = 0
        self.step = 0
        self.size_x = 0
        self.size_y = 0
        self.window_x = 0
        self.window_y = 0
        # self.hp = 0
        self.hit_delay = 0
        self.damage = 0
        self.speed_shoot = 0
        self.move = None

def default_bullet(scene):
    type = 0
    bullet = Bullet()
    bullet.size_x, bullet.size_y = size_x[type], size_y[type]
    bullet.step = step[type]
    bullet.damage = damage[type]
    bullet.setBrush(QBrush(color[type]))
    bullet.setRect(QRectF(0,0,bullet.size_x,bullet.size_y))
    bullet.setPos(
        scene.player.x() + (scene.player.size_x * scene.player.direction) + (bullet.size_x * (scene.player.direction - 1)),
                   (scene.player.y() + scene.player.size_y // 2) -bullet.size_y // 2)
    if scene.player.direction == 1:
        bullet.move_direction_R = 1
        bullet.move_direction_L = 0
    else:
        bullet.move_direction_L = 1
        bullet.move_direction_R = 0
    def move():
        if bullet.move_direction_R == 1:
            bullet.moveBy(bullet.step,0)
        else: bullet.moveBy(-bullet.step,0)
    bullet.move = move
    scene.addItem(bullet)
    return bullet



