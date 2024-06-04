import locale
import random
from math import sin, pi, cos

from PyQt6.QtCore import QTimer, QRectF, Qt
from PyQt6.QtGui import QColor, QPen, QBrush, QImage, QPixmap, QPainterPath, QPainter
from PyQt6.QtWidgets import QGraphicsRectItem

        # enemies = [ (name, hp, damage, step, speed_shoot, size_x, size_y, picture_name, type, max_count) ]
enemies = [
            ('Default',      3,  2,      1,          0,       30,     30,      'arrow_right.png',0,15),#45x45
            ('Ping_pong',    1,  1,      3,          0,       20,     20,      'arrow_right.png',1,10),
            ('Mother',       5,  0,      0.5,        500,     35,     35,      'arrow_right.png',2,3),
            ('Child',        1,  1,      2,          0,       20,     20,      'arrow_right.png',3,30),
            ('Static, so-so',10, 1,      0.5,        0,       20,     60,      'arrow_right.png',4,10),
            ('Boss',         100,3,      1,          2000,    200,    200,    'arrow_right.png',5,1)
        ]

hp = []
damage = []
step = []
speed_shoot = []
size_x = []
size_y = []
picture = []
type_count = []
max_count = []
for i in range(len(enemies)):
    hp.append(enemies[i][1])
    damage.append(enemies[i][2])
    step.append(enemies[i][3])
    speed_shoot.append(enemies[i][4])
    size_x.append(enemies[i][5])
    size_y.append(enemies[i][6])
    picture.append(enemies[i][7])
    type_count.append(0)
    max_count.append(enemies[i][9])
array_enemies = []
timer = QTimer()
timer.timeout.connect(timer.stop)

class Enemy(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        # self.setRect()
        # self.setPen(QPen(Qt.PenStyle.NoPen))
        self.type = -1
        # self.setBrush(brush)
        self.brush = QBrush(QColor(0,0,0))
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
        self.angle = 0
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

    def boundingRect(self):
        return self.rect()
        # return QRectF(self.x(),self.y(),self.size_x,self.size_y)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter: QPainter, option, widget=None):
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(self.brush)
        painter.drawRect(self.rect())
        # painter.setBrush(QBrush(Qt.GlobalColor.red))
        # painter.drawPath(self.shape())


def delete_enemy(scene,enemy):
    array_enemies.remove(enemy)
    scene.removeItem(enemy)
    type_count[enemy.type] -= 1

def default_enemy(scene):
    type = 0
    if type_count[type] >= max_count[type]:
        return None
    type_count[type] += 1
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]

    pm = QPixmap(picture[type])
    scled_pm = pm.scaled(enemy.size_x, enemy.size_y)
    # enemy.setBrush(QBrush(scled_pm))
    enemy.brush = QBrush(scled_pm)
    enemy.setRect(0,0,enemy.size_x,enemy.size_y)
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width()+1),int(scene.width())-int(scene.width()*1.2))
    y = random.randint(0,int(scene.height()-enemy.size_y))
    enemy.setPos(random.choice((x1,x2)),y)
    enemy.direction = random.choice((-1,1))
    enemy.angle = random.randint(-15,15)
    enemy.setTransformOriginPoint(enemy.rect().center())
    def move():
        if enemy.direction == -1:
            enemy.direction = 1
            enemy.angle += 180
        if enemy.angle >= 360:
            enemy.angle -= 360
        elif enemy.angle <= -360:
            enemy.angle += 360
        move_scale_x = cos(enemy.angle * (pi / 180)) * enemy.step
        move_scale_y = sin(enemy.angle * (pi / 180)) * enemy.step

        if enemy.rotation() != enemy.angle:
            enemy.setRotation(enemy.angle)
        enemy.moveBy(move_scale_x, move_scale_y)
    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    return enemy

def ping_pong_enemy(scene):
    type = 1
    if type_count[type] >= max_count[type]:
        return None
    type_count[type] += 1
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    pm = QPixmap(picture[type])
    scled_pm = pm.scaled(enemy.size_x, enemy.size_y)
    # enemy.setBrush(QBrush(scled_pm))
    enemy.brush = QBrush(scled_pm)
    enemy.setRect(0,0,enemy.size_x,enemy.size_y)
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width()+1),int(scene.width())-int(scene.width()*1.2))
    y = random.randint(0,int(scene.height()-enemy.size_y))
    enemy.setPos(random.choice((x1,x2)),y)
    enemy.direction = random.choice((-1,1))
    enemy.angle = random.randint(5,355)
    enemy.setTransformOriginPoint(enemy.rect().center())

    def move():
        if int(enemy.y() - enemy.step) < 0 or int(enemy.y() + enemy.rect().height() + enemy.step) > scene.height():
            enemy.angle *= -1
        if enemy.direction == -1:
            enemy.direction = 1
            enemy.angle += 180
        if enemy.angle >= 360:
            enemy.angle -= 360
        elif enemy.angle <= -360:
            enemy.angle += 360
        move_scale_x = cos(enemy.angle * (pi / 180)) * enemy.step
        move_scale_y = sin(enemy.angle * (pi / 180)) * enemy.step

        if enemy.rotation() != enemy.angle:
            enemy.setRotation(enemy.angle)
        enemy.moveBy(move_scale_x,move_scale_y)
    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    return enemy


