
import random
from math import sin

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor
def default_move(obj):
    if obj.move_direction_L == 0 and obj.move_direction_R == 0:
        obj.move_direction_L = random.randint(0,1)
        if obj.move_direction_L == 0:
            obj.move_direction_R = 1

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

def zlike_move(obj):
    if obj.move_direction_L == 0 and obj.move_direction_R == 0 and obj.move_direction_U == 0 and obj.move_direction_D == 0:
        obj.move_direction_L = random.randint(0,1)
        if obj.move_direction_L == 0:
            obj.move_direction_R = 1
        obj.move_direction_U = random.randint(0,1)
        if obj.move_direction_U == 0:
            obj.move_direction_D = 1



    if obj.y() - obj.step < 0:
        obj.move_direction_U = 0
        obj.move_direction_D = 1
    elif obj.y() + obj.size_y + obj.step > obj.window_y:
        obj.move_direction_U = 1
        obj.move_direction_D = 0

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
        # enemies = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color,                 move_pattern, parameters) ]
enemies = [
            ('Default',      3,  1,      1,    0,         0,           35,     35,      QColor(150, 0, 0),     default_move, None),#45x45
            ('Tiny',         1,  1,      3,    0,         0,           15,     15,      QColor(255, 111, 0),   zlike_move,   None),
            ('Fat',          5,  1,      0.5,  0,         0,           40,     40,      QColor(255, 111, 111), default_move, None),
        ]
array_enemies = []
timer = QTimer()

def create_enemy(scene, spawn_cd: int,max_enemies_count, array_enemies: list, enemies: list, wch_e_t: int):
    if timer.isActive() is False and len(array_enemies) < max_enemies_count:
        # enemy = self.create_rectobj(self,self.enemy_timer,1000,self.enemies[0][1],self.enemies[0][2],self.enemies[0][3],self.enemies[0][4],self.enemies[0][5],self.enemies[0][6],self.enemies[0][7],self.enemies[0][8],self.width(),self.height())
        enemy = scene.create_rectobj_podclass_from_class(scene, timer, spawn_cd, enemies[wch_e_t][1],
                                                        enemies[wch_e_t][2], enemies[wch_e_t][3], enemies[wch_e_t][4],
                                                        enemies[wch_e_t][5], enemies[wch_e_t][6], enemies[wch_e_t][7],
                                                        enemies[wch_e_t][8], scene.width(), scene.height(), enemies[wch_e_t][9],
                                                        enemies[wch_e_t][10])
        enemy.setZValue(2)
        randint_y = random.randint(0, int(scene.height() - enemy.size_y))
        randint_x1 = random.randint(int(scene.boundingField().x()), int(scene.boundingField().x() * 0.2))
        randint_x2 = random.randint(int(scene.width() * 0.6),
                                    int(scene.boundingField().width()))  # появление врагов дожно быть не ближе чем 2 экрана (direction)
        randint_x_choice = random.randint(0, 2)
        if randint_x_choice == 0:
            enemy.creation_pattern = lambda obj: obj.setPos(randint_x1, randint_y)  # переделать
        else:
            enemy.creation_pattern = lambda obj: obj.setPos(randint_x2, randint_y)  # переделать
        enemy.pos_create()
        array_enemies.append(enemy)
        return enemy

