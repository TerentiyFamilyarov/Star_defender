import locale
import random
from math import sin, pi, cos

from PyQt6.QtCore import QTimer, QRectF, Qt
from PyQt6.QtGui import QColor, QPen, QBrush, QImage, QPixmap, QPainterPath, QPainter
from PyQt6.QtWidgets import QGraphicsRectItem


difficult_koef = 1

enemies = []
hp = []
damage = []
step = []
speed_shoot = []
size_x = []
size_y = []
picture = []
def update_enemies_list():
    global enemies
    enemies = [
        ('Default',      int(3*difficult_koef),  (2*difficult_koef), (1*difficult_koef), 0, 30, 30, 'arrow_right.png', 0),  # 45x45
        ('Ping_pong',    int(1*difficult_koef),  (1*difficult_koef), (3*difficult_koef), 0, 20, 20, 'arrow_right.png', 1),
        ('Mother',       int(5*difficult_koef),  (0*difficult_koef), (0.5*difficult_koef), 500, 35, 35, 'arrow_right.png', 2),
        ('Child',        int(1*difficult_koef),  (1*difficult_koef), (2*difficult_koef), 0, 20, 20, 'arrow_right.png', 3),
        ('Static, so-so',int(10*difficult_koef), (1*difficult_koef), (0.5*difficult_koef), 0, 20, 60,         'arrow_right.png', 4),
        ('Boss',         int(100*difficult_koef),(3*difficult_koef), (1*difficult_koef), 2000, 200, 200,      'arrow_right.png', 5)
    ]
    hp.clear()
    damage.clear()
    step.clear()
    speed_shoot.clear()
    size_x.clear()
    size_y.clear()
    picture.clear()
    for i in range(len(enemies)):
        hp.append(enemies[i][1])
        damage.append(enemies[i][2])
        step.append(enemies[i][3])
        speed_shoot.append(enemies[i][4])
        size_x.append(enemies[i][5])
        size_y.append(enemies[i][6])
        picture.append(enemies[i][7])
update_enemies_list()
array_enemies = []
timer = QTimer()
timer.timeout.connect(timer.stop)

class Enemy(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.type = -1
        self.pixmap = QPixmap()
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

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter: QPainter, option, widget=None):
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(QBrush(self.pixmap.scaled(self.size_x,self.size_y)))
        painter.drawRect(self.rect())

    def update_size(self,size_x,size_y):
        self.setRect(0,0,size_x,size_y)
        self.size_x = size_x
        self.size_y = size_y
        self.setTransformOriginPoint(self.rect().center())

def delete_enemy(scene,enemy):
    array_enemies.remove(enemy)
    scene.removeItem(enemy)

def default_enemy(scene):
    type = 0
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]

    enemy.pixmap = QPixmap(picture[type])
    enemy.update_size(enemy.size_x,enemy.size_y)
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width()+1),int(scene.width())-int(scene.width()*1.2))
    y = random.randint(0,int(scene.height()-enemy.size_y))
    enemy.setPos(random.choice((x1,x2)),y)
    enemy.direction = random.choice((-1,1))
    enemy.angle = 0
    def move():
        if enemy.direction == -1:
            enemy.direction = 1
            enemy.angle += 180
        if enemy.angle > 360:
            enemy.angle -= 360
        elif enemy.angle < -360:
            enemy.angle += 360
        move_scale_x = cos(enemy.angle * (pi / 180)) * enemy.step
        move_scale_y = sin(enemy.angle * (pi / 180)) * enemy.step

        if enemy.rotation() != enemy.angle:
            enemy.setRotation(enemy.angle)
        enemy.moveBy(move_scale_x, move_scale_y)
    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    enemy.setZValue(3)
    return enemy

def ping_pong_enemy(scene):
    type = 1
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    enemy.pixmap = QPixmap(picture[type])
    enemy.update_size(enemy.size_x, enemy.size_y)
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width()+1),int(scene.width())-int(scene.width()*1.2))
    y = random.randint(0,int(scene.height()-enemy.size_y))
    enemy.setPos(random.choice((x1,x2)),y)
    enemy.direction = random.choice((-1,1))
    enemy.angle = random.randint(30,330)

    def move():
        if int(enemy.y() + (sin(enemy.angle * (pi / 180)) * enemy.step)) < 0 or int(
                enemy.y() + enemy.rect().height() + (sin(enemy.angle * (pi / 180)) * enemy.step)) > scene.height():
            enemy.angle *= -1
        if enemy.direction == -1:
            enemy.direction = 1
            enemy.angle += 180
        if enemy.angle > 360:
            enemy.angle -= 360
        elif enemy.angle < -360:
            enemy.angle += 360
        move_scale_x = cos(enemy.angle * (pi / 180)) * enemy.step
        move_scale_y = sin(enemy.angle * (pi / 180)) * enemy.step

        if enemy.rotation() != enemy.angle:
            enemy.setRotation(enemy.angle)
        enemy.moveBy(move_scale_x,move_scale_y)
    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    enemy.setZValue(2)
    return enemy