def child_enemy(scene):
    type = 3
    if type_count[type] >= max_count[type]:
        return None
    type_count[type] += 1
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    pm = QPixmap(picture[type])
    scled_pm = pm.scaled(enemy.size_x, enemy.size_y)
    # enemy.setBrush(QBrush(scled_pm))
    enemy.brush = QBrush(scled_pm)
    enemy.setRect(0, 0, enemy.size_x, enemy.size_y)
    # x = 400
    # y = 150
    # enemy.setPos(x,y)
    # enemy.direction = -1
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width() + 1), int(scene.width()) - int(scene.width() * 1.2))
    y = random.randint(0, int(scene.height() - enemy.size_y))
    enemy.setPos(random.choice((x1, x2)), y)
    enemy.direction = random.choice((-1, 1))
    enemy.setTransformOriginPoint(enemy.rect().center())

    move_proportion_x = 1
    move_proportion_y = 1
    enemy.future_x = enemy.x() - enemy.step
    def move():

        enemy.angle += random.randint(-1, 1)
        if enemy.direction == -1:
            enemy.direction = 1
            enemy.angle += 180
        if enemy.angle >= 360:
            enemy.angle -= 360
        elif enemy.angle <= -360:
            enemy.angle += 360
        move_scale_x = cos(enemy.angle * (pi / 180)) * enemy.step
        move_scale_y = sin(enemy.angle * (pi / 180)) * enemy.step

        if enemy.rotation() != enemy.angle:
            enemy.setRotation(enemy.angle)
        enemy.moveBy(move_scale_x,move_scale_y)
    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    return enemy

