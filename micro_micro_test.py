import sys
import threading
from math import ceil, sqrt
import random

from PyQt6.QtCore import QPoint, QSize, QRectF, Qt, QTimer, QPointF
from PyQt6.QtGui import QColor, QPainter, QBrush, QFont, QPixmap, QPen
from PyQt6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QWidget, \
    QLabel, QPushButton, QStackedWidget, QVBoxLayout


class Choice_Card(QWidget):
    def __init__(self, x_window, y_window, way_attr):
        super().__init__()
        num_cards = 3
        self.cards = []
        self.Create_Cards(num_cards, x_window, y_window)
        self.setStyleSheet('background-color: transparent;')
        self.setMinimumSize(int(x_window),int(y_window))


    def Create_Cards(self, count, x_window, y_window):
        for i in range(count):
            card_text = QLabel(self)
            card_text.setWordWrap(True)
            card = QPushButton(self)
            card_width = int((x_window/count)*0.85)
            card_height = int(y_window*0.8)
            card.setGeometry(i*((int(x_window)-card_width)//2),(int(y_window)-card_height)//2,card_width,card_height)
            card.setStyleSheet('QPushButton:hover{background-color:rgba(100,50,50,100)}'
                               'background-color:rgba(0,0,0,0)')
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            card_text.setStyleSheet(
                         "font-size: 25px;"
                         "padding: 15px;"
            "background-color:rgba(0,20,0,255)")
            card_text.setAlignment(Qt.AlignmentFlag.AlignTop)
            card_text.setGeometry(i*((int(x_window)-card_width)//2),(int(y_window)-card_height)//2,card_width,card_height)

            self.cards.append((card_text, card))

    def Set_Content(self,way_for_eff,card:any,Name:str,description:str,effects:list):
        card[0].setText(f'{Name}\n\n\n\n{description}')
        for i in range(len(effects)): # effects = [( object(player), effect(HP_O), value(+10) )]
            obj = getattr(way_for_eff, effects[i][0])
            card[1].clicked.connect(lambda: setattr(obj, effects[i][1], eval(f'{getattr(obj,effects[i][1])}{effects[i][2]}')))

    def randomize_cards(self, way_to_attr):
        types_cards = [
            ('Blessing','you lucky, you are blessed from the Universe. Gain you 1 HP', 'player2', 'hp', '+1'),
            ('OnePanchMan','100 pull-ups, 100 push-ups, 100 crunches, 10km run. your damage + 10', 'player2', 'damage', '+10') # лучше использовать лабел - тк можно будет разные стили сделать,
            # а еще переносить по словам
        ]
        for card in self.cards:
            name, description, obj, effect, value = random.choice(list(types_cards))
            self.Set_Content(way_to_attr,card, name, description, [(obj, effect, value)])


class Scene_game(QGraphicsScene):
    def __init__(self):
        super().__init__()

        self.setSceneRect(0,0,854,(480*0.8))
        # self.setSceneRect(0,0,480,(270*0.8))

        self.array_enemies = []
        self.array_bullets = []
        self.array_arrays = [self.array_enemies, self.array_bullets]

        # players = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.players = [
            ('Default',      3,  1,      8,    10,        370,         25,     25,     QColor(0, 0, 255)),
            ('IFeelPain',    1,  0.5,    16,   40,        290,         35,     35,     QColor(200, 150, 0)),
            ('UPower',       5,  2,      7,    15,        420,         65,     65,     QColor(100, 255, 255))
        ]
        # enemies = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.enemies = [
            ('Default',      3,  1,      0.2,    0,         0,           35,    35,     QColor(150, 0, 0)),#45x45
            ('Tiny',         1,  1,      3,    0,         0,           35,     35,     QColor(255, 111, 0)),
            ('Fat',          5,  1,      0.5,  0,         0,           85,     85,     QColor(255, 111, 111)),
        ]
        # bullets = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.bullets = [
            ('Default',      1,  1,      1,    0,         0,           10,     4,     QColor(0, 255, 0)),
            ('Tiny',         1,  1,      3,    0,         0,           35,     35,     QColor(255, 111, 0)),
            ('Fat',          5,  1,      0.5,  0,         0,           85,     85,     QColor(255, 111, 111)),
        ]

        self.player2_timer = QTimer()
        self.player2_chtimer = QTimer()
        # self.player2 = self.create_rectobj(self,self.player2_timer,1,self.players[0][1], self.players[0][2], self.players[0][3],self.players[0][4],self.players[0][5],self.players[0][6],self.players[0][7],self.players[0][8],self.width(),self.height(),QPointF(150,300),self.player_move,[self.player2_timer,self.array_arrays])
        # self.player2 = class_create_rectobj(self,self.player2_timer,1,self.players[0][1], self.players[0][2], self.players[0][3],self.players[0][4],self.players[0][5],self.players[0][6],self.players[0][7],self.players[0][8],self.width(),self.height(),QPointF(150,300),self.player_move,[self.player2_timer,self.array_arrays])
        scene = self
        self.rectobj = self.create_rectobj_podclass_from_class(self,self.player2_timer,1,self.players[0][1], self.players[0][2], self.players[0][3],self.players[0][4],self.players[0][5],self.players[0][6],self.players[0][7],self.players[0][8],self.width(),self.height(),QPointF(150,300),self.player_move,[self.player2_timer,self.array_arrays])
        self.player2 = self.rectobj
        self.player2.setZValue(1)

        self.enemy_timer = QTimer()

        self.bullet_timer = QTimer()

        self.timer = QTimer()
        self.timer.timeout.connect(lambda :self.updateScene(self.player2,self.array_enemies,self.array_bullets))
        self.set_game_default()
        self.enemy_timer = QTimer()
        self.bullet_timer1 = QTimer()

        self.interface()

    def create_rectobj_podclass_from_class(self,scene:QGraphicsScene,timer:QTimer,cd:int,hp:int,damage:float,step:float,soap_koef:int,speed_shoot:int,size_x:int,size_y:int,color:QColor,window_x:float,window_y:float,create_pos:QPointF,move_pattern,parameters:list):
        return self.create_rect_obj_class(scene,timer,cd,hp,damage,step,soap_koef,speed_shoot,size_x,size_y,color,window_x,window_y,create_pos,move_pattern,parameters)

    def set_game_default(self):
        self.msec = 0
        self.sec = 0
        self.min = 0
        self.set_default_rectobj(self.player2,self.players[0][1], self.players[0][2], self.players[0][3],self.players[0][4],self.players[0][5],self.players[0][6],self.players[0][7],self.players[0][8])
        self.player2.setPos(150,300)
        self.player2.direction = 1
        self.array_enemies.clear()
        self.array_bullets.clear()
        self.stop_game(False)

    def stop_game(self,bol:bool):
        if bol is True:
            self.timer.stop()
        else:
            self.timer.start(10)

    def boundingRect(self):
        return QRectF(0,0,self.width(),self.height())

    def boundingField(self):
        return QRectF(-2000, 0, (self.width() + 4000), (self.height()))

    def create_bullet(self,scene,player,bullet_timer:QTimer,array_bullets:list,bullets:list,wch_b_t):
        wch_b_t -= 1
        if player.shoot == 1:
                if bullet_timer.isActive() is False:
                    bullet = scene.create_rectobj_podclass_from_class(scene,bullet_timer,player.speed_shoot,
                                        bullets[wch_b_t][1],bullets[wch_b_t][2],bullets[wch_b_t][3],bullets[wch_b_t][4],
                                        bullets[wch_b_t][5],bullets[wch_b_t][6],bullets[wch_b_t][7],
                                        bullets[wch_b_t][8],scene.width(),scene.height(),
                                        QPointF(player.x() + (player.size_x*player.direction) +
                                            (bullets[wch_b_t][6]*(player.direction-1)),
                                            (player.y() + player.size_y // 2) - bullets[wch_b_t][7] // 2),
                                        scene.new_move,[None,None])
                    bullet.setZValue(1)
                    if player.direction == 1:
                        bullet.move_direction_R = 1
                        bullet.move_direction_L = 0
                    else:
                        bullet.move_direction_L = 1
                        bullet.move_direction_R = 0
                    array_bullets.append(bullet)
                    return bullet
    class create_rect_obj_class(QGraphicsRectItem):
        def __init__(obj,scene:QGraphicsScene,timer:QTimer,cd:int,hp:int,damage:float,step:float,soap_koef:int,speed_shoot:int,size_x:int,size_y:int,color:QColor,window_x:float,window_y:float,create_pos:QPointF,move_pattern,parameters:list):
            super().__init__()
            if timer.isActive() is False:
                # obj: scene.addRect(QRectF(0, 0, size_x, size_y), QPen(Qt.PenStyle.NoPen), QBrush(color))
                obj.setRect(QRectF(0, 0, size_x, size_y))
                obj.setPen(QPen(Qt.PenStyle.NoPen))
                obj.setBrush(QBrush(color))
                scene.addItem(obj)
                # obj.function = obj
                obj.setPos(create_pos)
                obj.move_direction_L = 0
                obj.move_direction_R = 0
                obj.move_direction_U = 0
                obj.move_direction_D = 0
                obj.shoot = 0
                obj.speed_l = 0
                obj.speed_r = 0
                obj.speed_u = 0
                obj.speed_d = 0
                obj.step = step
                obj.soap_koef = soap_koef
                obj.size_x = size_x
                obj.size_y = size_y
                obj.window_x = window_x
                obj.window_y = window_y
                obj.parameters = parameters
                obj.move_pattern = move_pattern
                obj.hp = hp
                obj.damage = damage
                obj.speed_shoot = speed_shoot
                timer.start(cd)
                timer.timeout.connect(timer.stop)

        def move(obj):
            obj.move_pattern(obj,obj.parameters)

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


    def new_move(self,obj,parameters:list):
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


    def player_move(self,obj,parameters:list):
        timer = parameters[0]
        arrays = parameters[1]
        if timer.isActive() is False:
            if obj.speed_l < obj.step and obj.move_direction_L == 1:
                obj.speed_l += 0.1
            elif obj.move_direction_L == 0 and obj.speed_l > 0:
                obj.speed_l -= 0.1
            elif obj.speed_l < 0:
                obj.speed_l = 0

            if obj.speed_r < obj.step and obj.move_direction_R == 1:
                obj.speed_r += 0.1
            elif obj.move_direction_R == 0 and obj.speed_r > 0:
                obj.speed_r -= 0.1
            elif obj.speed_r < 0:
                obj.speed_r = 0

            if obj.speed_u < obj.step and obj.move_direction_U == 1:
                obj.speed_u += 0.1
            elif obj.move_direction_U == 0 and obj.speed_u > 0:
                obj.speed_u -= 0.1
            elif obj.speed_u < 0:
                obj.speed_u = 0

            if obj.speed_d < obj.step and obj.move_direction_D == 1:
                obj.speed_d += 0.1
            elif obj.move_direction_D == 0 and obj.speed_d > 0:
                obj.speed_d -= 0.1
            elif obj.speed_d < 0:
                obj.speed_d = 0

            timer.timeout.connect(timer.stop)
            timer.start(int(obj.soap_koef))

        for array in arrays:
            for arr_obj in array:
                arr_obj.moveBy(obj.speed_l-obj.speed_r, 0)
                # self.new_move(arr_obj)
                arr_obj.move()

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
                for array in arrays:
                    for arr_obj in array:
                        arr_obj.moveBy(ch_speed,0)
            else:
                obj.moveBy(-ch_speed, 0)
                for array in arrays:
                    for arr_obj in array:
                        arr_obj.moveBy(-ch_speed, 0)

            chdirection_timer.timeout.connect(chdirection_timer.stop)
            chdirection_timer.start(msec)


    def check_collision(self,player,array_enemies,array_bullets):
        # Проверяем столкновение пуль с врагами
        # if self.player2.hp <= 0:
        #     self.timer.stop()
        #     for array in self.array_arrays:
        #         for arr_obj in array:
        #             self.removeItem(arr_obj)
        #     self.set_game_default()
        for enemy in array_enemies:
            damage_order = 0
            if QRectF(player.x(),player.y(),player.size_x,player.size_y).intersects(QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y)):
                if player.x() + player.size_x // 2 < enemy.x():
                    player.speed_l = player.step * 0.5
                    player.speed_r = 0
                    damage_order = 1
                elif player.x() + player.size_x // 2 > enemy.x() + enemy.size_x:
                    player.speed_r = player.step * 0.5
                    player.speed_l = 0
                    damage_order = 1
                elif player.y() + player.size_y // 2 < enemy.y():  # Отталкивание игрока от врага
                    player.speed_u = player.step * 0.5
                    player.speed_d = 0
                    damage_order = 1
                elif player.y() + player.size_y // 2 > enemy.y() + enemy.size_y:
                    player.speed_d = player.step * 0.5
                    player.speed_u = 0
                    damage_order = 1
            if damage_order == 1:
                player.hp -= enemy.damage
                damage_order = 0
            if QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y).intersects(self.boundingRect()) is False and enemy.isVisible() is True:
                enemy.setVisible(False)
            elif QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y).intersects(self.boundingRect()) is True and enemy.isVisible() is False:
                enemy.setVisible(True)
            if self.boundingField().contains(QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y)) is False:
                self.array_enemies.remove(enemy)
                self.removeItem(enemy)
                continue
            for bullet in array_bullets:
                if self.boundingRect().intersects(QRectF(bullet.x(),bullet.y(),bullet.size_x,bullet.size_y)) is False:
                    array_bullets.remove(bullet)
                    self.removeItem(bullet)
                    continue
                if enemy.x() <= self.width() - (enemy.size_x // 2):
                    if QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y).intersects(QRectF(bullet.x(),bullet.y(),bullet.size_x,bullet.size_y)):
                        array_bullets.remove(bullet)
                        self.removeItem(bullet)
                        enemy.hp -= (bullet.damage * player.damage)
                        if enemy.hp <= 0:
                            self.array_enemies.remove(enemy)
                            self.removeItem(enemy)


    def updateScene(self,player,array_enemies,array_bullets):
        self.msec += 1
        self.draw_time_timer_text()
        # if player.shoot == 1:
        #         x_size = 10
        #         y_size = 4
        #         if self.bullet_timer.isActive() is False:
        #             bullet = self.create_rectobj(self,self.bullet_timer,int(self.player2.speed_shoot),1,1,9,0,0,x_size,y_size,QColor(0,255,0),self.width(),self.height())
        #             bullet.setPos(player.x() + (player.size_x*player.direction) +
        #                                   (x_size*(player.direction-1)),(player.y() + player.size_y // 2) - y_size // 2)
        #             bullet.setZValue(1)
        #             if player.direction == 1:
        #                 bullet.move_direction_R = 1
        #                 bullet.move_direction_L = 0
        #             else:
        #                 bullet.move_direction_L = 1
        #                 bullet.move_direction_R = 0
        #             array_bullets.append(bullet)
        bullet = self.create_bullet(self,player,self.bullet_timer,array_bullets,self.bullets,1)
        # for bullett in array_bullets:
        #     bullett.function.move()
        if self.enemy_timer.isActive() is False and len(array_enemies) < 0:
            enemy = self.create_rectobj(self,self.enemy_timer,1000,self.enemies[0][1],self.enemies[0][2],self.enemies[0][3],self.enemies[0][4],self.enemies[0][5],self.enemies[0][6],self.enemies[0][7],self.enemies[0][8],self.width(),self.height())
            enemy.setZValue(2)
            #------------------------------------------- enemy.setBrush(QBrush(QPixmap('low_fanist.jpg'))) <- обрезало
            #--------------------------------------------enemy.setBrush(QBrush(QPixmap('low_star.jpg'))) <- расширило до размеров врага
            # enemy.setBrush(QBrush(QPixmap('low_nokia.jpg')))
            randint_y = random.randint(0,int(self.height()-enemy.size_y))
            randint_x1 = random.randint(int(self.boundingField().x()),int(self.boundingField().x()*0.2))
            randint_x2 = random.randint(int(self.width()*0.6),int(self.boundingField().width())) # появление врагов дожно быть не ближе чем 2 экрана (direction)
            randint_x_choice = random.randint(0,2) # не позволять экрану засорятся слишком многим количеством противников
            if randint_x_choice == 0:
                enemy.setPos(randint_x1,randint_y)
            else: enemy.setPos(randint_x2,randint_y)
            enemy.move_direction_L = 1
            array_enemies.append(enemy)
        # self.player_move(self.player2,self.player2_timer,[self.array_bullets,self.array_enemies])
        player.move()
        left_x,right_x = 150,self.width()-150
        if int(player.x()) != right_x and player.direction == 0:
            self.player_chdirection(player,self.player2_chtimer,10,player.direction,right_x,[array_enemies,array_bullets])
        elif int(player.x()) != left_x and player.direction == 1:
            self.player_chdirection(player,self.player2_chtimer,10,player.direction,left_x,[array_enemies,array_bullets])
        self.draw_player_hp(player.hp,50,8,self.height()+15,10,50,QColor(255,100,100))
        self.check_collision(player,array_enemies,array_bullets)
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

        if event.text() == 'p':
            self.stop_game(True)
        if event.text() == '[':
            self.stop_game(False)

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


    # def create_card_page(self):
        # self.stack_widget_game = QStackedWidget()
        # layout = QVBoxLayout()
        # background = self.addRect(self.boundingRect(), QPen(Qt.PenStyle.NoPen), QBrush(QColor(0,0,0,50)))
        # layout.addItem(background)
        # cards = Choice_Card(self.width(), self.height() * (10 / 8), self)
        # layout.addItem(cards)
        # self.stack_widget_game.addWidget(layout)
        # cards.randomize_cards(self)
        # self.stack_widget_game.addWidget(self)

    # корочь сделай так чтобы при вызове появлялось кв и кнопки а потом когда выберешь все пропадало


    def interface(self):
        background = self.addRect(self.boundingRect(), QPen(Qt.PenStyle.NoPen), QBrush(QColor(100,100,100)))
        info_bar = self.addRect(QRectF(0, self.height(), self.width(), ((self.height() * (10 / 8)) - self.height())),
                     QPen(Qt.PenStyle.NoPen), QBrush(QColor(50, 50, 50)))
        # left_cover = self.addRect(self.boundingField().x(),0,abs(self.boundingField().x()-self.boundingRect().x()),self.height() * (10 / 8),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
        # left_cover.setZValue(3)
        # right_cover = self.addRect(self.width(),0,self.boundingField().width(),self.height() * (10 / 8),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
        # right_cover.setZValue(3)
        self.hps = []
        self.timer_text = self.addText('00:00:00')
        self.timer_text.setDefaultTextColor(QColor('white'))
        self.timer_text.setFont(QFont('Courier New, monospace;',25))
        self.timer_text.setPos(self.width()-200,self.height())
        # self.create_card_page()


