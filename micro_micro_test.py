import sys
from math import ceil, sqrt
import random

from PyQt6.QtCore import QPoint, QSize, QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QBrush
from PyQt6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsView, QGraphicsScene


class StartGame(QGraphicsScene):
    def __init__(self, menu, game_begin=False):
        super().__init__()
        self.game_begin = game_begin
        self.menu = menu

        self.setSceneRect(0,0,1120,(600*0.8))
        self.setBackgroundBrush(QColor(100,100,100))
        self.addRect(self.boundingRect(),QColor('black'),QBrush(QColor('black')))


        self.previous_size = QSize()

        self.count_restart_sec = 3

        self.mode = 0

        self.sec = -1
        self.min = 0

        # players = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.players = [
            ('Default',      3,  1,      8,   25,        370,         30,     30,     QColor(0, 0, 255)),
            ('IFeelPain',    1,  0.5,    16,   40,        290,         35,     35,     QColor(200, 150, 0)),
            ('UPower',       5,  2,      7,    15,        420,         65,     65,     QColor(100, 255, 255))
        ]
        # players = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.enemies = [
            ('Default',      3,  1,      0.4,    0,         0,           45,     45,     QColor(255, 0, 0)),
            ('Tiny',         1,  1,      3,    0,         0,           35,     35,     QColor(255, 111, 0)),
            ('Fat',          5,  1,      0.5,  0,         0,           85,     85,     QColor(255, 111, 111)),
        ]

        self.player2_timer = QTimer()
        self.player2_chtimer = QTimer()
        self.player2 = self.create_rectobj(self.player2_timer,1, self.players[0][1], self.players[0][2], self.players[0][3],self.players[0][4],self.players[0][5],self.players[0][6],self.players[0][7],self.players[0][8],self.width(),self.height())
        self.player2.setPos(200,300)
        self.player2.direction = 1
        self.player2.speed_l_ch = 0
        self.player2.speed_r_ch = 0
        self.array_enemies = []
        self.enemy_timer = QTimer()
        self.array_bullets = []
        self.bullet_timer = QTimer()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScene)
        self.timer.start(10)
        self.enemy_timer = QTimer(self)
        self.bullet_timer1 = QTimer(self)

    def boundingRect(self):
        # return QRectF(-100, -100, (self.scene.width() + 200), (self.scene.height() + 200))
        return QRectF(0,0,self.width(),self.height())

    def boundingField(self):
        return QRectF(-1000, 0, (self.width() + 2000), (self.height()))

    def create_rectobj(self,timer,cd,hp,damage,step,soap_koef,speed_shoot,size_x,size_y,color,window_x,wimdow_y):
        if timer.isActive() is False:
            rectobj = self.addRect(QRectF(0,0,size_x,size_y),QColor(color),QBrush(color))
            rectobj.move_direction_L = 0
            rectobj.move_direction_R = 0
            rectobj.move_direction_U = 0
            rectobj.move_direction_D = 0
            rectobj.shoot = 0
            rectobj.speed_l = 0
            rectobj.speed_r = 0
            rectobj.speed_u = 0
            rectobj.speed_d = 0
            rectobj.hp = hp
            rectobj.damage = damage
            rectobj.step = step
            rectobj.soap_koef = soap_koef
            rectobj.speed_shoot = speed_shoot
            rectobj.size_x = size_x
            rectobj.size_y = size_y
            rectobj.window_x = window_x
            rectobj.window_y = wimdow_y
            timer.start(cd)
            timer.timeout.connect(timer.stop)
            return rectobj

    def set_default_rectobj(self,name,hp,damage,step,soap_koef,speed_shoot,size_x,size_y,color):
        name.hp = hp
        name.damage = damage
        name.step = step
        name.soap_koef = soap_koef
        name.speed_shoot = speed_shoot
        name.size_x = size_x
        name.size_y = size_y
        name.setPen(color)
        name.setBrush(color)


    def new_move(self,obj):
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

            obj.moveBy(-obj.speed_l + obj.speed_r,-obj.speed_u + obj.speed_d)


    def player_move(self,obj,timer,arrays:list):
        if timer.isActive() is False:
            if obj.speed_l < obj.step * 0.1 and obj.move_direction_L == 1:
                obj.speed_l = obj.step * 0.1
            elif obj.speed_l < obj.step and obj.move_direction_L == 1:
                obj.speed_l += 0.5
            elif obj.move_direction_L == 0 and obj.speed_l > 0:
                obj.speed_l -= 0.5
            elif obj.speed_l < 0:
                obj.speed_l = 0

            if obj.speed_r < obj.step * 0.1 and obj.move_direction_R == 1:
                obj.speed_r = obj.step * 0.1
            elif obj.speed_r < obj.step and obj.move_direction_R == 1:
                obj.speed_r += 0.5
            elif obj.move_direction_R == 0 and obj.speed_r > 0:
                obj.speed_r -= 0.5
            elif obj.speed_r < 0:
                obj.speed_r = 0

            if obj.speed_u < obj.step * 0.1 and obj.move_direction_U == 1:
                obj.speed_u = obj.step * 0.1
            elif obj.speed_u < obj.step and obj.move_direction_U == 1:
                obj.speed_u += 0.5
            elif obj.move_direction_U == 0 and obj.speed_u > 0:
                obj.speed_u -= 0.5
            elif obj.speed_u < 0:
                obj.speed_u = 0

            if obj.speed_d < obj.step * 0.1 and obj.move_direction_D == 1:
                obj.speed_d = obj.step * 0.1
            elif obj.speed_d < obj.step and obj.move_direction_D == 1:
                obj.speed_d += 0.5
            elif obj.move_direction_D == 0 and obj.speed_d > 0:
                obj.speed_d -= 0.5
            elif obj.speed_d < 0:
                obj.speed_d = 0

            timer.timeout.connect(timer.stop)
            timer.start(int(obj.soap_koef))

        if obj.x() + obj.speed_l < 0:
            obj.setX(0)
            obj.speed_l = 0
        else:
            for array in arrays:
                for arr_obj in array:
                    arr_obj.moveBy(obj.speed_l+obj.speed_l_ch, 0)

        if obj.x() + obj.speed_r + obj.size_x > obj.window_x:
            obj.setX(obj.window_x - obj.size_x)
            obj.speed_r = 0
        else:
            for array in arrays:
                for arr_obj in array:
                    arr_obj.moveBy(-obj.speed_r-obj.speed_r_ch, 0)

        if obj.y() + obj.speed_u < 0:
            obj.setY(0)
            obj.speed_u = 0
        else:
            obj.moveBy(0, -obj.speed_u)

        if obj.y() + obj.speed_d + obj.size_y > obj.window_y:
            obj.setY(obj.window_y - obj.size_y)
            obj.speed_d = 0
        else:
            obj.moveBy(0, obj.speed_d)


    def player_move2(self,obj,timer,arrays:list):
        if timer.isActive() is False:
           if obj.move_direction_L == 1:
              # 1 - скорость всех обьектов больше, чем ожидалось
              # 2 - нужно как то сделать передвижение по логарифму для игрока

            timer.timeout.connect(timer.stop)
            timer.start(int(obj.soap_koef))

    def player_chdirection(self,obj,chdirection_timer,msec,direction,future_x):
        if chdirection_timer.isActive() is False:
            ch_speed = round(sqrt(int(abs(future_x-obj.x()))),2)
            # ch_speed = round(0.05*(abs(int(future_x-obj.x()))),2)
            if ch_speed < 0.3:
                ch_speed = 0.3
            if direction == 0:
                obj.moveBy(ch_speed,0)
                obj.speed_l_ch = ch_speed
                obj.speed_r_ch = 0
            else:
                obj.moveBy(-ch_speed, 0)
                obj.speed_r_ch = ch_speed
                obj.speed_l_ch = 0

            chdirection_timer.timeout.connect(chdirection_timer.stop)
            chdirection_timer.start(msec)


    # def create_obj(self,cd,timer,array_objs,pos,hp,damage,step,speed_shoot,x_size,y_size,color):
    #     if timer.isActive() is False:
    #         obj = MovingObject(pos[0], pos[1], hp, damage, step,  speed_shoot,
    #                                     x_size, y_size, self.width(), self.height())
    #         obj.set_default()
    #         obj.draw_color = color
    #         obj.setBrush(QColor(color))
    #         array_objs.append(obj)
    #         timer.start(cd)
    #         timer.timeout.connect(timer.stop)
    #         return obj

    def check_collision(self):
        # if self.player1.HP_O <= 0:
            # self.menu.stackWidget.setCurrentWidget(self.menu.game_over_page)
        # Проверяем столкновение пуль с врагами
        for enemy in self.array_enemies:
            if QRectF(self.player2.x(),self.player2.y(),self.player2.size_x,self.player2.size_y).intersects(QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y)):
                if self.player2.x() + self.player2.size_x // 2 < enemy.x():
                    self.player2.speed_l = self.player2.step * 1
                    self.player2.speed_r = 0
                    self.player2.hp -= enemy.damage
                elif self.player2.x() + self.player2.size_x // 2 > enemy.x() + enemy.size_x:
                    self.player2.speed_r = self.player2.step * 1
                    self.player2.speed_l = 0
                    self.player2.hp -= enemy.damage
                elif self.player2.y() + self.player2.size_y // 2 < enemy.y():  # Отталкивание игрока от врага
                    self.player2.speed_u = self.player2.step * 1
                    self.player2.speed_d = 0
                    self.player2.hp -= enemy.damage
                elif self.player2.y() + self.player2.size_y // 2 > enemy.y() + enemy.size_y:
                    self.player2.speed_d = self.player2.step * 1
                    self.player2.speed_u = 0
                    self.player2.hp -= enemy.damage

            if self.boundingField().contains(QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y)) is False:
                self.array_enemies.remove(enemy)
                self.removeItem(enemy)
            for bullet in self.array_bullets:
                if self.boundingRect().intersects(QRectF(bullet.x(),bullet.y(),bullet.size_x,bullet.size_y)) is False:
                    self.array_bullets.remove(bullet)
                    self.removeItem(bullet)
                    continue
                if enemy.x() <= self.width() - (enemy.size_x // 2):
                    if QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y).intersects(QRectF(bullet.x(),bullet.y(),bullet.size_x,bullet.size_y)):
                        self.array_bullets.remove(bullet)
                        self.removeItem(bullet)
                        enemy.hp -= (bullet.damage * self.player2.damage)
                        if enemy.hp <= 0:
                            self.array_enemies.remove(enemy)
                            self.removeItem(enemy)

    def updateScene(self):
        # self.restart_timer_txt.setText(f'{self.count_restart_sec}')
        # if self.restart_timer.isActive() is False:
        #     if self.count_restart_sec > 1:
        #         self.restart_timer.start(1000)
        #         self.count_restart_sec -= 1

        # if self.menu.stackWidget.currentWidget() == self and self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
            # if self.sec == 3 or self.sec % 10 == 0 and self.sec > 0:
            #     self.menu.stackWidget.setCurrentWidget(self.menu.choose_card_page)  # Костыль, переделай
            #     self.menu.choose_card_page.randomize_cards(self)
            #
            #     self.sec += 1

            # if len(self.menu.stars) < 100:
            #     randomint = random.randint(0, 101)
            #     if randomint <= 4:
            #         self.menu.create_star(1)
            # for star in self.menu.stars:
            #     star.move_direction_L = 1
            #     # if star.max_step_x < star.primary_step*1.5:
            #     #     star.step_x += 1
            #     star.new_move(1, 0, 0)
            #     if star.x() <= -star.x_size:
            #         self.menu.reborn_star(star)

        if self.player2.shoot == 1:
                x_size = 10
                y_size = 4
                if self.bullet_timer.isActive() is False:
                    bullet = self.create_rectobj(self.bullet_timer,int(self.player2.speed_shoot),1,1,8,0,0,x_size,y_size,QColor(0,255,0),self.width(),self.height())
                    bullet.setPos(self.player2.x() + (self.player2.size_x*self.player2.direction) +
                                          (x_size*(self.player2.direction-1)),(self.player2.y() + self.player2.size_y // 2) - y_size // 2)
                    if self.player2.direction == 1:
                        bullet.move_direction_R = 1
                        bullet.move_direction_L = 0  # Почему то не изчезают пули --> они не пропадают тк врагов нет
                    else:
                        bullet.move_direction_L = 1
                        bullet.move_direction_R = 0
                    self.array_bullets.append(bullet)

        # enemy = self.create_obj(2000, self.enemy_timer, self.array_enemies,
        #                     (self.width(), random.randint(0, int(self.height()*0.8)-self.enemies[0][7])),
        #                     self.enemies[0][1], self.enemies[0][2], self.enemies[0][3], self.enemies[0][5],
        #                     self.enemies[0][6], self.enemies[0][7], self.enemies[0][8])
        if self.enemy_timer.isActive() is False:
            enemy = self.create_rectobj(self.enemy_timer,500,self.enemies[0][1],self.enemies[0][2],self.enemies[0][3],self.enemies[0][4],self.enemies[0][5],self.enemies[0][6],self.enemies[0][7],self.enemies[0][8],self.width(),self.height())
            randint_y = random.randint(0,int(self.height()-enemy.size_y))
            randint_x1 = random.randint(int(self.boundingField().x()),0)
            randint_x2 = random.randint(int(self.width()),int(self.boundingField().width()))
            randint_x_choice = random.randint(0,2)
            if randint_x_choice == 0:
                enemy.setPos(randint_x1,randint_y)
            else: enemy.setPos(randint_x2,randint_y)
            enemy.move_direction_L = 1
            self.array_enemies.append(enemy)
            # self.player1.new_move(1,1,1)
        # self.new_move(self.player2,self.player2_timer,1,1,1)
        self.player_move(self.player2,self.player2_timer,[self.array_bullets,self.array_enemies])
        left_x,right_x = 200,920
        if int(self.player2.x()) != right_x and self.player2.direction == 0:
            self.player_chdirection(self.player2,self.player2_chtimer,10,self.player2.direction,right_x)
        elif int(self.player2.x()) != left_x and self.player2.direction == 1:
            self.player_chdirection(self.player2,self.player2_chtimer,10,self.player2.direction,left_x)
        else:
            self.player2.speed_l_ch = 0
            self.player2.speed_r_ch = 0
        for bullet in self.array_bullets:
                # bullet.new_move(1, 0, 0)
            self.new_move(bullet)

        for enemy in self.array_enemies:
            self.new_move(enemy)
        self.check_collision()
        # else:
            # self.player1.new_move(0)
        # if self.isActiveWindow() is False and self.menu.stackWidget.currentWidget() == self:
        #     self.menu.stackWidget.setCurrentWidget(self.menu.pause_page)
        self.update()



    def keyPressEvent(self, event):
        # if self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
            if event.text() in ['Ц', 'ц', 'W', 'w']:
                self.player2.move_direction_U = 1

            if event.text() in ['Ф', 'ф', 'A', 'a']:
                self.player2.move_direction_L = 1
                self.player2.direction = 0

            if event.text() in ['Ы', 'ы', 'S', 's']:
                self.player2.move_direction_D = 1


            elif event.text() in ['В', 'в', 'D', 'd']:
                self.player2.move_direction_R = 1
                self.player2.direction = 1

            if event.text() in ['C', 'c', 'С', 'с']:
                self.player2.shoot = 1

            # print(self.player2.boundingRect())
            # print(self.boundingRect().x(),'x ',self.boundingRect().y(),'y ',self.boundingRect().width(),'w ',self.boundingRect().height(),'h')

            # print('Scene ',self.width(), 'w ',self.height(), 'h')
            # print(self.player1.x(),'x ',self.player1.y(),'y ',self.player1.x_size,'w ',self.player1.y_size,'h')
            # scene_coords = QPoint(int(self.player1.x()),int(self.player1.y()))
            # view_coords = self.view.mapFromScene(self.player1.x(),self.player1.y())
            # global_coords = self.view.mapToGlobal(QPoint(0,0))
            # parent_coords = self.view.mapToParent(QPoint(0,0))
            # view_coords = self.view.mapToScene(scene_coords)
            # print('scene p ->',scene_coords)
            # print('view p ->',view_coords)
            # print('global p ->',global_coords)
            # print('parent p ->',parent_coords)
            # if event.key() == Qt.Key.Key_Escape:  # кнопку надо ограничить в свое нажатии, можно прям в меню ее нажать
            #     self.menu.stackWidget.setCurrentWidget(self.menu.pause_page)

    def keyReleaseEvent(self, event):
        if event.text() in ['Ц', 'ц', 'W', 'w']:
            self.player2.move_direction_U = 0

        elif event.text() in ['Ф', 'ф', 'A', 'a']:
            self.player2.move_direction_L = 0

        elif event.text() in ['Ы', 'ы', 'S', 's']:
            self.player2.move_direction_D = 0

        elif event.text() in ['В', 'в', 'D', 'd']:
            self.player2.move_direction_R = 0

        if event.text() in ['C', 'c', 'С', 'с']:
            self.player2.shoot = 0



    # def paint(self, painter):
    #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    #     painter.fillRect(0, 0, self.width(), self.height(),
    #                      QColor(0,0,0))  # Очищаем окно, закрашивая его зеленым
    #     # for star in self.menu.stars:
    #     #     star.paint(painter)
    #
    #     painter.fillRect(0, ceil(self.height() * 0.8), self.width(), self.height(), QColor(100, 100, 100))
    #
    #     for i in range(int(self.player1.HP_O)):
    #         painter.fillRect(ceil(self.width() * 0.05) + i * (ceil(self.width() * 0.01) + 2),
    #                          ceil(self.height() * 0.82),
    #                          ceil(self.width() * 0.01), ceil(self.width() * 0.03), QColor(200, 100, 100))
    #     # self.player1.paint(painter)
    #     # for bullet in self.array_bullets:
    #     #     bullet.paint(painter)
    #     for enemy in self.array_enemies:
    #         enemy.paint(painter)
    #
    #     # if self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
    #     #     self.restart_timer_txt.hide()
    #     # else:
    #     #     self.restart_timer_txt.show()
    #     #     painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 0, 200))
    #
    # def paint_static(self):
    #     info_bar = QGraphicsRectItem(0,ceil(self.height() * 0.8),self.width(),self.height())
    #     info_bar.setBrush(QColor(100, 100, 100))
    #     self.addItem(info_bar)

# с помощью лебел можно сделать переход по словам, также модификации у обьектов должен быть как у карточек

class Game(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setGeometry(0,0,1120,600)
        self.setMinimumSize(1120,600)
        self.showMaximized()
        self.setScene(scene)
        self.setSceneRect(0,0,1120,600)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)



    def resizeEvent(self, event):
        self.fitInView(QRectF(0,0,1120,600), Qt.AspectRatioMode.KeepAspectRatio)
        # super().resizeEvent(event)
        # self.fitInView(self.sceneRect(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio) # из-за него все вылетает
        # self.fitInView(self.setSceneRect(0,0,self.width(),self.height()),Qt.AspectRatioMode.IgnoreAspectRatio)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = StartGame(None,True)
    game_window = Game(game)
    game_window.show()
    sys.exit(app.exec())