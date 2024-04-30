import random
from math import sin

from PyQt6.QtCore import QTimer, QPointF
from PyQt6.QtGui import QColor

def default_move(obj):
    if obj.move_direction_L == 1:
        obj.speed_l = obj.step
    elif obj.move_direction_L == 0:
        obj.speed_l = 0

    if obj.move_direction_R == 1:
        obj.speed_r = obj.step
    elif obj.move_direction_R == 0:
        obj.speed_r = 0

    if obj.move_direction_U == 1:
        obj.speed_u = obj.step
    elif obj.move_direction_U == 0:
        obj.speed_u = 0

    if obj.move_direction_D == 1:
        obj.speed_d = obj.step
    elif obj.move_direction_D == 0:
        obj.speed_d = 0

    obj.moveBy(-obj.speed_l + obj.speed_r, -obj.speed_u + obj.speed_d)
def sinlike_move(obj):
    if obj.move_direction_L == 1:
        obj.speed_l = obj.step
        obj.speed_u = sin(obj.x())*obj.step
    if obj.move_direction_R == 1:
        obj.speed_r = obj.step
        obj.speed_u = sin(obj.x())*obj.step

def unsinlike_move(obj):
    if obj.move_direction_L == 1:
        obj.speed_l = obj.step
        obj.speed_u = -sin(obj.x()) * obj.step
    if obj.move_direction_R == 1:
        obj.speed_r = obj.step
        obj.speed_u = -sin(obj.x()) * obj.step

    obj.moveBy(-obj.speed_l + obj.speed_r, -obj.speed_u + obj.speed_d)

        # bullets = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color, move_pattern, parameters) ]
bullets = [
            ('Default',      1,  1,      13,    0,         0,           10,     4,     QColor(0, 255, 0), default_move, None),
            ('Tiny',         1,  0.5,    9,    0,         -100,        13,     3,     QColor(255, 111, 0), random.choice((sinlike_move,unsinlike_move)),None),
            ('Fat',          1,  2,      9,     0,         +100,        10,     7,     QColor(255, 111, 111),default_move,None),
        ]
array_bullets = []
timer = QTimer()
def create_bullet(scene, player, array_bullets: list, bullets: list, wch_b_t:int):
    if player.shoot == 1:
        if timer.isActive() is False:
            bullet = scene.create_rectobj_podclass_from_class(scene, timer, player.speed_shoot+bullets[wch_b_t][5],
                                                              bullets[wch_b_t][1], bullets[wch_b_t][2],
                                                              bullets[wch_b_t][3], bullets[wch_b_t][4],
                                                              bullets[wch_b_t][5], bullets[wch_b_t][6],
                                                              bullets[wch_b_t][7],
                                                              bullets[wch_b_t][8], scene.width(), scene.height(),
                                                              bullets[wch_b_t][9],bullets[wch_b_t][10])
            bullet.creation_pattern = lambda obj: obj.setPos(QPointF(player.x() + (player.size_x * player.direction) +
                                                                     (bullets[wch_b_t][6] * (player.direction - 1)),
                                                                     (player.y() + player.size_y // 2) -
                                                                     bullets[wch_b_t][7] // 2))
            bullet.pos_create()
            bullet.setZValue(1)
            if player.direction == 1:
                bullet.move_direction_R = 1
                bullet.move_direction_L = 0
            else:
                bullet.move_direction_L = 1
                bullet.move_direction_R = 0

            array_bullets.append(bullet)
            return bullet