def child_enemy(scene):
    type = 3
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    enemy.pixmap = QPixmap(picture[type])
    enemy.update_size(enemy.size_x, enemy.size_y)
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width() + 1), int(scene.width()) - int(scene.width() * 1.2))
    y = random.randint(0, int(scene.height() - enemy.size_y))
    enemy.setPos(random.choice((x1, x2)), y)
    enemy.direction = random.choice((-1, 1))

    move_proportion_x = 1
    move_proportion_y = 1
    enemy.future_x = enemy.x() - enemy.step
    def move():

        enemy.angle += random.randint(-1, 1)
        if enemy.direction == -1:
            enemy.direction = 1
            enemy.angle += 180
        if enemy.angle > 360:
            enemy.angle -= 360
        elif enemy.angle < -360:
            enemy.angle += 360
        move_scale_x = cos(enemy.angle * (pi / 180)) * enemy.step
        move_scale_y = sin(enemy.angle * (pi / 180)) * enemy.step

        if enemy.rotation() != enemy.angle:
            enemy.setRotation(enemy.angle)
        enemy.moveBy(move_scale_x,move_scale_y)
    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    enemy.setZValue(2)
    return enemy

def mother_enemy(scene):
    type = 2
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    enemy.pixmap = QPixmap(picture[type])
    enemy.update_size(enemy.size_x, enemy.size_y)
    x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
    x2 = random.randint(-int(scene.boundingField().width() + 1), int(scene.width()) - int(scene.width() * 1.2))
    y = random.randint(0, int(scene.height() - enemy.size_y))
    enemy.setPos(random.choice((x1, x2)), y)
    distance = random.randint(150,500)
    spread = 30
    distance_size = distance + spread + enemy.step + 100
    center_distance = distance + ((spread+enemy.step)/2)
    enemy.angle_for_move = 0
    enemy.direction = 1
    main_y_pos = enemy.y()
    def move():
        enemy_x_center = enemy.x()+(enemy.size_x/2)
        enemy_y_center = enemy.y()+(enemy.size_y/2)
        player_x_center = scene.player.x()+(scene.player.size_x/2)
        player_y_center = scene.player.y()+(scene.player.size_y/2)
        enemy_distance_from_player = abs(abs(enemy_x_center)-player_x_center)

        if enemy_distance_from_player > distance_size:
            if enemy_x_center > player_x_center:
                enemy.angle_for_move = 180
            else:
                enemy.angle_for_move = 0
        elif enemy_distance_from_player+(distance//3) < distance:
            if enemy_x_center > player_x_center:
                enemy.angle_for_move = 0
            else:
                enemy.angle_for_move = 180

        if not (distance < enemy_distance_from_player < distance_size):
            if enemy.direction == -1:
                enemy.direction = 1
                enemy.angle_for_move += 180
            if enemy.angle_for_move > 360:
                enemy.angle_for_move -= 360
            elif enemy.angle_for_move < -360:
                enemy.angle_for_move += 360
            move_scale_x = cos(enemy.angle_for_move * (pi / 180)) * enemy.step
            move_scale_y = sin(enemy.angle_for_move * (pi / 180)) * enemy.step

            if enemy.rotation() != enemy.angle_for_move:
                enemy.setRotation(enemy.angle_for_move)
            enemy.moveBy(move_scale_x, move_scale_y)
        else:
            if enemy.timer.isActive() is False:
                enemy.timer.start(speed_shoot[type])
            if player_x_center < enemy_x_center:
                enemy.angle_for_move = 180
            else:
                enemy.angle_for_move = 0
            if enemy.rotation() != enemy.angle_for_move:
                enemy.setRotation(enemy.angle_for_move)

            if abs(enemy_distance_from_player-center_distance) < spread/2 and abs(main_y_pos-enemy.y()) < spread/2:
                enemy.moveBy(cos(enemy.angle*(pi/180))*0.3,sin(enemy.angle*(pi/180))*0.3)
            else:
                enemy.moveBy(-cos(enemy.angle * (pi / 180)) * 0.3,
                             -sin(enemy.angle * (pi / 180)) * 0.3)
                enemy.angle = random.randint(0,360)

    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    enemy.setZValue(3)

    def create():
        if not (enemy in array_enemies):
            enemy.timer.disconnect()
            enemy.timer.deleteLater()
            return
        if enemy.isVisible() is True:
            child = child_enemy(scene)
            if child != None:
                child.setPos(enemy.x()+((enemy.size_x//2) - (child.size_x//2)),enemy.y()+((enemy.size_y//2) - (child.size_y//2)))
                child.angle = random.randint(0,360)
                enemy.setZValue(2)

    enemy.timer.timeout.connect(enemy.timer.stop)
    enemy.timer.timeout.connect(create)

    return enemy


def static_ss_enemy(scene):
    type = 4
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    enemy.pixmap = QPixmap(picture[type])
    enemy.update_size(enemy.size_x, enemy.size_y)
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
    enemy.setZValue(3)
    return enemy

def boss_enemy(scene):
 type = 5
 if random.randint(0,100) <= 1:
    enemy = Enemy()
    enemy.type = type
    enemy.size_x, enemy.size_y = size_x[type], size_y[type]
    enemy.step = step[type]
    enemy.damage = damage[type]
    enemy.hp = hp[type]
    enemy.pixmap = QPixmap(picture[type])
    enemy.update_size(enemy.size_x, enemy.size_y)
    x = scene.width() + 10
    y = abs(enemy.size_y-scene.height())/2
    enemy.setPos(x, y)
    distance = 500
    spread = 50
    distance_size = distance + spread + enemy.step + 100
    center_distance = distance + ((spread + enemy.step) / 2)
    enemy.direction = 1
    enemy.angle_for_move = 0
    main_y_pos = enemy.y()

    def move():
        if enemy.isVisible() is False:
            enemy.step = step[type] + abs(scene.width()-enemy.x())//2
        else:
            enemy.step = step[type]
        enemy_x_center = enemy.x() + (enemy.size_x / 2)
        enemy_y_center = enemy.y() + (enemy.size_y / 2)
        player_x_center = scene.player.x() + (scene.player.size_x / 2)
        player_y_center = scene.player.y() + (scene.player.size_y / 2)
        enemy_distance_from_player = abs(abs(enemy_x_center) - player_x_center)
        if enemy_distance_from_player > distance_size:
            if enemy_x_center > player_x_center:
                enemy.angle_for_move = 180
            else:
                enemy.angle_for_move = 0
        elif enemy_distance_from_player+(distance//3) < distance:
            if enemy_x_center > player_x_center:
                enemy.angle_for_move = 0
            else:
                enemy.angle_for_move = 180

        if not (distance < enemy_distance_from_player < distance_size):

            if enemy.direction == -1:
                enemy.direction = 1
                enemy.angle_for_move += 180
            if enemy.angle_for_move > 360:
                enemy.angle_for_move -= 360
            elif enemy.angle_for_move < -360:
                enemy.angle_for_move += 360
            move_scale_x = cos(enemy.angle_for_move * (pi / 180)) * enemy.step
            move_scale_y = sin(enemy.angle_for_move * (pi / 180)) * enemy.step

            if enemy.rotation() != enemy.angle_for_move:
                enemy.setRotation(enemy.angle_for_move)
            enemy.moveBy(move_scale_x, move_scale_y)
        else:
            if enemy.timer.isActive() is False:
                enemy.timer.start(speed_shoot[type])
            if player_x_center < enemy_x_center:
                enemy.angle_for_move = 180
            else:
                enemy.angle_for_move = 0
            if enemy.rotation() != enemy.angle_for_move:
                enemy.setRotation(enemy.angle_for_move)

            if abs(enemy_distance_from_player - center_distance) < spread / 2 and abs(
                    main_y_pos - enemy.y()) < spread / 2:
                enemy.moveBy(cos(enemy.angle * (pi / 180)) * 0.3,
                             sin(enemy.angle * (pi / 180)) * 0.3)
            else:
                enemy.moveBy(-cos(enemy.angle * (pi / 180)) * 0.3,
                             -sin(enemy.angle * (pi / 180)) * 0.3)
                enemy.angle = random.randint(0, 360)

    enemy.move = move
    scene.addItem(enemy)
    array_enemies.append(enemy)
    enemy.setZValue(3)
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
                child = random.choice((child_enemy,ping_pong_enemy))
                child = child(scene)
                if child != None:
                    child.angle = a1 + d * (i - 1)
                    child.setPos(enemy.x()+((enemy.size_x//2) - (child.size_x//2)),enemy.y()+((enemy.size_y//2) - (child.size_y//2)))
                    child.size_x = int(child.size_x*1.5)
                    child.size_y = int(child.size_y*1.5)
                    child.update_size(child.size_x, child.size_y)
                    child.damage *= 2
                    enemy.setZValue(2)
            if enemy.bullet_count < 20:
                enemy.bullet_count += 1

    enemy.timer.timeout.connect(enemy.timer.stop)
    enemy.timer.timeout.connect(create)

    return enemy

list_of_types = [
    default_enemy,
    ping_pong_enemy,
    child_enemy,
    mother_enemy,
    boss_enemy
]

