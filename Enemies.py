import locale
import random
from math import sin

from PyQt6.QtCore import QTimer, QRectF, Qt
from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsRectItem

        # enemies = [ (name, hp, damage, step, speed_shoot, size_x, size_y, color) ]
enemies = [
            ('Default',      3,  1,      1,          0,       35,     35,      QColor(150, 0, 0)),#45x45
            ('Ping_pong',    1,  1,      3,          0,       15,     15,      QColor(255, 111, 0)),
            ('Fat',          5,  1,      0.5,        0,       40,     40,      QColor(255, 111, 111)),
        ]
hp = []
damage = []
step = []
speed_shoot = []
size_x = []
size_y = []
color = []
for i in range(len(enemies)):
    hp.append(enemies[i][1])
    damage.append(enemies[i][2])
    step.append(enemies[i][3])
    speed_shoot.append(enemies[i][4])
    size_x.append(enemies[i][5])
    size_y.append(enemies[i][6])
    color.append(enemies[i][7])
array_enemies = []
timer = QTimer()
timer.timeout.connect(timer.stop)

class Enemy(QGraphicsRectItem):
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
        self.shoot = 0
        self.speed_l = 0
        self.speed_r = 0
        self.speed_u = 0
        self.speed_d = 0
        self.step = 0
        self.size_x = 0
        self.size_y = 0
        self.window_x = 0
        self.window_y = 0
        self.hp = 0
        self.hit_delay = 0
        self.damage = 0
        self.speed_shoot = 0
        self.move = None

def default_enemy(scene):
    type = 0
    enemy = Enemy()
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    enemy.setBrush(QBrush(color[type]))
    enemy.setRect(0,0,enemy.size_x,enemy.size_y)
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width()+1),int(scene.width())-int(scene.width()*1.2))
    y = random.randint(0,int(scene.height()-enemy.size_y))
    enemy.setPos(random.choice((x1,x2)),y)
    direction = random.choice((-1,1))
    def move():
        enemy.moveBy(enemy.step*direction,0)
    enemy.move = move
    scene.addItem(enemy)
    return enemy

def ping_pong_enemy(scene):
    type = 1
    enemy = Enemy()
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    enemy.setBrush(QBrush(color[type]))
    enemy.setRect(0,0,enemy.size_x,enemy.size_y)
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width()+1),int(scene.width())-int(scene.width()*1.2))
    y = random.randint(0,int(scene.height()-enemy.size_y))
    enemy.setPos(random.choice((x1,x2)),y)
    direction = random.choice((-1,1))

    move_proportion_x = random.uniform(0.3,0.9)
    move_proportion_y = 1 - move_proportion_x
    enemy.speed_d = random.choice((-enemy.step,enemy.step))
    def move():
        if enemy.y() - enemy.step < 0:
            enemy.speed_d = enemy.step
            enemy.speed_u = 0
        elif enemy.y() + enemy.size_y + enemy.step > scene.height():
            enemy.speed_u = enemy.step
            enemy.speed_d = 0
        enemy.moveBy((enemy.step*direction)*move_proportion_x,(enemy.speed_d-enemy.speed_u)*move_proportion_y)
    enemy.move = move
    scene.addItem(enemy)
    return enemy











