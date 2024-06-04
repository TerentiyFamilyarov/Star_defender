import random
from math import sin, cos, pi
from time import sleep

from PyQt6.QtCore import QTimer, QPointF, Qt, QRectF
from PyQt6.QtGui import QColor, QBrush, QPen, QKeyEvent, QInputEvent
from PyQt6.QtWidgets import QGraphicsRectItem

# bullets = [ (name,         damage, step, speed_shoot, size_x, size_y, color) ]
bullet_count = 1
bullet_degree = 45
first_arg_method = bullet_count
second_arg_mothod = bullet_degree
size_koef = 1
damage_koef = 1
speed_koef = 1
speed_shoot_koef = 1
bullets = [
            ('Default',      1,      13,  1,   10,  3,     QColor(0, 255, 0)),
            ('Chaos',        0.5,    5,   1,4,   4,     QColor(255, 111, 0)),
            ('Navigation',   5,      2,   400, 5,   6,     QColor(255, 111, 111)),
        ]

def update_bullets_list():
    global bullets, bullet_count, bullet_degree, first_arg_method, second_arg_mothod
    bullets = [
        ('Default',   (1*damage_koef),  (13 * speed_koef),int(1*speed_shoot_koef),   int(10 * size_koef),int(3 * size_koef), QColor(0, 255, 0)),
        ('Chaos',     (0.5*damage_koef),(5 * speed_koef), int(1*speed_shoot_koef),int(4 * size_koef), int(4 * size_koef), QColor(255, 111, 0)),
        ('Navigation',(5*damage_koef),  (2 * speed_koef), int(4*speed_shoot_koef), int(5 * size_koef), int(6 * size_koef), QColor(255, 111, 111)),
    ]
    damage.clear()
    step.clear()
    speed_shoot.clear()
    size_x.clear()
    size_y.clear()
    color.clear()
    for i in range(len(bullets)):
        damage.append(bullets[i][1])
        step.append(bullets[i][2])
        speed_shoot.append(bullets[i][3])
        size_x.append(bullets[i][4])
        size_y.append(bullets[i][5])
        color.append(bullets[i][6])
    if bullet_count < 1:
        bullet_count = 1
    if bullet_degree >= 360:
        bullet_degree -= 360
    elif bullet_degree <= -360:
        bullet_degree +=360
    first_arg_method = bullet_count
    second_arg_mothod = bullet_degree
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
        self.angle = 0
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
    # bullet.size_x, bullet.size_y = bullets[type][4], bullets[type][5]
    bullet.step = step[type]
    bullet.damage = damage[type]
    bullet.speed_shoot = speed_shoot[type]
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
        move_scale_x = cos(bullet.angle * (pi / 180)) * bullet.step
        move_scale_y = -sin(bullet.angle * (pi / 180)) * bullet.step
        if bullet.move_direction_R == 1:
            if bullet.rotation() != -bullet.angle:
                bullet.setRotation(-bullet.angle)
            bullet.moveBy(move_scale_x,move_scale_y)
        else:
            if bullet.rotation() != bullet.angle:
                bullet.setRotation(bullet.angle)
            bullet.moveBy(-move_scale_x,move_scale_y)
    bullet.move = move
    scene.addItem(bullet)
    array_bullets.append(bullet)
    return bullet