# class class_create_rectobj(Scene_game):
#         def __init__(obj,scene:QGraphicsScene,timer:QTimer,cd:int,hp:int,damage:float,step:float,soap_koef:int,speed_shoot:int,size_x:int,size_y:int,color:QColor,window_x:float,window_y:float,create_pos:QPointF,move_pattern,parameters:list):
#             super().__init__()
#             if timer.isActive() is False:
#                 obj.rectobj = scene.addRect(QRectF(0,0,size_x,size_y),QPen(Qt.PenStyle.NoPen),QBrush(color))
#                 obj.rectobj.setPos(create_pos)
#                 obj.rectobj.move_direction_L = 0
#                 obj.rectobj.move_direction_R = 0
#                 obj.rectobj.move_direction_U = 0
#                 obj.rectobj.move_direction_D = 0
#                 obj.rectobj.shoot = 0
#                 obj.rectobj.speed_l = 0
#                 obj.rectobj.speed_r = 0
#                 obj.rectobj.speed_u = 0
#                 obj.rectobj.speed_d = 0
#                 obj.rectobj.step = step
#                 obj.rectobj.soap_koef = soap_koef
#                 obj.rectobj.size_x = size_x
#                 obj.rectobj.size_y = size_y
#                 obj.rectobj.window_x = window_x
#                 obj.rectobj.window_y = window_y
#                 param = 'obj.rectobj,'
#                 # for parameter in parameters:
#                 #     if parameter != parameters[-1]:
#                 #         param += f'{parameter},'
#                 #     else:
#                 #         param += f'{parameter}'
#                 obj.timer, obj.arrays = parameters[0],parameters[1]
#                 # obj.rectobj.move_pattern(obj.rectobj,timer,arrays)
#                 # print('hell')
#                 obj.move_pattern = move_pattern
#                 obj.rectobj.hp = hp
#                 obj.rectobj.damage = damage
#                 obj.rectobj.speed_shoot = speed_shoot
#                 timer.start(cd)
#                 timer.timeout.connect(timer.stop)
#
#         def move(obj):
#             obj.move_pattern(obj.rectobj,obj.timer,obj.arrays)




class View_dame(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setGeometry(0,0,1120,600)
        self.setMinimumSize(1120,600)
        self.setBackgroundBrush(QColor(0, 0, 0))
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
    game = Scene_game()
    game_window = View_dame(game)
    game_window.show()
    fullscreen = 0
    timer = QTimer()
    timer.timeout.connect(lambda: toggle_fullscreen(game_window))
    timer.start(10)
    sys.exit(app.exec())

    # что если враги за экраном будут постоянно уменьшать свой шаг, так, теоретически можно не прибегая к обольшй карте сделать хранение врагов почти бесконечним
    #  например -500 дальше враг имеет меньшую строрость и так далее а когда приблежаентся ко мне то увеличивает ее
    # добавить в подкласс creation def - чтобы можно было при определенном def создавать пули, врагов по разному