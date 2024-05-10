import sys
import threading
from math import ceil, sqrt
import random

from PyQt6.QtCore import QPoint, QSize, QRectF, Qt, QTimer, QPointF, QRect
from PyQt6.QtGui import QColor, QPainter, QBrush, QFont, QPixmap, QPen, QTextOption, QPalette
from PyQt6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QWidget, \
    QLabel, QPushButton, QStackedWidget, QVBoxLayout, QStyle, QMainWindow, QGraphicsEffect, QGraphicsProxyWidget

import Bullets
import Cards
import Enemies

chosen_player = 0

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
        global chosen_player
        chosen_player = self.chosen_player
        players = self.game.players
        self.game.set_player(self.game,self.game.player,players,self.chosen_player)
        self.about_player_txt.setPlainText(f"Name: {self.game.players[self.chosen_player][0]} \n"
                                      f"Health: {self.game.player.hp} \n"
                                      f"Speed: {self.game.player.step} \n"
                                      f"Soap move: {self.game.player.soap_koef} \n"
                                      f"Damage: {self.game.player.damage} \n"
                                      f"Speed shoot: {self.game.player.speed_shoot} \n"
                                      f"Size: {self.game.player.size_x}")
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

        self.cards = []
        self.array_enemies = Enemies.array_enemies
        self.array_bullets = Bullets.array_bullets
        self.array_arrays = [self.array_enemies, self.array_bullets]

        # players = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.players = [
            ('Default',      3,  1,      4,    1,        370,         25,     25,     QColor(0, 0, 255)),
            ('IFeelPain',    1,  0.5,    7,    2,        290,         20,     20,     QColor(200, 150, 0)),
            ('UPower',       5,  2,      4,    3,        420,         30,     30,     QColor(100, 255, 255))
        ]
        # enemies = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.enemies = Enemies.enemies
        # bullets = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.bullets = Bullets.bullets

        self.player_timer = QTimer()
        self.player_chtimer = QTimer()
        self.player = self.fabrick_rectobj(self)
        self.set_player(self,self.player,self.players,0)
        self.player.setZValue(1)

        self.events_timer = QTimer()
        self.events_timer.timeout.connect(self.game_events)
        self.events_timer.start(150)

        self.game_timer = QTimer()
        self.game_timer.timeout.connect(lambda :self.updateScene(self.player,self.array_enemies,self.array_bullets))
        self.set_game_default()
        self.stop_game(True)

        self.interface()


    def game_events(self):
        # if self.view.scene() != self:
        #     self.stop_game(True)
        # else:self.stop_game(False)
        pass

    def set_game_default(self):
        global chosen_player
        self.cur_worked = 0
        self.msec = 0
        self.sec = 0
        self.min = 0
        self.bullet_type = 0
        self.enemy_types = [Enemies.default_enemy]
        self.set_player(self, self.player, self.players,chosen_player)
        self.player.setPos(200,300)
        self.player.move_direction_L = 0
        self.player.move_direction_R = 0
        self.player.move_direction_U = 0
        self.player.move_direction_D = 0
        self.player.shoot = 0
        self.player.speed_l = 0
        self.player.speed_r = 0
        self.player.speed_u = 0
        self.player.speed_d = 0
        self.player.direction = 1
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

    class fabrick_rectobj(QGraphicsRectItem):
        def __init__(self,scene):
            super().__init__()
            self.setRect(0,0,10,10)
            self.setPen(QPen(Qt.PenStyle.NoPen))
            self.setBrush(QBrush(QColor('white')))
            scene.addItem(self)
            self.timer = QTimer()
            self.shoot = 0
            self.speed_l = 0
            self.speed_r = 0
            self.speed_u = 0
            self.speed_d = 0
            self.step = 0
            self.size_x = 0
            self.size_y = 0
            self.hp = 0
            self.hit_delay = 0
            self.damage = 0
            self.speed_shoot = 0
            self.move = None


    def set_player(self,scene,obj,players:list,player_type:int):
        obj.move_direction_L = 0
        obj.move_direction_R = 0
        obj.move_direction_U = 0
        obj.move_direction_D = 0
        obj.future_x = obj.x()
        obj.future_y = obj.y()
        obj.hp = players[player_type][1]
        obj.damage = players[player_type][2]
        obj.step = players[player_type][3]
        obj.soap_koef = players[player_type][4]
        obj.speed_shoot = players[player_type][5]
        obj.size_x = players[player_type][6]
        obj.size_y = players[player_type][7]

        obj.setBrush(players[player_type][8])
        obj.setRect(0,0,obj.size_x,obj.size_y)
        obj.direction_timer = QTimer()

        def move():
            if obj.timer.isActive() is False:
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

                obj.timer.timeout.connect(obj.timer.stop)
                obj.timer.start(int(obj.soap_koef*10))

            if obj.y() - obj.speed_u < 0:
                obj.setY(0)
                obj.speed_u = 0
            else:
                obj.moveBy(0, -obj.speed_u)

            if obj.y() + obj.speed_d + obj.size_y > scene.height():
                obj.setY(scene.height() - obj.size_y)
                obj.speed_d = 0
            else:
                obj.moveBy(0, obj.speed_d)

        obj.move = move

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
        if self.player.hp <= 0:
            self.show_game_over_page(True)
        for enemy in array_enemies:
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
            self.show_card_page_new(True)
            self.cur_worked = self.sec
        self.draw_time_timer_text()
        if player.shoot == 1:
            if Bullets.timer.isActive() is False:
                bullet = Bullets.default_bullet(self)
                Bullets.array_bullets.append(bullet)
                Bullets.timer.start(player.speed_shoot)
        for array in [array_enemies,array_bullets]:
            for arr_obj in array:
                arr_obj.moveBy(player.speed_l - player.speed_r, 0)
                arr_obj.move()
        if Enemies.timer.isActive() is False:
            enemy_function = random.choice(self.enemy_types)
            enemy = enemy_function(self)
            Enemies.array_enemies.append(enemy)
            Enemies.timer.start(1000)
        player.move()
        left_x,right_x = 200,self.width()-player.size_x-200
        if int(player.x()) != right_x and player.direction == 0:
            self.player_chdirection(player,self.player_chtimer,10,player.direction,right_x,[array_enemies,array_bullets])
        elif int(player.x()) != left_x and player.direction == 1:
            self.player_chdirection(player,self.player_chtimer,10,player.direction,left_x,[array_enemies,array_bullets])
        self.draw_player_hp(player.hp,50,8,self.height()+15,10,50,QColor(255,100,100))
        self.check_collision(player,array_enemies,array_bullets)
        self.update()



    def keyPressEvent(self, event):

        if event.text() in ['Ц', 'ц', 'W', 'w']:
            self.player.move_direction_U = 1

        if event.text() in ['Ф', 'ф', 'A', 'a']:
            self.player.move_direction_L = 1
            self.player.direction = 0

        if event.text() in ['Ы', 'ы', 'S', 's']:
            self.player.move_direction_D = 1

        if event.text() in ['В', 'в', 'D', 'd']:
            self.player.move_direction_R = 1
            self.player.direction = 1

        if event.text() in ['C', 'c', 'С', 'с']:
            self.player.shoot = 1

        if event.key() == Qt.Key.Key_Escape:
            if self.game_timer.isActive() is True:
                self.show_pause_page(True)

        # if event.key() == Qt.Key.Key_K:
        #     # self.show_card_page(True)
        #     self.show_card_page_new(True)


    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            global fullscreen
            if fullscreen == 1:
                fullscreen = 0
            else:
                fullscreen = 1
        # if event.key() == Qt.Key.Key_Escape:
        #     fullscreen = 0

        if event.text() in ['Ц', 'ц', 'W', 'w']:
            self.player.move_direction_U = 0

        elif event.text() in ['Ф', 'ф', 'A', 'a']:
            self.player.move_direction_L = 0

        elif event.text() in ['Ы', 'ы', 'S', 's']:
            self.player.move_direction_D = 0

        elif event.text() in ['В', 'в', 'D', 'd']:
            self.player.move_direction_R = 0

        if event.text() in ['C', 'c', 'С', 'с']:
            self.player.shoot = 0

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
        self.cards = []
        for i in range(3):
            wid = 150
            hei = 200
            card = Cards.Card(QRect(i * wid + 10, 100, wid, hei), QFont('Courier New, monospace;', 25),
                              QFont('Courier New, monospace;', 14))
            # Cards.card_blessing(card,self.player2)
            Cards.card_snake_shoot(card, self)
            card_obj = self.addWidget(card)
            self.cards.append(card_obj)

    def create_card_page_new(self):
        for i in range(3):
            wid = 200
            hei = 250
            card = random.choice(Cards.array_cards)
            card_widget = card(self,QRect(i*(wid+100),100,wid,hei),QFont('Courier New, monospace;', 25),
                              QFont('Courier New, monospace;', 14))
            card_item = self.addWidget(card_widget)
            card_item.setZValue(3)
            self.cards.append(card_item)

    def show_card_page(self,bol):
        if bol is True and self.cards[0].isVisible() is False:
            # Cards.randomize_cards(self,self.types_cards,self.cards)
            self.stop_game(True)
            for obj in self.cards:
                obj.setVisible(True)
        elif bol is False and self.cards[0].isVisible() is True:
            self.stop_game(False)
            for obj in self.cards:
                obj.setVisible(False)

    def show_card_page_new(self,bol):
        if bol is True and len(self.cards) == 0:
            self.create_card_page_new()
            self.stop_game(True)
        elif bol is False and len(self.cards) > 0:
            self.stop_game(False)
            for card in self.cards:
                card.hide()
                card.deleteLater()
            self.cards.clear()

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
        # self.create_card_page_new()
        # self.show_card_page(False)
        self.pause_page = self.create_pause_game()
        self.show_pause_page(False)
        self.game_over_page = self.create_game_over_page()
        self.show_game_over_page(False)


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
        # self.scale(0.7,0.7)
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