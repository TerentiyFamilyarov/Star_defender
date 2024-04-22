import sys
from math import ceil, sqrt
import random

from PyQt6.QtCore import QPoint, QSize, QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QBrush, QFont, QPixmap, QPen
from PyQt6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsView, QGraphicsScene, QGraphicsTextItem


class StartGame(QGraphicsScene):
    def __init__(self, menu, game_begin=False):
        super().__init__()
        self.game_begin = game_begin
        self.menu = menu

        self.setSceneRect(0,0,854,(480*0.8))
        self.setBackgroundBrush(QColor(0,0,0))

        # players = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.players = [
            ('Default',      3,  1,      8,   25,        370,         30,     30,     QColor(0, 0, 255)),
            ('IFeelPain',    1,  0.5,    16,   40,        290,         35,     35,     QColor(200, 150, 0)),
            ('UPower',       5,  2,      7,    15,        420,         65,     65,     QColor(100, 255, 255))
        ]
        # enemies = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.enemies = [
            ('Default',      3,  1,      0.2,    0,         0,           45,     45,     QColor(150, 0, 0)),#45x45
            ('Tiny',         1,  1,      3,    0,         0,           35,     35,     QColor(255, 111, 0)),
            ('Fat',          5,  1,      0.5,  0,         0,           85,     85,     QColor(255, 111, 111)),
        ]

        self.player2_timer = QTimer()
        self.player2_chtimer = QTimer()
        self.player2 = self.create_rectobj(self.player2_timer,1, self.players[0][1], self.players[0][2], self.players[0][3],self.players[0][4],self.players[0][5],self.players[0][6],self.players[0][7],self.players[0][8],self.width(),self.height())
        self.player2.setZValue(1)

        self.enemy_timer = QTimer()

        self.bullet_timer = QTimer()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScene)
        # self.timer.start(10)
        self.set_game_default()
        self.enemy_timer = QTimer()
        self.bullet_timer1 = QTimer()

        self.interface()


    def set_game_default(self):
        self.msec = 0
        self.sec = 0
        self.min = 0
        self.set_default_rectobj(self.player2,self.players[0][1], self.players[0][2], self.players[0][3],self.players[0][4],self.players[0][5],self.players[0][6],self.players[0][7],self.players[0][8])
        self.player2.setPos(150,300)
        self.player2.direction = 1
        self.player2.speed_l_ch = 0
        self.player2.speed_r_ch = 0
        self.array_enemies = []
        self.array_bullets = []
        self.array_arrays = [self.array_enemies,self.array_bullets]
        self.timer.start(10)

    def boundingRect(self):
        return QRectF(0,0,self.width(),self.height())

    def boundingField(self):
        return QRectF(-2000, 0, (self.width() + 4000), (self.height()))
        # return QRectF(0,0,self.width(),self.height())


    def create_rectobj(self,timer,cd,hp,damage,step,soap_koef,speed_shoot,size_x,size_y,color,window_x,wimdow_y):
        if timer.isActive() is False:
            rectobj = self.addRect(QRectF(0,0,size_x,size_y),QPen(Qt.PenStyle.NoPen),QBrush(color))
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

    def set_default_rectobj(self,rectobj,hp,damage,step,soap_koef,speed_shoot,size_x,size_y,color):
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
        rectobj.setBrush(color)


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
            if obj.speed_l < obj.step and obj.move_direction_L == 1:
                obj.speed_l += 0.5
            elif obj.move_direction_L == 0 and obj.speed_l > 0:
                obj.speed_l -= 0.5
            elif obj.speed_l < 0:
                obj.speed_l = 0

            if obj.speed_r < obj.step and obj.move_direction_R == 1:
                obj.speed_r += 0.5
            elif obj.move_direction_R == 0 and obj.speed_r > 0:
                obj.speed_r -= 0.5
            elif obj.speed_r < 0:
                obj.speed_r = 0

            if obj.speed_u < obj.step and obj.move_direction_U == 1:
                obj.speed_u += 0.5
            elif obj.move_direction_U == 0 and obj.speed_u > 0:
                obj.speed_u -= 0.5
            elif obj.speed_u < 0:
                obj.speed_u = 0

            if obj.speed_d < obj.step and obj.move_direction_D == 1:
                obj.speed_d += 0.5
            elif obj.move_direction_D == 0 and obj.speed_d > 0:
                obj.speed_d -= 0.5
            elif obj.speed_d < 0:
                obj.speed_d = 0

            timer.timeout.connect(timer.stop)
            timer.start(int(obj.soap_koef))

        if obj.x() - obj.speed_l < 0:
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

        if obj.y() - obj.speed_u < 0:
            obj.setY(0)
            obj.speed_u = 0
        else:
            obj.moveBy(0, -obj.speed_u)

        if obj.y() + obj.speed_d + obj.size_y > obj.window_y:
            obj.setY(obj.window_y - obj.size_y)
            obj.speed_d = 0
        else:
            obj.moveBy(0, obj.speed_d)


    def player_chdirection(self,obj,chdirection_timer,msec,direction,future_x,arrays:list):
        if chdirection_timer.isActive() is False:
            ch_speed = round(sqrt(int(abs(future_x-obj.x()))),2)
            if ch_speed < 0.3:
                ch_speed = 0.3
            if direction == 0:
                obj.moveBy(ch_speed,0)
                obj.speed_r_ch = 0
                for array in arrays:
                    for arr_obj in array:
                        arr_obj.moveBy(ch_speed,0)
            else:
                obj.moveBy(-ch_speed, 0)
                obj.speed_l_ch = 0
                for array in arrays:
                    for arr_obj in array:
                        arr_obj.moveBy(-ch_speed, 0)

            chdirection_timer.timeout.connect(chdirection_timer.stop)
            chdirection_timer.start(msec)


    def check_collision(self):
        # Проверяем столкновение пуль с врагами
        if self.player2.hp <= 0:
            self.timer.stop()
            for array in self.array_arrays:
                for arr_obj in array:
                    self.removeItem(arr_obj)
            self.set_game_default()
        for enemy in self.array_enemies:
            damage_order = 0
            if QRectF(self.player2.x(),self.player2.y(),self.player2.size_x,self.player2.size_y).intersects(QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y)):
                if self.player2.x() + self.player2.size_x // 2 < enemy.x():
                    self.player2.speed_l = self.player2.step * 1
                    self.player2.speed_r = 0
                    damage_order = 1
                elif self.player2.x() + self.player2.size_x // 2 > enemy.x() + enemy.size_x:
                    self.player2.speed_r = self.player2.step * 1
                    self.player2.speed_l = 0
                    damage_order = 1
                elif self.player2.y() + self.player2.size_y // 2 < enemy.y():  # Отталкивание игрока от врага
                    self.player2.speed_u = self.player2.step * 1
                    self.player2.speed_d = 0
                    damage_order = 1
                elif self.player2.y() + self.player2.size_y // 2 > enemy.y() + enemy.size_y:
                    self.player2.speed_d = self.player2.step * 1
                    self.player2.speed_u = 0
                    damage_order = 1
            if damage_order == 1:
                self.player2.hp -= enemy.damage
                damage_order = 0

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
        self.msec += 1
        self.draw_time_timer_text()
        if self.player2.shoot == 1:
                x_size = 10
                y_size = 4
                if self.bullet_timer.isActive() is False:
                    bullet = self.create_rectobj(self.bullet_timer,int(self.player2.speed_shoot),1,1,9,0,0,x_size,y_size,QColor(0,255,0),self.width(),self.height())
                    bullet.setPos(self.player2.x() + (self.player2.size_x*self.player2.direction) +
                                          (x_size*(self.player2.direction-1)),(self.player2.y() + self.player2.size_y // 2) - y_size // 2)
                    bullet.setZValue(1)
                    if self.player2.direction == 1:
                        bullet.move_direction_R = 1
                        bullet.move_direction_L = 0
                    else:
                        bullet.move_direction_L = 1
                        bullet.move_direction_R = 0
                    self.array_bullets.append(bullet)

        if self.enemy_timer.isActive() is False:
            enemy = self.create_rectobj(self.enemy_timer,1000,self.enemies[0][1],self.enemies[0][2],self.enemies[0][3],self.enemies[0][4],self.enemies[0][5],self.enemies[0][6],self.enemies[0][7],self.enemies[0][8],self.width(),self.height())
            enemy.setZValue(2)
            #------------------------------------------- enemy.setBrush(QBrush(QPixmap('low_fanist.jpg'))) <- обрезало
            #--------------------------------------------enemy.setBrush(QBrush(QPixmap('low_star.jpg'))) <- расширило до размеров врага
            #-------------------------------------------- еще можно enemy.setVisible за границами чтобы появлялись позже
            # enemy.setBrush(QBrush(QPixmap('low_nokia.jpg')))
            randint_y = random.randint(0,int(self.height()-enemy.size_y))
            randint_x1 = random.randint(int(self.boundingField().x()),int(self.boundingField().x()*0.2))
            randint_x2 = random.randint(int(self.width()*0.6),int(self.boundingField().width())) # появление врагов дожно быть не ближе чем 2 экрана (direction)
            randint_x_choice = random.randint(0,2) # не позволять экрану засорятся слишком многим количеством противников
            if randint_x_choice == 0:
                enemy.setPos(randint_x1,randint_y)
            else: enemy.setPos(randint_x2,randint_y)
            enemy.move_direction_L = 1
            self.array_enemies.append(enemy)
        self.player_move(self.player2,self.player2_timer,[self.array_bullets,self.array_enemies])
        left_x,right_x = 150,self.width()-150
        if int(self.player2.x()) != right_x and self.player2.direction == 0:
            self.player_chdirection(self.player2,self.player2_chtimer,10,self.player2.direction,right_x,self.array_arrays)
        elif int(self.player2.x()) != left_x and self.player2.direction == 1:
            self.player_chdirection(self.player2,self.player2_chtimer,10,self.player2.direction,left_x,self.array_arrays)
        else:
            self.player2.speed_l_ch = 0
            self.player2.speed_r_ch = 0
        # if len(self.hps) > self.player2.hp and len(self.hps) > 0:
        #     hp = self.hps[-1]
        #     self.removeItem(hp)
        #     self.hps.remove(hp)
        # #------------------------------------------------------------
        # elif len(self.hps) < self.player2.hp and len(self.hps) == 0:
        #     self.draw_player_hp( 1, 50, 8, self.height()+15, 10, 50, QColor(255, 100, 100))
        # elif len(self.hps) < self.player2.hp and len(self.hps) > 0:
        #     last_hp = self.hps[-1]
        #     new_hp = self.draw_player_hp( 1, int(last_hp.x()) + last_hp.size_x + 8, 8, int(last_hp.y()), last_hp.size_x, last_hp.size_y, QColor(255, 100, 100))
        self.draw_player_hp(self.player2.hp,50,8,self.height()+15,10,50,QColor(255,100,100))
        for bullet in self.array_bullets:
            self.new_move(bullet)
        for enemy in self.array_enemies:
            self.new_move(enemy)
            if QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y).intersects(self.boundingRect()) is False and enemy.isVisible() is True:
                enemy.setVisible(False)
            elif QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y).intersects(self.boundingRect()) is True and enemy.isVisible() is False:
                enemy.setVisible(True)
        self.check_collision()
        self.update()



    def keyPressEvent(self, event):

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


    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            global fullscreen
            if fullscreen == 1:
                fullscreen = 0
            else:
                fullscreen = 1
        if event.key() == Qt.Key.Key_Escape:
            fullscreen = 0

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


    def draw_player_hp(self,count_hp,x,between,y,w,h,color):
        if len(self.hps) > count_hp and len(self.hps) > 0:
            last_hp = self.hps[-1]
            self.hps.remove(last_hp)
            self.removeItem(last_hp)
        elif len(self.hps) < count_hp and len(self.hps) == 0:
            hp = self.addRect(0, 0, w, h, QPen(Qt.PenStyle.NoPen), QBrush(color))
            hp.setPos(x,y)
            hp.size_x = w
            hp.size_y = h
            self.hps.append(hp)
        elif len(self.hps) < count_hp and len(self.hps) > 0:
            last_hp = self.hps[-1]
            hp = self.addRect(0,0,w,h,QPen(Qt.PenStyle.NoPen),QBrush(color))
            hp.setPos(last_hp.x()+between+w,y)
            self.hps.append(hp)

    def draw_time_timer_text(self):
        text = ''
        if self.min < 10:
            text += f'0{self.min}:'
        else:
            text += f'{self.min}:'
        if self.sec < 10:
            text += f'0{self.sec}:'
        elif self.sec > 59:
            self.min +=1
            self.sec = 0
        else:
            text += f'{self.sec}:'
        if self.msec < 10:
            text += f'0{self.msec}'
        elif self.msec > 99:
            self.sec += 1
            self.msec = 0
        else:
            text += f'{self.msec}'
        self.timer_text.setPlainText(text)

    def interface(self):
        background = self.addRect(self.boundingRect(), QPen(Qt.PenStyle.NoPen), QBrush(QColor(100,100,100)))
        info_bar = self.addRect(QRectF(0, self.height(), self.width(), ((self.height() * (10 / 8)) - self.height())),
                     QPen(Qt.PenStyle.NoPen), QBrush(QColor(50, 50, 50)))
        left_cover = self.addRect(self.boundingField().x(),0,abs(self.boundingField().x()-self.boundingRect().x())-1,self.height() * (10 / 8),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
        left_cover.setZValue(3)
        right_cover = self.addRect(self.width(),0,self.boundingField().width(),self.height() * (10 / 8),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
        right_cover.setZValue(3)
        # HP_text = self.addText('HP',QFont('Arial',25))
        # HP_text.setDefaultTextColor(QColor('red'))
        # HP_text.setPos(20,self.height()+10)
        self.hps = []
        # pl_level_hp = self.draw_player_hp(self.player2.hp,50,8,self.height()+15,10,50,QColor(255,100,100))
        self.timer_text = self.addText('00:00:00')
        self.timer_text.setDefaultTextColor(QColor('white'))
        self.timer_text.setFont(QFont('Courier New, monospace;',25))
        self.timer_text.setPos(self.width()-200,self.height())




class Game(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setGeometry(0,0,1120,600)
        self.setMinimumSize(1120,600)
        self.showMaximized()
        self.setScene(scene)
        # self.setSceneRect(0,0,1120,600)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.scale(0.6,0.6)
        self.setStyleSheet('border:none')

    def resizeEvent(self, event):
        self.fitInView(QRectF(0,0,849,475), Qt.AspectRatioMode.KeepAspectRatio)

def toggle_fullscreen(obj):
    if obj.isFullScreen() is False and fullscreen == 1:
        obj.showFullScreen()
    elif obj.isFullScreen() is True and fullscreen == 0:
        obj.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = StartGame(None,True)
    game_window = Game(game)
    game_window.show()
    fullscreen = 0
    timer = QTimer()
    timer.timeout.connect(lambda: toggle_fullscreen(game_window))
    timer.start(10)
    sys.exit(app.exec())

    # оптимизировать использование массивов(проц доходит до 25%):
    # ордер на создание и удаление(очередь)
