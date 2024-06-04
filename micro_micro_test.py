import sys
import threading
import time
from math import ceil, sqrt
import random

from PyQt6 import QtCore
from PyQt6.QtCore import QPoint, QSize, QRectF, Qt, QTimer, QPointF, QRect, QThreadPool, pyqtSignal, QThread, QObject, \
    QMutex, QRunnable, QWaitCondition, pyqtSlot
from PyQt6.QtGui import QColor, QPainter, QBrush, QFont, QPixmap, QPen, QTextOption, QPalette, QPainterPath, QTransform
from PyQt6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QWidget, \
    QLabel, QPushButton, QStackedWidget, QVBoxLayout, QStyle, QMainWindow, QGraphicsEffect, QGraphicsProxyWidget


import Bullets
import Cards
import Enemies

Screen_Resolution = (1280,720)

chosen_player = 0

def create_txt_widget(scene,name: str, fontstyle: str,textcolor:QColor,fontsize:int, pos:QPointF):
    txt = QGraphicsTextItem()
    txt.setDefaultTextColor(textcolor)
    txt.setPlainText(name)
    txt.setFont(QFont(fontstyle,fontsize))
    txt.setPos(pos)
    scene.addItem(txt)
    return txt

def create_txt(widget:QWidget,name:str,fontstyle:str,textcolor:str,fontsize:int,pos:QPoint,size:QSize):
    txt = QLabel(f'{name}',widget)
    txt.setStyleSheet(f'color:{textcolor}')
    txt.setFont(QFont(fontstyle,fontsize))
    txt.setGeometry(QRect(pos,size))
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

class main_page(QWidget):
    def __init__(self,view,stack_widget:QStackedWidget):
        super().__init__()
        self.setGeometry(0,0,600,600)
        self.setStyleSheet('background-color: transparent')
        self.Main_title = create_txt(self,'STAR DEFENDER','Courier, monospace','rgba(200,200,200,50)',60,QPoint(0,50),QSize(700,60))
        self.start_button = create_button(self, 'Start', QRect(0, 300, 100, 20),
                       'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                       '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                       '                    font-size: 20px;}'
                       'QPushButton:hover {color: rgb(219,203,180)}')
        self.start_button.clicked.connect(lambda: stack_widget.setCurrentIndex(1))
        self.start_button.clicked.connect(lambda: stack_widget.show())
        self.exit_button = create_button(self, 'Exit', QRect(0, 350, 100, 20),
                     'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                     '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                     '                   font-size:20px}'
                     'QPushButton:hover {color: rgb(219,203,180)}')
        self.exit_button.clicked.connect(view.close)