def mother_enemy(scene):
    type = 2
    if type_count[type] >= max_count[type]:
        return None
    type_count[type] += 1
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    pm = QPixmap(picture[type])
    scled_pm = pm.scaled(enemy.size_x, enemy.size_y)
    # enemy.setBrush(QBrush(scled_pm))
    enemy.brush = QBrush(scled_pm)
    enemy.setRect(0, 0, enemy.size_x, enemy.size_y)
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width() + 1), int(scene.width()) - int(scene.width() * 1.2))
    y = random.randint(0, int(scene.height() - enemy.size_y))
    enemy.setPos(random.choice((x1, x2)), y)
    distance = random.randint(150,500)
    spread = 30
    distance_size = distance + spread + enemy.step
    center_distance = distance + ((spread+enemy.step)/2)
    enemy.angle_for_move = random.randint(-5,5)
    main_y_pos = enemy.y()
    def move():
        enemy_x_center = enemy.x()+(enemy.size_x/2)
        enemy_y_center = enemy.y()+(enemy.size_y/2)
        player_x_center = scene.player.x()+(scene.player.size_x/2)
        player_y_center = scene.player.y()+(scene.player.size_y/2)
        enemy_distance_from_player = abs(abs(enemy_x_center)-player_x_center)
        if enemy_distance_from_player > distance_size:
            if player_x_center < enemy_x_center:
                enemy.direction = -1
            else: enemy.direction = 1
        elif enemy_distance_from_player < distance:
            if player_x_center < enemy_x_center:
                enemy.direction = 1
            else: enemy.direction = -1
        if not (distance < enemy_distance_from_player < distance_size):
            if enemy.direction == -1:
                enemy.direction = 1
                enemy.angle_for_move += 180
            if enemy.angle_for_move >= 360:
                enemy.angle_for_move -= 360
            elif enemy.angle_for_move <= -360:
                enemy.angle_for_move += 360
            move_scale_x = cos(enemy.angle_for_move * (pi / 180)) * enemy.step
            move_scale_y = sin(enemy.angle_for_move * (pi / 180)) * enemy.step

            if enemy.rotation() != enemy.angle:
                enemy.setRotation(enemy.angle)
            enemy.moveBy(move_scale_x, move_scale_y)
        else:
            enemy.angle_for_move = 0
            if abs(enemy_distance_from_player-center_distance) < spread/2 and abs(main_y_pos-enemy.y()) < spread/2:
                enemy.moveBy(cos(enemy.angle*(pi/180))*enemy.step*0.2,sin(enemy.angle*(pi/180))*enemy.step*0.2)
            else:
                enemy.moveBy(-cos(enemy.angle * (pi / 180)) * enemy.step * 0.2,
                             -sin(enemy.angle * (pi / 180)) * enemy.step * 0.2)
                enemy.angle = random.randint(0,359)

    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    def create():
        if not (enemy in array_enemies):
            enemy.timer.disconnect()
            enemy.timer.deleteLater()
            return
        if enemy.isVisible() is True:
            child = child_enemy(scene)
            if child != None:
                child.setPos(enemy.x()+((enemy.size_x//2) - (child.size_x//2)),enemy.y()+((enemy.size_y//2) - (child.size_y//2)))
                child.angle = random.randint(0,359)
    enemy.timer = QTimer()
    enemy.timer.timeout.connect(create)
    enemy.timer.start(speed_shoot[type])

    return enemy


def static_ss_enemy(scene):
    type = 4
    if type_count[type] >= max_count[type]:
        return None
    type_count[type] += 1
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    pm = QPixmap(picture[type])
    scled_pm = pm.scaled(enemy.size_x, enemy.size_y)
    # enemy.setBrush(QBrush(scled_pm))
    enemy.brush = QBrush(scled_pm)
    enemy.setRect(0,0,enemy.size_x,enemy.size_y)
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width()+1),int(scene.width())-int(scene.width()*1.2))
    y = random.randint(0,int(scene.height()-enemy.size_y))
    enemy.setPos(random.choice((x1,x2)),y)
    enemy.direction = random.choice((-1,1))
    def move():
        enemy.moveBy(enemy.step*random.choice((-enemy.step,enemy.step)),enemy.step*random.choice((-enemy.step,enemy.step)))
    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    return enemy

def boss_enemy(scene):
    type = 5
    if type_count[type] >= max_count[type] or scene.min < 0:
        return None
    type_count[type] += 1
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    # enemy.setBrush(QBrush(color[type]))
    pm = QPixmap(picture[type])
    scled_pm = pm.scaled(enemy.size_x, enemy.size_y)
    # enemy.setBrush(QBrush(scled_pm))
    enemy.brush = QBrush(scled_pm)
    enemy.setRect(0, 0, enemy.size_x, enemy.size_y)
    x = scene.width() + 10
    y = abs(enemy.size_y-scene.height())/2
    enemy.setPos(x, y)
    distance = 500
    spread = 50
    distance_size = distance + spread + enemy.step
    center_distance = distance + ((spread + enemy.step) / 2)
    main_y_pos = enemy.y()

    def move():
        if enemy.isVisible() is False:
            enemy.step = step[type] + abs(abs(scene.width()-enemy.x())-1)
        else:
            enemy.step = step[type]
        enemy_x_center = enemy.x() + (enemy.size_x / 2)
        enemy_y_center = enemy.y() + (enemy.size_y / 2)
        player_x_center = scene.player.x() + (scene.player.size_x / 2)
        player_y_center = scene.player.y() + (scene.player.size_y / 2)
        enemy_distance_from_player = abs(abs(enemy_x_center) - player_x_center)
        if enemy_distance_from_player > distance_size:
            if player_x_center < enemy_x_center:
                enemy.direction = -1
            else:
                enemy.direction = 1
        elif enemy_distance_from_player < distance:
            if player_x_center < enemy_x_center:
                enemy.direction = 1
            else:
                enemy.direction = -1
        if not (distance < enemy_distance_from_player < distance_size):
            enemy.moveBy(enemy.step * enemy.direction, 0)
        else:
            if abs(enemy_distance_from_player - center_distance) < spread / 2 and abs(
                    main_y_pos - enemy.y()) < spread / 2:
                enemy.moveBy(cos(enemy.angle * (pi / 180)) * 0.1,
                             sin(enemy.angle * (pi / 180)) * 0.1)
            else:
                enemy.moveBy(-cos(enemy.angle * (pi / 180)) * 0.1,
                             -sin(enemy.angle * (pi / 180)) * 0.1)
                enemy.angle = random.randint(0, 359)

    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    enemy.bullet_count = 5
    def create():
        if not (enemy in array_enemies):
            enemy.timer.disconnect()
            enemy.timer.deleteLater()
            return
        if enemy.isVisible() is True:
            for i in range(1, enemy.bullet_count + 1):
                a1 = 360
                max_a = -a1
                d = (max_a - a1) / (enemy.bullet_count - 1)
                child = child_enemy(scene)
                if child != None:
                    child.setScale(2)
                    child.angle = a1 + d * (i - 1)
                    child.setPos(enemy.x()+((enemy.size_x//2) - (child.size_x//2)),enemy.y()+((enemy.size_y//2) - (child.size_y//2)))
                    child.size_x *= 2
                    child.size_y *= 2
                    # child.setRect(0,0,child.size_x,child.size_y)
                    child.damage *= 2
            if enemy.bullet_count < 20:
                enemy.bullet_count += 1

    enemy.timer = QTimer()
    enemy.timer.timeout.connect(create)
    enemy.timer.start(speed_shoot[type])

    return enemy



