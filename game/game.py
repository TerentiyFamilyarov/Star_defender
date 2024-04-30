import sys
import threading
from math import ceil, sqrt
import random

from PyQt6.QtCore import QPoint, QSize, QRectF, Qt, QTimer, QPointF, QRect
from PyQt6.QtGui import QColor, QPainter, QBrush, QFont, QPixmap, QPen, QTextOption, QPalette
from PyQt6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QWidget, \
    QLabel, QPushButton, QStackedWidget, QVBoxLayout, QStyle, QMainWindow, QGraphicsEffect, QGraphicsProxyWidget

import Bullets
import Enemies

def create_txt_widget(scene,name: str, fontstyle: str,textcolor:QColor,fontsize:int, pos:QPointF):
    txt = QGraphicsTextItem()
    txt.setDefaultTextColor(textcolor)
    txt.setPlainText(name)
    txt.setFont(QFont(fontstyle,fontsize))
    txt.setPos(pos)
    scene.addItem(txt)
    return txt


def create_button_widget(scene,txt:str,geometry:QRect,style:str):
    button = QPushButton()
    button.setText(txt)
    button.setGeometry(geometry)
    button.setStyleSheet(style)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    scene.addWidget(button)
    return button

def create_button(parent,txt:str,geometry:QRect,style:str):
    button = QPushButton(parent)
    button.setText(txt)
    button.setGeometry(geometry)
    button.setStyleSheet(style)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    return button

class main_page(QGraphicsScene):
    def __init__(self,view):
        super().__init__()
        self.setSceneRect(0,0,854,480)
        self.setBackgroundBrush(QColor(0,0,0,0))
        self.choose_player_menu = None
        self.Main_title = create_txt_widget(self,'STAR DEFENDER','Courier, monospace',QColor(200,200,200,50),60,QPointF(0,50))
        self.start_button = create_button_widget(self, 'Start', QRect(0, 300, 100, 20),
                       'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                       '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                       '                    font-size: 20px;}'
                       'QPushButton:hover {color: rgb(219,203,180)}')
        self.start_button.clicked.connect(lambda: view.setScene(self.choose_player_menu))
        self.exit_button = create_button_widget(self, 'Exit', QRect(0, 350, 100, 20),
                     'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                     '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                     '                   font-size:20px}'
                     'QPushButton:hover {color: rgb(219,203,180)}')
        self.exit_button.clicked.connect(view.close)