class choose_player_page(QWidget):
    def __init__(self,view,stack_widget:QStackedWidget):
        super().__init__()
        self.setGeometry(0, 0, 600, 600)
        self.setStyleSheet('background-color: transparent')
        self.stack_widget = stack_widget
        self.view = view
        self.game = self.view.game
        self.choose_player_txt = create_txt(self,'CHOOSE PLAYER','Courier, monospace','rgba(200,200,200,50)',30,QPoint(0,50),QSize(300,30))
        self.about_player_txt = create_txt(self,'About player','Courier New, monospace','rgb(200,200,200)',15,QPoint(300,300),QSize(200,15))
        self.back_button = create_button(self, 'back', QRect(600, 200, 100, 20),
                       'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                       '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                       '                    font-size: 20px;}'
                       'QPushButton:hover {color: rgb(219,203,180)}')
        self.chosen_player = 0
        self.back_button.clicked.connect(self.onemode)
        self.next_button = create_button(self, 'next', QRect(700, 200, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        self.next_button.clicked.connect(self.twomode)
        self.play_button = create_button(self, 'Play', QRect(600, 350, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        self.play_button.clicked.connect(lambda: self.restart_game())
        self.main_menu_button = create_button(self, 'Got to menu', QRect(0, 350, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        self.main_menu_button.clicked.connect(lambda: stack_widget.setCurrentIndex(0))
        self.main_menu_button.clicked.connect(lambda: stack_widget.show())

    def restart_game(self):
        self.game.restart_game()
        self.stack_widget.hide()

    def draw_actual_info(self):
        global chosen_player
        chosen_player = self.chosen_player
        players = self.game.players
        self.game.set_player(self.game,self.game.player,players,self.chosen_player)
        self.about_player_txt.setText(f"Name: {self.game.players[self.chosen_player][0]} \n"
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


class Scene_game(QGraphicsScene):
    def __init__(self,view,stack_widget:QStackedWidget):
        super().__init__()

        self.setSceneRect(0,0,Screen_Resolution[0],(Screen_Resolution[1]*0.8))
        # self.setSceneRect(0,0,854,(480*0.8))
        # self.setSceneRect(0,0,480,(270*0.8))
        self.view = view
        self.scene = self
        self.stack_widget = stack_widget

        self.cards = []
        self.array_enemies = Enemies.array_enemies
        self.array_bullets = Bullets.array_bullets
        self.array_arrays = [self.array_enemies, self.array_bullets]

        # players = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.players = [
            ('Default',      5,  1,      4,    1,        370,         20,     20,     QBrush(QColor(0, 0, 255))),
            ('IFeelPain',    3,  0.5,    7,    2,        290,         15,     15,     QBrush(QPixmap('arrow_right.png'))),
            ('UPower',       6,  2,      4,    2,        420,         30,     30,     QBrush(QColor(100, 255, 255)))
        ]
        # enemies = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.enemies = Enemies.enemies
        # bullets = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.bullets = Bullets.bullets
        self.key_up_pressed = 0
        self.key_down_pressed = 0

        self.player_timer = QTimer()
        self.player_chtimer = QTimer()
        self.player = self.fabrick_rectobj(self)
        self.player.current_bullet_method = Bullets.triple_like_method
        self.player.current_bullet_type = Bullets.default_bullet
        self.set_player(self,self.player,self.players,0)
        self.player.setZValue(1)

        self.check_collision_thread = self.check_collision_thread_class()
        self.check_collision_thread.request_data.connect(self.update_check_data)
        self.check_collision_thread.enemy_visible_true.connect(self.enemy_visible_true)
        self.check_collision_thread.enemy_visible_false.connect(self.enemy_visible_false)
        self.check_collision_thread.deal_damage_enemy.connect(self.deal_damage_enemy)
        self.check_collision_thread.enemy_delete.connect(self.enemy_delete)
        self.check_collision_thread.bullet_delete.connect(self.bullet_delete)
        self.check_collision_thread.change_player_speed_and_hp.connect(self.change_player_speed_and_hp)

        self.game_timer = QTimer()
        self.game_timer.timeout.connect(lambda :self.updateScene(self.player,self.array_enemies,self.array_bullets))
        self.set_game_default()

        self.interface()
        self.stop_game(True)
        self.thread_timer = QTimer()
        self.thread_timer.timeout.connect(self.thread_timer.stop)
        self.check_collision_finished = True
        self.count_finished = 0


    @pyqtSlot()
    def start_check(self):
        if not self.check_collision_thread.isRunning():
            self.check_collision_thread.start()
    @pyqtSlot()
    def stop_check(self):
        self.check_collision_thread.stop()
    @pyqtSlot()
    def update_check_data(self):
        # self.check_collision_thread.receive_data(16,self.boundingRect(),self.boundingField(),self.player,self.array_enemies,self.array_bullets)
        self.check_collision_thread.receive_data(16,self.itemsBoundingRect(),self.boundingField(),self.player,self.array_enemies,self.array_bullets)
    @pyqtSlot(object,float)
    def deal_damage_enemy(self,enemy,damage):
        if enemy in self.array_enemies:
            enemy.hp -= damage
    @pyqtSlot(object)
    def enemy_delete(self,enemy):
        if enemy in self.array_enemies:
            Enemies.delete_enemy(self,enemy)
    @pyqtSlot(object)
    def enemy_visible_false(self,enemy):
        for object in self.array_enemies:
            if object == enemy:
                object.setVisible(False)
                break
    @pyqtSlot(object)
    def enemy_visible_true(self,enemy):
        for object in self.array_enemies:
            if object == enemy:
                object.setVisible(True)
                break
    @pyqtSlot(object)
    def bullet_delete(self,bullet):
        if bullet in self.array_bullets:
            Bullets.array_bullets.remove(bullet)
            self.removeItem(bullet)

    @pyqtSlot(float,float,float,float,int)
    def change_player_speed_and_hp(self,speed_l,speed_r,speed_u,speed_d,damage):
        print('player_damaged')
        self.player.hit_delay.start(500)
        self.player.hp -= damage
        self.player.speed_l = speed_l
        self.player.speed_r = speed_r
        self.player.speed_u = speed_u
        self.player.speed_d = speed_d
        if self.player.hp <= 0:
            self.show_game_over_page(True)

    class check_collision_thread_class(QThread):
            request_data = pyqtSignal()
            receive_data = pyqtSlot(object)
            finished = pyqtSignal()
            deal_damage_enemy = pyqtSignal(object,float)
            enemy_delete = pyqtSignal(object)
            enemy_visible_false = pyqtSignal(object)
            enemy_visible_true = pyqtSignal(object)
            bullet_delete = pyqtSignal(object)
            change_player_speed_and_hp = pyqtSignal(float,float,float,float,int)
            def __init__(self):
                super().__init__()
                self.is_running = False
                self.speed_update = None
                self.scene_boundingRect = None
                self.scene_boundingField = None
                self.player = None
                self.array_enemies = None
                self.array_bullets = None
            def run(self):
                self.is_running = True
                while self.is_running:
                    self.request_data.emit()
                    if (self.scene_boundingRect is not None and self.scene_boundingField is not None and
                            self.player is not None and self.array_enemies is not None and
                            self.array_bullets is not None and self.speed_update is not None):
                        player_rect = QRectF(self.player.x(), self.player.y(), self.player.size_x, self.player.size_y)
                        for enemy in self.array_enemies:
                            enemy_rect = QRectF(enemy.x(), enemy.y(), enemy.size_x, enemy.size_y)
                            if enemy_rect.intersects(
                                    self.scene_boundingRect) is False and enemy.isVisible() is True:
                                self.enemy_visible_false.emit(enemy)
                            elif enemy_rect.intersects(
                                    self.scene_boundingRect) is True and enemy.isVisible() is False:
                                self.enemy_visible_true.emit(enemy)
                            # if player_rect.intersects(enemy_rect):
                            # if self.player.shape().intersects(enemy.shape()):
                            if self.player.collidesWithItem(enemy):
                                self.player_damaged = 0
                                if self.player.hit_delay.isActive() is False:
                                    self.player_damaged = 0
                                self.player_speed_l = 0
                                self.player_speed_r = 0
                                self.player_speed_u = 0
                                self.player_speed_d = 0

                                if player_rect.center().x() < enemy_rect.center().x():
                                    self.player_speed_r = 0
                                    self.player_speed_l = (self.player.step + enemy.step) * 0.5

                                elif player_rect.center().x() > enemy_rect.center().x():
                                    self.player_speed_l = 0
                                    self.player_speed_r = (self.player.step + enemy.step) * 0.5

                                elif player_rect.center().y() < enemy_rect.center().y():
                                    self.player_speed_d = 0
                                    self.player_speed_u = (self.player.step + enemy.step) * 0.5

                                elif player_rect.center().y() > enemy_rect.center().y():
                                    self.player_speed_u = 0
                                    self.player_speed_d = (self.player.step + enemy.step) * 0.5

                                self.change_player_speed_and_hp.emit(self.player_speed_l,self.player_speed_r,
                                                                         self.player_speed_u,self.player_speed_d,self.player_damaged)


                            if self.scene_boundingField.contains(enemy_rect) is False:
                                self.enemy_delete.emit(enemy)
                                continue
                            if enemy.isVisible() is False:
                                continue
                            else:
                                for bullet in self.array_bullets:
                                    bullet_rect = QRectF(bullet.x(), bullet.y(), bullet.size_x, bullet.size_y)
                                    if self.scene_boundingRect.intersects(bullet_rect) is False:
                                        self.bullet_delete.emit(bullet)
                                        continue
                                    if enemy_rect.intersects(bullet_rect):
                                        self.bullet_delete.emit(bullet)
                                        damage = (bullet.damage * self.player.damage)
                                        self.deal_damage_enemy.emit(enemy,damage)
                                        if enemy.hp <= 0 and enemy in self.array_enemies:
                                            self.enemy_delete.emit(enemy)
                        self.msleep(self.speed_update)
                self.finished.emit()
            def stop(self):
                self.is_running = False
                self.wait()
            @pyqtSlot(object)
            def receive_data(self,speed_update:int,scene_boundingRect,scene_boundingField,player,array_enemies,array_bullets):
                self.speed_update = speed_update
                self.scene_boundingRect = scene_boundingRect
                self.scene_boundingField = scene_boundingField
                self.player = player
                self.array_enemies = array_enemies
                self.array_bullets = array_bullets

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
            self.stop_check()
        else:
            self.game_timer.start(16)
            self.start_check()

    # def boundingRect(self):
    #     return QRectF(0,0,self.width(),self.height()*(10/8))
    def itemsBoundingRect(self):
        return QRectF(0, 0, self.width(), self.height() * (10 / 8))
    def boundingField(self):
        return QRectF(-1000, -100, (self.width() + 2000), (self.height())+200)

    class fabrick_rectobj(QGraphicsRectItem):
        def __init__(self,scene):
            super().__init__()
            self.setRect(0,0,10,10)
            # self.setPen(QPen(Qt.PenStyle.NoPen))
            self.brush = QBrush(QColor('gray'))
            scene.addItem(self)
            self.timer = QTimer()

            self.direction_timer = QTimer()
            self.shoot = 0
            self.direction = 1
            self.move_direction_L = 0
            self.move_direction_R = 0
            self.move_direction_U = 0
            self.move_direction_D = 0
            self.soap_koef = 0
            self.future_x = 0
            self.future_y = 0
            self.speed_l = 0
            self.speed_r = 0
            self.speed_u = 0
            self.speed_d = 0
            self.step = 0
            self.size_x = 0
            self.size_y = 0
            self.hp = 0
            self.hit_delay = QTimer()
            self.hit_delay.timeout.connect(self.hit_delay.stop)
            self.damage = 0
            self.speed_shoot = 0
            self.current_bullet_method = None
            self.current_bullet_type = None
            self.move = None

        def boundingRect(self):
            return self.rect()

        def shape(self):
            path = QPainterPath()
            path.addRect(self.boundingRect())
            return path
        def paint(self, painter: QPainter, option, widget=None):
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            painter.setBrush(self.brush)
            painter.drawRect(self.rect())
            # painter.setBrush(QBrush(QColor(0,0,255)))
            # painter.drawPath(self.shape())


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

        # obj.setBrush(players[player_type][8])
        obj.brush = players[player_type][8]
        obj.setRect(0,0,obj.size_x,obj.size_y)

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

    def updateScene(self,player,array_enemies,array_bullets):
        self.msec += 1
        # if self.sec % 10 == 0 and self.cur_worked != self.sec:
        #     self.show_card_page_new(True)
        #     self.cur_worked = self.sec
        self.draw_time_timer_text()
        if player.shoot == 1:
            if Bullets.timer.isActive() is False:
                bullet_type = Bullets.chaos_bullet
                # bullet = Bullets.triple_method(self,bullet_type)
                bullet = player.current_bullet_method(self,player.current_bullet_type,Bullets.first_arg_method,Bullets.second_arg_mothod)
                Bullets.timer.start(player.speed_shoot+bullet.speed_shoot)
        for array in [array_enemies,array_bullets]:
            for arr_obj in array:
                arr_obj.moveBy(player.speed_l - player.speed_r, 0)
                arr_obj.move()
        if Enemies.timer.isActive() is False and len(Enemies.array_enemies) < 20:

            type_enemy = random.choice([Enemies.default_enemy,Enemies.ping_pong_enemy,Enemies.mother_enemy,Enemies.static_ss_enemy,Enemies.boss_enemy])
            enemy = type_enemy(self)
            print(len(Enemies.array_enemies))
            Enemies.timer.start(50)
        player.move()
        left_x,right_x = 200,self.width()-player.size_x-200
        if int(player.x()) != right_x and player.direction == 0:
            self.player_chdirection(player,self.player_chtimer,10,player.direction,right_x,[array_enemies,array_bullets])
        elif int(player.x()) != left_x and player.direction == 1:
            self.player_chdirection(player,self.player_chtimer,10,player.direction,left_x,[array_enemies,array_bullets])
        self.draw_player_hp(player.hp,50,8,self.height()+15,10,50,QColor(255,100,100))
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

        if event.key() == Qt.Key.Key_Up:
            self.key_up_pressed = 1
        if event.key() == Qt.Key.Key_Down:
            self.key_down_pressed = 1

        if event.key() == Qt.Key.Key_K:
            # self.show_card_page(True)
            self.show_card_page_new(True)


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

        if event.key() == Qt.Key.Key_Up:
            self.key_up_pressed = 0
        if event.key() == Qt.Key.Key_Down:
            self.key_down_pressed = 0

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
            hp.setZValue(3)
            hp.setPos(x,y)
            hp.size_x = w
            hp.size_y = h
            self.hps.append(hp)
        elif len(self.hps) < count_hp and len(self.hps) > 0:
            last_hp = self.hps[-1]
            hp = self.addRect(0,0,w,h,QPen(Qt.PenStyle.NoPen),QBrush(color))
            hp.setZValue(3)
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
        pause_page.setGeometry(0,0,Screen_Resolution[0],Screen_Resolution[1])
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
        main_menu_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        main_menu_button.clicked.connect(lambda: self.stack_widget.show())
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
        over_page.setGeometry(0,0,Screen_Resolution[0],Screen_Resolution[1])
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
        choose_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))
        choose_button.clicked.connect(lambda: self.stack_widget.show())
        main_menu_button = create_button(over_page, 'Main menu', QRect(0, 400, 100, 20),
                        'QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;'
                        '                   text-align: left; margin: 0px; background-color: rgba(255,0,0,0);'
                        '                    font-size: 20px;}'
                        'QPushButton:hover {color: rgb(219,203,180)}')
        main_menu_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        main_menu_button.clicked.connect(lambda: self.stack_widget.show())
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
        count = 3
        for i in range(count):
            wid = int(self.width()*0.25)
            hei = int(self.height()*0.8)
            beetwen = 100
            end_x = (count-1)*(wid+beetwen)+wid
            start_x = int((self.width()-end_x)/2)
            start_y = int((self.height()*(10/8)-hei)/2)
            card = random.choice(Cards.array_cards)
            card_widget = card(self,QRect(i*(wid+beetwen)+start_x,start_y,wid,hei),QFont('Courier New, monospace;', 25),
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
        # background = self.addRect(self.boundingRect(), QPen(Qt.PenStyle.NoPen), QBrush(QColor(100,100,100)))
        background = self.addRect(self.itemsBoundingRect(), QPen(Qt.PenStyle.NoPen), QBrush(QColor(100,100,100)))
        info_bar = self.addRect(QRectF(0, self.height(), self.width(), ((self.height() * (10 / 8)) - self.height())),
                     QPen(Qt.PenStyle.NoPen), QBrush(QColor(50, 50, 50)))
        info_bar.setZValue(3)
        # left_cover = self.addRect(self.boundingField().x(),0,abs(self.boundingField().x()-self.boundingRect().x()),self.height() * (10 / 8),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
        # left_cover.setZValue(3)
        # right_cover = self.addRect(self.width(),0,self.boundingField().width(),self.height() * (10 / 8),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
        # right_cover.setZValue(3)
        self.hps = []
        self.timer_text = self.addText('00:00:00')
        self.timer_text.setDefaultTextColor(QColor('white'))
        self.timer_text.setFont(QFont('Courier New, monospace;',25))
        self.timer_text.setPos(self.width()-200,self.height())
        self.timer_text.setZValue(3)
        # self.create_card_page_new()
        # self.show_card_page(False)
        self.pause_page = self.create_pause_game()
        self.show_pause_page(False)
        self.game_over_page = self.create_game_over_page()
        self.show_game_over_page(False)


# class View_game(QGraphicsView):
#     def __init__(self, scene):
#         super().__init__(scene)
#         self.setGeometry(0,0,1120,600)
#         self.setMinimumSize(1120,600)
#         self.setBackgroundBrush(QColor(0, 0, 0))
#         self.showMaximized()
#         self.setScene(scene)
#         # self.setSceneRect(0,0,1120,600)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.setAlignment(Qt.AlignmentFlag.AlignTop)
#         # self.scale(0.6,0.6)
#         self.setStyleSheet('border:none')
#
#     def resizeEvent(self, event):
#         self.fitInView(QRectF(0,0,849,475), Qt.AspectRatioMode.KeepAspectRatio)


class View_Menu(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,1120,600)
        self.setMinimumSize(1120,600)
        self.setBackgroundBrush(QColor(0, 0, 0))
        # self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.showMaximized()
        stack_widget = QStackedWidget()
        stack_widget.setStyleSheet('background-color: rgba(0,0,0,150)')
        # stack_widget.setGeometry(0,0,854,480)
        stack_widget.setGeometry(0,0,Screen_Resolution[0],Screen_Resolution[1])
        self.game = Scene_game(self,stack_widget)
        main_menu = main_page(self,stack_widget)
        stack_widget.addWidget(main_menu)
        choose_player_menu = choose_player_page(self,stack_widget)
        stack_widget.addWidget(choose_player_menu)
        choose_player_menu.twomode()
        self.setScene(self.game)
        stack_widget_scene = self.game.addWidget(stack_widget)
        stack_widget_scene.setZValue(3)
        # self.setSceneRect(0,0,1120,600)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scale(0.7,0.7)
        self.setStyleSheet('border:none')

    def closeEvent(self, a0):
        self.game.stop_game(True)
        a0.accept()

    # def resizeEvent(self, event):
    #     # self.fitInView(QRectF(0,0,1019,571), Qt.AspectRatioMode.KeepAspectRatio)
    #     self.fitInView(QRectF(0,0,Screen_Resolution[0]-5,Screen_Resolution[1]-5), Qt.AspectRatioMode.KeepAspectRatio)
    #     # self.fitInView(QRectF(0,0,849,475), Qt.AspectRatioMode.KeepAspectRatio)

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