def chaos_bullet(scene):
    type = 1
    bullet = Bullet()
    bullet.size_x, bullet.size_y = size_x[type], size_y[type]
    bullet.step = step[type]
    bullet.damage = damage[type]
    bullet.speed_shoot = speed_shoot[type]
    bullet.setBrush(QBrush(color[type]))
    bullet.setRect(QRectF(0, 0, bullet.size_x, bullet.size_y))
    bullet.setPos(
        scene.player.x() + (scene.player.size_x * scene.player.direction) + (
                    bullet.size_x * (scene.player.direction - 1)),
        (scene.player.y() + scene.player.size_y // 2) - bullet.size_y // 2)
    if scene.player.direction == 1:
        bullet.move_direction_R = 1
        bullet.move_direction_L = 0
    else:
        bullet.move_direction_L = 1
        bullet.move_direction_R = 0
    bullet.timer.start(100)
    bullet.timer.timeout.connect(bullet.timer.stop)
    def move():
        # if bullet.timer.isActive() is False:
        bullet.angle += random.randint(-3,3)
            # bullet.timer.start(25)
        move_scale_x = cos(bullet.angle * (pi / 180)) * bullet.step
        move_scale_y = -sin(bullet.angle * (pi / 180)) * bullet.step
        if bullet.move_direction_R == 1:
            if bullet.rotation() != -bullet.angle:
                bullet.setRotation(-bullet.angle)
            bullet.moveBy(move_scale_x, move_scale_y)
        else:
            if bullet.rotation() != bullet.angle:
                bullet.setRotation(bullet.angle)
            bullet.moveBy(-move_scale_x, move_scale_y)

    bullet.move = move
    scene.addItem(bullet)
    array_bullets.append(bullet)
    return bullet

def navigation_bullet(scene):
    type = 2
    bullet = Bullet()
    bullet.size_x, bullet.size_y = size_x[type], size_y[type]
    bullet.step = step[type]
    bullet.damage = damage[type]
    bullet.speed_shoot = speed_shoot[type]
    bullet.setBrush(QBrush(color[type]))
    bullet.setRect(QRectF(0, 0, bullet.size_x, bullet.size_y))
    bullet.setPos(
        scene.player.x() + (scene.player.size_x * scene.player.direction) + (
                    bullet.size_x * (scene.player.direction - 1)),
        (scene.player.y() + scene.player.size_y // 2) - bullet.size_y // 2)
    if scene.player.direction == 1:
        bullet.move_direction_R = 1
        bullet.move_direction_L = 0
    else:
        bullet.move_direction_L = 1
        bullet.move_direction_R = 0

    def move():
        move_scale_x = cos(bullet.angle * (pi / 180)) * bullet.step
        move_scale_y = -sin(bullet.angle * (pi / 180)) * bullet.step
        if bullet.move_direction_R == 1:
            if bullet.rotation() != -bullet.angle:
                bullet.setRotation(-bullet.angle)
            bullet.moveBy(move_scale_x, move_scale_y)
        else:
            if bullet.rotation() != bullet.angle:
                bullet.setRotation(bullet.angle)
            bullet.moveBy(-move_scale_x, move_scale_y)
        if scene.key_up_pressed == 1:
            bullet.angle += 1
        elif scene.key_down_pressed == 1:
            bullet.angle -= 1

    bullet.move = move
    scene.addItem(bullet)
    array_bullets.append(bullet)
    return bullet


def triple_like_method(scene,*args):
    # global bullet_count
    # count = 3
    ch_bullet, count, degree = args
    # if count < 1:
    #     bullet_count = 1
    #     count = 1
    # if degree >= 360:
    #     degree -= 360
    # elif degree <= -360:
    #     degree += 360
    if count == 1:
        bullet = ch_bullet(scene)
        bullet.angle = 0
    else:
        for i in range(1,count+1):
            # a1 = 15
            a1 = degree
            max_a = -a1
            d = (max_a-a1)/(count-1)
            bullet = ch_bullet(scene)
            bullet.angle = a1 + d*(i-1)
    return bullet

def five_method(scene,ch_bullet):
    count = 5
    for i in range(1,count+1):
        a1 = 15
        max_a = -a1
        d = (max_a-a1)/(count-1)
        bullet = ch_bullet(scene)
        bullet.angle = a1 + d*(i-1)

def seven_method(scene,ch_bullet):
    count = 7
    for i in range(1,count+1):
        a1 = 15
        max_a = -a1
        d = (max_a-a1)/(count-1)
        bullet = ch_bullet(scene)
        bullet.angle = a1 + d*(i-1)