class choose_player_page(QGraphicsScene):
    def __init__(self,view):
        super().__init__()
        self.setSceneRect(0,0,854,480)
        self.setBackgroundBrush(QColor(0,0,0,0))
        self.view = view
        self.game = None
        self.main_menu = None
        self.choose_player_txt = create_txt_widget(self,'CHOOSE PLAYER','Courier, monospace',QColor(200,200,200,50),30,QPointF(0,50))
        self.about_player_txt = create_txt_widget(self,'About player','Courier New, monospace',QColor(200,200,200),15,QPointF(300,300))
        self.back_button = create_button_widget(self, 'back', QRect(600, 200, 100, 20),
                       'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                       '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                       '                    font-size: 20px;}'
                       'QPushButton:hover {color: rgb(219,203,180)}')
        self.chosen_player = 0
        self.back_button.clicked.connect(self.onemode)
        self.next_button = create_button_widget(self, 'next', QRect(700, 200, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        self.next_button.clicked.connect(self.twomode)
        self.play_button = create_button_widget(self, 'Play', QRect(600, 350, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        self.play_button.clicked.connect(lambda: self.restart_game())
        self.main_menu_button = create_button_widget(self, 'Got to menu', QRect(0, 350, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        self.main_menu_button.clicked.connect(lambda: view.setScene(self.main_menu))

    def restart_game(self):
        self.game.restart_game()
        self.view.setScene(self.game)

    def draw_actual_info(self):
        players = self.game.players
        self.game.set_default_rectobj(self.game.player2,players[self.chosen_player][1], players[self.chosen_player][2],
                                   players[self.chosen_player][3], players[self.chosen_player][4],
                                   players[self.chosen_player][5], players[self.chosen_player][6],
                                   players[self.chosen_player][7], players[self.chosen_player][8])
        self.about_player_txt.setPlainText(f"Name: {self.game.players[self.chosen_player][0]} \n"
                                      f"Health: {self.game.player2.hp} \n"
                                      f"Speed: {self.game.player2.step} \n"
                                      f"Soap move: {self.game.player2.soap_koef} \n"
                                      f"Damage: {self.game.player2.damage} \n"
                                      f"Speed shoot: {self.game.player2.speed_shoot} \n"
                                      f"Size: {self.game.player2.size_x}")
    def onemode(self):
        self.chosen_player -= 1
        maxx = len(self.game.players)-1
        if self.chosen_player < 0:
            self.chosen_player = len(self.game.players)-1
        elif self.chosen_player > maxx:
            self.chosen_player = 0
        self.draw_actual_info()

    def twomode(self):
        self.chosen_player += 1
        maxx = len(self.game.players) - 1
        if self.chosen_player < 0:
            self.chosen_player = len(self.game.players) - 1
        elif self.chosen_player > maxx:
            self.chosen_player = 0
        self.draw_actual_info()

class pause_page(QGraphicsScene):
    def __init__(self,view):
        super().__init__()
        self.setSceneRect(0, 0, 854, 480)
        self.setBackgroundBrush(QColor(0, 0, 0, 0))
        self.game = None
        self.main_menu = None
        self.view = view
        self.pause_txt = create_txt_widget(self, 'PAUSE', 'Courier, monospace', QColor(200, 200, 200, 50),
                                               30, QPointF(0, 50))
        self.resume_button = create_button_widget(self, 'Resume', QRect(0, 300, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        self.resume_button.clicked.connect(lambda :view.setScene(self.game))
        self.restart_button = create_button_widget(self, 'Restart', QRect(0, 350, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        self.restart_button.clicked.connect(self.restart_game)
        self.main_menu_button = create_button_widget(self, 'Main menu', QRect(0, 400, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        self.main_menu_button.clicked.connect(lambda :view.setScene(self.main_menu))

    def restart_game(self):
        self.game.set_game_default()
        self.view.setScene(self.game)


class Scene_game(QGraphicsScene):
    def __init__(self,view):
        super().__init__()

        self.setSceneRect(0,0,854,(480*0.8))
        # self.setSceneRect(0,0,480,(270*0.8))
        self.pause_menu = None
        self.main_menu = None
        self.choose_menu = None
        self.view = view
        self.scene = self

        self.array_enemies = Enemies.array_enemies
        self.array_bullets = Bullets.array_bullets
        self.array_arrays = [self.array_enemies, self.array_bullets]

        # players = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.players = [
            ('Default',      3,  1,      8,    10,        370,         25,     25,     QColor(0, 0, 255)),
            ('IFeelPain',    1,  0.5,    16,   40,        290,         20,     20,     QColor(200, 150, 0)),
            ('UPower',       5,  2,      7,    15,        420,         30,     30,     QColor(100, 255, 255))
        ]
        # enemies = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.enemies = Enemies.enemies
        # bullets = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.bullets = Bullets.bullets

        self.player2_timer = QTimer()
        self.player2_chtimer = QTimer()
        self.player2 = self.create_rectobj_podclass_from_class(self,self.player2_timer,1,self.players[0][1], self.players[0][2], self.players[0][3],self.players[0][4],self.players[0][5],self.players[0][6],self.players[0][7],self.players[0][8],self.width(),self.height(),self.player_move,[self.player2_timer,self.array_arrays])
        self.player2.creation_pattern = lambda obj:obj.setPos(150,300)
        self.player2.setZValue(1)



        self.events_timer = QTimer()
        self.events_timer.timeout.connect(self.game_events)
        self.events_timer.start(150)

        self.game_timer = QTimer()
        self.game_timer.timeout.connect(lambda :self.updateScene(self.player2,self.array_enemies,self.array_bullets))
        self.set_game_default()

        self.interface()


    def game_events(self):
        # if self.view.scene() != self:
        #     self.stop_game(True)
        # else:self.stop_game(False)
        pass


    def create_rectobj_podclass_from_class(self,scene:QGraphicsScene,timer:QTimer,cd:int,hp:int,damage:float,step:float,soap_koef:int,speed_shoot:int,size_x:int,size_y:int,color:QColor,window_x:float,window_y:float,move_pattern,parameters):
        return self.create_rect_obj_class(scene,timer,cd,hp,damage,step,soap_koef,speed_shoot,size_x,size_y,color,window_x,window_y,move_pattern,parameters)

    def set_game_default(self):
        self.cur_worked = 0
        self.msec = 0
        self.sec = 0
        self.min = 0
        self.bullet_type = 0
        self.enemy_types = 0
        # self.set_default_rectobj(self.player2,self.players[0][1], self.players[0][2], self.players[0][3],self.players[0][4],self.players[0][5],self.players[0][6],self.players[0][7],self.players[0][8])
        self.player2.setPos(150,300)
        self.player2.move_direction_L = 0
        self.player2.move_direction_R = 0
        self.player2.move_direction_U = 0
        self.player2.move_direction_D = 0
        self.player2.shoot = 0
        self.player2.speed_l = 0
        self.player2.speed_r = 0
        self.player2.speed_u = 0
        self.player2.speed_d = 0
        self.player2.direction = 1
        for array in self.array_arrays:
            for arr_obj in array:
                self.removeItem(arr_obj)
        self.array_enemies.clear()
        self.array_bullets.clear()
        self.stop_game(False)

    def stop_game(self,bol:bool):
        if bol is True:
            self.game_timer.stop()
        else:
            self.game_timer.start(10)

    def boundingRect(self):
        return QRectF(0,0,self.width(),self.height())

    def boundingField(self):
        return QRectF(-2000, -100, (self.width() + 4000), (self.height())+200)


    class create_rect_obj_class(QGraphicsRectItem):
        def __init__(obj,scene:QGraphicsScene,timer:QTimer,cd:int,hp:int,damage:float,step:float,soap_koef:int,speed_shoot:int,size_x:int,size_y:int,color:QColor,window_x:float,window_y:float,move_pattern,parameters):
            super().__init__()
            if timer.isActive() is False:
                obj.setRect(QRectF(0, 0, size_x, size_y))
                obj.setPen(QPen(Qt.PenStyle.NoPen))
                obj.setBrush(QBrush(color))
                scene.addItem(obj)
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
                obj.creation_pattern = None
                obj.move_pattern = move_pattern
                obj.hp = hp
                obj.hit_delay = 0
                obj.damage = damage
                obj.speed_shoot = speed_shoot
                timer.start(cd)
                timer.timeout.connect(timer.stop)


        def pos_create(obj):
            obj.creation_pattern(obj)

        def move(obj):
            if obj.parameters != None:
                obj.move_pattern(obj,obj.parameters)
            else: obj.move_pattern(obj)

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
        rectobj.setRect(0,0,rectobj.size_x,rectobj.size_y)
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
            if direction == 0:  # можно обьединить player_move и это ^
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
        if self.player2.hp <= 0:
            self.show_game_over_page(True)
        for enemy in array_enemies:
            for enemy2 in array_enemies:
                if enemy != enemy2:
                    if QRectF(enemy2.x(), enemy2.y(), enemy2.size_x, enemy2.size_y).intersects(
                            QRectF(enemy.x(), enemy.y(), enemy.size_x, enemy.size_y)):
                        if enemy2.x() + enemy2.size_x // 2 < enemy.x():
                            enemy2.move_direction_R = 0
                            enemy2.move_direction_L = 1
                        elif enemy2.x() + enemy2.size_x // 2 > enemy.x() + enemy.size_x:
                            enemy2.move_direction_R = 1
                            enemy2.move_direction_L = 0
                        elif enemy2.y() + enemy2.size_y // 2 < enemy.y():  # Отталкивание игрока от врага
                            enemy2.move_direction_D = 0
                            enemy2.move_direction_U = 1
                        elif enemy2.y() + enemy2.size_y // 2 > enemy.y() + enemy.size_y:
                            enemy2.move_direction_U = 0
                            enemy2.move_direction_D = 1
            if QRectF(player.x(),player.y(),player.size_x,player.size_y).intersects(QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y)):
                if player.hit_delay == 0:
                    player.hp -= enemy.damage
                player.hit_delay = 500
                if player.x() + player.size_x // 2 < enemy.x():
                    player.speed_l = (player.step + enemy.step) * 0.5
                    player.speed_r = 0
                elif player.x() + player.size_x // 2 > enemy.x() + enemy.size_x:
                    player.speed_r = (player.step + enemy.step) * 0.5
                    player.speed_l = 0
                elif player.y() + player.size_y // 2 < enemy.y():  # Отталкивание игрока от врага
                    player.speed_u = (player.step + enemy.step) * 0.5
                    player.speed_d = 0
                elif player.y() + player.size_y // 2 > enemy.y() + enemy.size_y:
                    player.speed_d = (player.step + enemy.step) * 0.5
                    player.speed_u = 0
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
        if player.hit_delay > 0:
            player.hit_delay -= 10
        if self.sec % 10 == 0 and self.cur_worked != self.sec:
            self.show_card_page(True)
            self.cur_worked = self.sec
        self.draw_time_timer_text()
        bullet = Bullets.create_bullet(self,player,array_bullets,self.bullets,self.bullet_type)
        enemy = Enemies.create_enemy(self,1000,50,array_enemies,
                                     self.enemies,random.randint(0,self.enemy_types))
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

        if event.key() == Qt.Key.Key_Escape:
            if self.game_timer.isActive() is True:
                self.show_pause_page(True)

        # if event.key() == Qt.Key.Key_K:
        #     self.show_card_page(True)


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

        # if event.text() == 'p':
        #     self.stop_game(True)
        # if event.text() == '[':
        #     self.stop_game(False)

    def draw_player_hp(self,count_hp,x,between,y,w,h,color):
        if len(self.hps) > count_hp and len(self.hps) > 0:
            last_hp = self.hps[-1]
            self.hps.remove(last_hp)
            self.removeItem(last_hp)
        elif len(self.hps) < count_hp and len(self.hps) == 0:
            hp = self.addRect(0, 0, w, h, QPen(Qt.PenStyle.NoPen), QBrush(color))
            hp.setZValue(2)
            hp.setPos(x,y)
            hp.size_x = w
            hp.size_y = h
            self.hps.append(hp)
        elif len(self.hps) < count_hp and len(self.hps) > 0:
            last_hp = self.hps[-1]
            hp = self.addRect(0,0,w,h,QPen(Qt.PenStyle.NoPen),QBrush(color))
            hp.setZValue(2)
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

    def create_pause_game(self):
        pause_page = QWidget()
        pause_page.setGeometry(0,0,854,480)
        pause_page.setStyleSheet('background-color: transparent')

        pause_txt = QLabel(pause_page)
        pause_txt.setText('PAUSE')
        pause_txt.setFont(QFont('Courier, monospace',30))
        pause_txt.setGeometry(0,50,100,30)

        resume_button = create_button(pause_page, 'Resume', QRect(0, 300, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')

        resume_button.clicked.connect(lambda: self.show_pause_page(False))
        restart_button = create_button(pause_page, 'Restart', QRect(0, 350, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        restart_button.clicked.connect(self.restart_game)
        main_menu_button = create_button(pause_page, 'Main menu', QRect(0, 400, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        main_menu_button.clicked.connect(lambda: self.view.setScene(self.main_menu))
        widget = self.addWidget(pause_page)
        widget.setZValue(3)
        return widget

    def show_pause_page(self,bol:bool):
        if self.pause_page.isVisible() is False and bol is True:
            self.stop_game(True)
            self.pause_page.setVisible(True)
        elif self.pause_page.isVisible() is True and bol is False:
            self.stop_game(False)
            self.pause_page.setVisible(False)

    def restart_game(self):
        self.set_game_default()
        self.show_pause_page(False)
        self.show_game_over_page(False)

    def create_game_over_page(self):
        over_page = QWidget()
        over_page.setGeometry(0,0,854,480)
        over_page.setStyleSheet('background-color: transparent')

        over_txt = QLabel(over_page)
        over_txt.setText('YOU DESTROYED!')
        over_txt.setFont(QFont('Courier, monospace',40))
        over_txt.setGeometry(0,50,100,40)

        restart_button = create_button(over_page, 'Restart', QRect(0, 300, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        restart_button.clicked.connect(self.restart_game)
        choose_button = create_button(over_page,'Choose player',QRect(0,350,100,20),
                      'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                      '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                      '                    font-size: 20px;}'
                      'QPushButton:hover {color: rgb(219,203,180)}')
        choose_button.clicked.connect(lambda: self.view.setScene(self.choose_menu))
        main_menu_button = create_button(over_page, 'Main menu', QRect(0, 400, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        main_menu_button.clicked.connect(lambda: self.view.setScene(self.main_menu))
        widget = self.addWidget(over_page)
        widget.setZValue(3)
        return widget

    def show_game_over_page(self,bol:bool):
        if self.game_over_page.isVisible() is False and bol is True:
            self.stop_game(True)
            self.game_over_page.setVisible(True)
        elif self.game_over_page.isVisible() is True and bol is False:
            self.stop_game(False)
            self.game_over_page.setVisible(False)

    def create_card_page(self):
        self.types_cards = [
            ['Blessing', 'you lucky, you are blessed from the Universe. Gain you 1 HP', [('player2', 'hp', '+1')], -1],
            ['OnePanchMan', '100 pull-ups, 100 push-ups, 100 crunches, 10km run. your damage + 10', [('player2', 'damage',
             '+10')], -1],
            ['Snake shoot','your shoot is very s-s-snake, but enemies will be more various',[('scene','bullet_type','+1'),('scene','enemy_types','+1')],1]
            # хуйня, переделывай тк нельзя нормально что либо сделать
        ]
        self.card_objs = []
        backgr = self.addRect(QRectF(0,0,self.width(),self.height()*(10/8)),QPen(Qt.PenStyle.NoPen),QBrush(QColor(20,20,20,200)))
        backgr.setZValue(3)
        self.card_objs.append(backgr)
        count = 3
        self.cards = []
        for i in range(count):
            card_width = int((self.width() / count) * 0.85)
            card_height = int(self.height() * 0.8)
            card_position_x = (i*(int(self.width()) - card_width - 50) // 2) + 25
            card_position_y = (int(self.height()*(10/8)) - card_height) // 2

            card_rect = self.addRect(QRectF(card_position_x, card_position_y, card_width, card_height),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
            card_rect.setZValue(3)
            self.card_objs.append(card_rect)

            card_text = self.addText('nothing')
            card_text.setZValue(3)
            self.card_objs.append(card_text)
            card_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
            card_text.setDefaultTextColor(QColor(200,200,200))
            card_text.setFont(QFont('Courier New, monospace;',14))
            card_text.setTextWidth(card_width-10)
            card_text.setPos(card_position_x + 5, card_position_y + 5)

            card = QPushButton()
            card.setGeometry(card_position_x,card_position_y,card_width,card_height)
            card.setStyleSheet('QPushButton:hover{background-color:rgba(100,50,50,100)}'
                               'QPushButton{background-color:rgba(0,0,0,0);border:none;}'
                               'QPushButton:pressed{background-color:rgba(50,50,150,100)}')
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            card_widget = self.addWidget(card)
            card_widget.setZValue(3) # пересоздавать виджет и еще с массивами нужно поработать
            self.card_objs.append(card_widget)
            self.cards.append((card_text, card))# <- вот его и еще там есть другой в них нужно будет обновить информацию

    def Set_Content(self,way_for_eff,card:any,Name:str,description:str,effects:list,sign):
        card[0].setPlainText(f'{Name}\n\n\n\n{description}')
        # for i in range(len(effects)): # effects = [( object(player), effect(HP_O), value(+10) )]
        for i in range(len(effects)):
            obj = getattr(way_for_eff, effects[i][0])
            card[1].clicked.connect(lambda :print('e e cha-cha cha-cha'))
            card[1].clicked.disconnect()
            card[1].clicked.connect(lambda: setattr(obj, effects[i][1], eval(f'{getattr(obj,effects[i][1])}{effects[i][2]}')))
            card[1].clicked.connect(lambda: self.show_card_page(False))
        if sign > 0:
            card[1].clicked.connect(lambda:self.abobe(Name))


    def abobe(self, name):
        for j in range(len(self.types_cards)):
            if self.types_cards[j][0] == name:
                self.types_cards[j][3] -= 1
                print(self.types_cards[j])
    def randomize_cards(self, way_to_attr):
        for card in self.cards:
            name, description, effects, sign = random.choice(list(self.types_cards))
            while sign == 0:
                name, description, effects, sign = random.choice(list(self.types_cards))
            self.Set_Content(way_to_attr, card, name, description, effects, sign)


    def show_card_page(self,bol):
        if bol == '?':
            if self.card_objs[0].isVisible() is False:
                return False
            else: return True
        elif bol is True and self.card_objs[0].isVisible() is False:
            self.randomize_cards(self)
            self.stop_game(True)
            for obj in self.card_objs:
                obj.setVisible(True)
        elif bol is False and self.card_objs[0].isVisible() is True:
            self.stop_game(False)
            for obj in self.card_objs:
                obj.setVisible(False)



    def interface(self):
        background = self.addRect(self.boundingRect(), QPen(Qt.PenStyle.NoPen), QBrush(QColor(100,100,100)))
        info_bar = self.addRect(QRectF(0, self.height(), self.width(), ((self.height() * (10 / 8)) - self.height())),
                     QPen(Qt.PenStyle.NoPen), QBrush(QColor(50, 50, 50)))
        left_cover = self.addRect(self.boundingField().x(),0,abs(self.boundingField().x()-self.boundingRect().x()),self.height() * (10 / 8),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
        left_cover.setZValue(3)
        right_cover = self.addRect(self.width(),0,self.boundingField().width(),self.height() * (10 / 8),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
        right_cover.setZValue(3)
        self.hps = []
        self.timer_text = self.addText('00:00:00')
        self.timer_text.setDefaultTextColor(QColor('white'))
        self.timer_text.setFont(QFont('Courier New, monospace;',25))
        self.timer_text.setPos(self.width()-200,self.height())
        # self.create_card_page()
        self.create_card_page()
        self.show_card_page(False)
        self.pause_page = self.create_pause_game()
        self.show_pause_page(False)
        self.game_over_page = self.create_game_over_page()
        self.show_game_over_page(False)
        self.randomize_cards(self)


class View_game(QGraphicsView):
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


class View_Menu(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,1120,600)
        self.setMinimumSize(1120,600)
        self.setBackgroundBrush(QColor(0, 0, 0))
        self.showMaximized()

        main_menu = main_page(self)
        choose_player_menu = choose_player_page(self)
        game = Scene_game(self)
        # pause_menu = pause_page(self)

        main_menu.choose_player_menu = choose_player_menu
        choose_player_menu.game = game
        choose_player_menu.twomode()
        choose_player_menu.main_menu = main_menu
        # game.pause_menu = pause_menu
        game.main_menu = main_menu
        game.choose_menu = choose_player_menu
        # pause_menu.main_menu = main_menu
        # pause_menu.game = game

        self.setScene(main_menu)
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
    # game = Scene_game()
    # game_window = View_game(game)
    # game_window.show()
    # fullscreen = 0
    # timer = QTimer()
    # timer.timeout.connect(lambda: toggle_fullscreen(game_window))
    # timer.start(10)
    menu = View_Menu()
    menu.show()
    sys.exit(app.exec())

    # что если враги за экраном будут постоянно уменьшать свой шаг, так, теоретически можно не прибегая к обольшй карте сделать хранение врагов почти бесконечним
    #  например -500 дальше враг имеет меньшую строрость и так далее а когда приблежаентся ко мне то увеличивает ее
    # добавить в подкласс creation def - чтобы можно было при определенном def создавать пули, врагов по разному
    # импортируй в bullets enemies: movepattern, spawn_pos