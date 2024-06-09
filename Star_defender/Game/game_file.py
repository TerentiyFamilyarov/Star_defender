import os
import sys
import threading
import time
from math import ceil, sqrt
import random

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QPoint, QSize, QRectF, Qt, QTimer, QPointF, QRect, QThreadPool, pyqtSignal, QThread, QObject, \
    QMutex, QRunnable, QWaitCondition, pyqtSlot
from PyQt6.QtGui import QColor, QPainter, QBrush, QFont, QPixmap, QPen, QTextOption, QPalette, QPainterPath, QTransform, \
    QEnterEvent
from PyQt6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QWidget, \
    QLabel, QPushButton, QStackedWidget, QVBoxLayout, QStyle, QMainWindow, QGraphicsEffect, QGraphicsProxyWidget, \
    QGraphicsPixmapItem

from Bullets import bullets_file
from Enemies import enemies_file
from Cards import cards_file

Screen_Resolution = (1280, 720)
# main_font = "Tempus Sans ITC"


class FontLoader:
    @staticmethod
    def load_font(font_path):
        if not os.path.exists(font_path):
            print(f"Font file not found: {font_path}")
            return None

        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Failed to load font from {font_path}")
            return None

        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)
        if font_family:
            return font_family[0]

        print(f"Failed to retrieve font family for {font_path}")
        return None


chosen_player = 0


def create_txt(widget: QWidget, name: str, fontstyle: str, textcolor: str, fontsize: int, pos: QPoint):
    txt = QLabel(f'{name}', widget)
    txt.setStyleSheet(f'color:{textcolor}')
    txt.setFont(QFont(fontstyle, fontsize))
    txt.move(pos)
    return txt


def create_button(parent, txt: str, pos: QPoint, style: str):
    button = QPushButton(parent)
    button.setText(txt)
    button.move(pos)
    button.setStyleSheet(style)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    return button


class MainPage(QWidget):
    def __init__(self, game, stack_widget: QStackedWidget):
        super().__init__()
        self.setGeometry(0, 0, Screen_Resolution[0], Screen_Resolution[1])
        self.setStyleSheet('background-color: transparent')
        self.main_title = create_txt(
            self, 'STAR DEFENDER', main_font,
            'rgba(200,200,200,150)', 70, QPoint(0, 50))
        self.main_title.setFixedWidth(self.width())
        self.main_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_button = create_button(self, 'Start', QPoint(0, 400), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.start_button.setFont(QFont(main_font))
        self.start_button.clicked.connect(lambda: stack_widget.setCurrentIndex(1))
        self.exit_button = create_button(self, 'Exit', QPoint(0, 450), '''                              
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size:30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.exit_button.setFont(QFont(main_font))
        self.exit_button.clicked.connect(game.view.close)


class ChoosePlayerPage(QWidget):
    def __init__(self, game, stack_widget: QStackedWidget):
        super().__init__()
        self.setGeometry(0, 0, Screen_Resolution[0], Screen_Resolution[1])
        label_pix = QLabel(self)
        label_pix.setStyleSheet('padding:0px')
        label_pix.setPixmap(QPixmap('../Game/images/player_info_field.png'))
        label_pix.move(600,330)
        self.setStyleSheet('background-color: transparent')
        self.stack_widget = stack_widget
        self.game = game
        self.choose_player_txt = create_txt(
            self, 'CHOOSE PLAYER', main_font,
            'rgba(200,200,200,150)', 40, QPoint(0, 50))
        self.about_player_txt = create_txt(
            self, 'About player', main_font,
            'rgb(200,200,200)', 25, QPoint(660, 360))
        self.back_button = create_button(self, 'back', QPoint(850, 100), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.back_button.setFont(QFont(main_font))
        self.chosen_player = 0
        self.back_button.clicked.connect(self.back_ship)
        self.next_button = create_button(self, 'next', QPoint(1000, 100), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.next_button.setFont(QFont(main_font))
        self.next_button.clicked.connect(self.next_ship)
        self.play_button = create_button(self, 'Play', QPoint(850, 250), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.play_button.setFont(QFont(main_font))
        self.play_button.clicked.connect(lambda: self.restart_game())
        self.main_menu_button = create_button(self, 'Go to menu', QPoint(0, 450), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0); word-spacing: -10px;
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.main_menu_button.setFont(QFont(main_font))
        self.main_menu_button.clicked.connect(lambda: stack_widget.setCurrentIndex(0))

        self.player_pixmap = QPixmap('')

    def restart_game(self):
        self.game.restart_game()
        self.game.stack_proxy_widget.setVisible(False)

    def draw_actual_info(self):
        global chosen_player
        chosen_player = self.chosen_player
        players = self.game.players
        self.game.set_player(self.game, self.game.player, players, self.chosen_player)
        self.about_player_txt.setText(f"Name: {self.game.players[self.chosen_player][0]} \n"
                                      f"Health: {self.game.player.hp} \n"
                                      f"Speed: {self.game.player.step} \n"
                                      f"Breaking speed: {self.game.player.soap_koef * 100}% \n"
                                      f"Damage: {self.game.player.damage} \n"
                                      f"Shoot cooldown: {self.game.player.speed_shoot} \n"
                                      f"Size: {self.game.player.size_x}")
        self.player_pixmap.load(self.game.players[chosen_player][8])
        self.update()

    def back_ship(self):
        self.chosen_player -= 1
        maxx = len(self.game.players) - 1
        if self.chosen_player < 0:
            self.chosen_player = len(self.game.players) - 1
        elif self.chosen_player > maxx:
            self.chosen_player = 0
        self.draw_actual_info()

    def next_ship(self):
        self.chosen_player += 1
        maxx = len(self.game.players) - 1
        if self.chosen_player < 0:
            self.chosen_player = len(self.game.players) - 1
        elif self.chosen_player > maxx:
            self.chosen_player = 0
        self.draw_actual_info()

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.drawPixmap(600, 100, 200, 200, QPixmap('../Game/images/draw_player_field.png'))
        painter.drawPixmap(
            QRectF(700-(self.game.player.size_x*4)//2, 200-(self.game.player.size_y*4)//2,
                   self.game.player.size_x*4, self.game.player.size_y*4).toRect(), self.player_pixmap)


class PausePage(QWidget):
    def __init__(self, game, stack_widget: QStackedWidget):
        super().__init__()
        self.game = game
        self.stack_widget = stack_widget
        self.setGeometry(0, 0, Screen_Resolution[0], Screen_Resolution[1])
        self.setStyleSheet('background-color: transparent')
        self.pause_txt = create_txt(
            self, 'PAUSE', main_font, 'rgba(200,200,200,150)', 40, QPoint(0, 50))
        self.resume_button = create_button(self, 'Resume', QPoint(0, 350), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.resume_button.setFont(QFont(main_font))
        self.resume_button.clicked.connect(lambda: self.game.stack_proxy_widget.setVisible(False))
        self.resume_button.clicked.connect(lambda: self.game.stop_game(False))
        self.restart_button = create_button(self, 'Restart', QPoint(0, 400), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.restart_button.setFont(QFont(main_font))
        self.restart_button.clicked.connect(self.game.restart_game)
        self.main_menu_button = create_button(self, 'Main menu', QPoint(0, 450), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.main_menu_button.setFont(QFont(main_font))
        self.main_menu_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))


class GameOverPage(QWidget):
    def __init__(self, game, stack_widget):
        super().__init__()
        self.game = game
        self.stack_widget = stack_widget
        self.setGeometry(0, 0, Screen_Resolution[0], Screen_Resolution[1])
        self.setStyleSheet('background-color: transparent')
        self.over_txt = create_txt(
            self, 'YOU DESTROYED!', main_font,
            'rgba(200,200,200,150)', 50, QPoint(0, 45))
        self.restart_button = create_button(self, 'Restart', QPoint(0, 300), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.restart_button.setFont(QFont(main_font))
        self.restart_button.clicked.connect(self.game.restart_game)
        self.choose_button = create_button(self, 'Choose player', QPoint(0, 350), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.choose_button.setFont(QFont(main_font))
        self.choose_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))
        self.main_menu_button = create_button(self, 'Main menu', QPoint(0, 400), '''
        QPushButton {color: rgb(220,220,220); letter-spacing: 5px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        self.main_menu_button.setFont(QFont(main_font))
        self.main_menu_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))


class CardPage(QWidget):
    def __init__(self, game, stack_widget):
        super().__init__()
        self.game = game
        self.stack_widget = stack_widget
        self.setStyleSheet('background-color: transparent')
        self.setAutoFillBackground(True)
        self.setGeometry(0, 0, Screen_Resolution[0], Screen_Resolution[1])
        self.cards = []
        self.layout = QVBoxLayout(self)

    def random_cards(self):
        for card in self.cards:
            card.hide()
            self.layout.removeWidget(card)
            card.deleteLater()
        self.cards.clear()
        count = 3
        for i in range(count):
            wid = int(self.game.width() * 0.28)
            hei = int(self.game.height() * 1)
            between = 66
            end_x = (count - 1) * (wid + between) + wid
            start_x = int((self.game.width() - end_x) / 2)
            start_y = int((self.game.height() * (10 / 8) - hei) / 2)
            card = random.choice(cards_file.array_cards)
            card_widget = card(self.game, QRect((i * (wid + between) + start_x), start_y, wid, hei),
                               QFont(main_font, 32),
                               QFont(main_font, 16))
            card_widget.pixmap.load('../Game/images/card_background.png')
            card_widget.enter_pixmap_path = '../Game/images/card_background_hover.png'
            self.layout.addChildWidget(card_widget)
            card_widget.show()
            self.cards.append(card_widget)



class SceneGame(QGraphicsScene):
    def __init__(self, view):
        super().__init__()
        self.setSceneRect(0, 0, Screen_Resolution[0], (Screen_Resolution[1] * 0.8))
        self.view = view
        self.scene = self

        self.cards = []
        self.array_enemies = enemies_file.array_enemies
        self.available_enemy_types = []
        self.array_bullets = bullets_file.array_bullets
        self.array_arrays = [self.array_enemies, self.array_bullets]

        # players = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.players = [
            ('MSh-01', 5, 1, 4, 1, 370, 25, 25, f'../Game/images/default_player.png'),
            ('avf.MSh-00.03', 3, 0.5, 7, 2, 290, 20, 20, '../Game/images/pain_player.png'),
            ('P-MSh', 7, 2, 4, 2, 420, 35, 35, '../Game/images/power_player.png')
        ]
        # enemies = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.enemies = enemies_file.enemies
        self.difficult_koef = 1
        # bullets = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.bullets = bullets_file.bullets
        self.key_up_pressed = 0
        self.key_down_pressed = 0

        self.player_ch_timer = QTimer()
        self.player = self.Player()
        self.player.timer.timeout.connect(self.player.timer.stop)
        self.addItem(self.player)
        self.player.current_bullet_method = bullets_file.triple_like_method
        self.player.current_bullet_type = bullets_file.default_bullet
        self.set_player(self, self.player, self.players, 0)
        self.player.setZValue(3)

        self.check_collision_thread = self.CheckCollisionThread()
        self.check_collision_thread.request_data.connect(self.update_check_data)
        self.check_collision_thread.enemy_visible_true.connect(self.enemy_visible_true)
        self.check_collision_thread.enemy_visible_false.connect(self.enemy_visible_false)
        self.check_collision_thread.deal_damage_enemy.connect(self.deal_damage_enemy)
        self.check_collision_thread.enemy_delete.connect(self.enemy_delete)
        self.check_collision_thread.bullet_delete.connect(self.bullet_delete)
        self.check_collision_thread.change_player_speed_and_hp.connect(self.change_player_speed_and_hp)

        self.cards_timer = cards_file.timer
        self.game_timer = QTimer()
        self.game_sec_time = 0
        self.msec = 0
        self.sec = 0
        self.min = 0
        self.keys_txt = self.addText('', QFont(main_font, 20))

        self.far_star_background_list = []
        self.close_star_background_list = []
        self.super_close_star_background_list = []

        self.game_timer.timeout.connect(lambda: self.update_scene(self.player, self.array_enemies, self.array_bullets))
        self.set_game_default()

        self.interface()
        self.stop_game(True)

    @pyqtSlot()
    def start_check(self):
        if not self.check_collision_thread.isRunning():
            self.check_collision_thread.start()

    @pyqtSlot()
    def stop_check(self):
        self.check_collision_thread.stop()

    @pyqtSlot()
    def update_check_data(self):
        self.check_collision_thread.receive_data(16, self.itemsBoundingRect(), self.boundingField(), self.player,
                                                 self.array_enemies, self.array_bullets)

    @pyqtSlot(object, float)
    def deal_damage_enemy(self, enemy, damage):
        if enemy in self.array_enemies:
            enemy.hp -= damage

    @pyqtSlot(object)
    def enemy_delete(self, enemy):
        if enemy in self.array_enemies:
            enemies_file.delete_enemy(self, enemy)

    @pyqtSlot(object)
    def enemy_visible_false(self, enemy):
        for obj in self.array_enemies:
            if obj == enemy:
                obj.setVisible(False)
                break

    @pyqtSlot(object)
    def enemy_visible_true(self, enemy):
        for obj in self.array_enemies:
            if obj == enemy:
                obj.setVisible(True)
                break

    @pyqtSlot(object)
    def bullet_delete(self, bullet):
        if bullet in self.array_bullets:
            bullets_file.array_bullets.remove(bullet)
            self.removeItem(bullet)

    @pyqtSlot(float, float, float, float, int)
    def change_player_speed_and_hp(self, speed_l, speed_r, speed_u, speed_d, damage):
        self.player.hit_delay.start(500)
        self.player.hp -= damage
        self.player.speed_l = speed_l
        self.player.speed_r = speed_r
        self.player.speed_u = speed_u
        self.player.speed_d = speed_d
        if self.player.hp <= 0:
            self.stack_widget.setCurrentIndex(3)
            self.stack_proxy_widget.setVisible(True)
            self.stop_game(True)

    class CheckCollisionThread(QThread):
        request_data = pyqtSignal()
        receive_data = pyqtSlot(object)
        finished = pyqtSignal()
        deal_damage_enemy = pyqtSignal(object, float)
        enemy_delete = pyqtSignal(object)
        enemy_visible_false = pyqtSignal(object)
        enemy_visible_true = pyqtSignal(object)
        bullet_delete = pyqtSignal(object)
        change_player_speed_and_hp = pyqtSignal(float, float, float, float, int)

        def __init__(self):
            super().__init__()
            self.is_running = False
            self.speed_update = None
            self.scene_boundingRect = None
            self.scene_boundingField = None
            self.player = None
            self.array_enemies = None
            self.array_bullets = None
            self.player_damaged = 0
            self.player_speed_l = 0
            self.player_speed_r = 0

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
                        if not self.scene_boundingField.contains(enemy_rect):
                            self.enemy_delete.emit(enemy)
                            continue
                        if not self.scene_boundingRect.intersects(enemy_rect):
                            if enemy.isVisible():
                                self.enemy_visible_false.emit(enemy)
                        elif not enemy.isVisible():
                            self.enemy_visible_true.emit(enemy)
                        if self.player.collidesWithItem(enemy):
                            self.player_speed_l = 0
                            self.player_speed_r = 0
                            self.player_damaged = 0
                            if not self.player.hit_delay.isActive():
                                self.player_damaged = int(enemy.damage)
                            if player_rect.center().x() < enemy_rect.center().x():
                                self.player_speed_l = enemy.step * 3
                                if int(self.player_speed_l) > 20:
                                    self.player_speed_l = 20
                            elif player_rect.center().x() > enemy_rect.center().x():
                                self.player_speed_r = enemy.step * 3
                                if int(self.player_speed_r) > 20:
                                    self.player_speed_r = 20
                            self.change_player_speed_and_hp.emit(
                                self.player_speed_l, self.player_speed_r, 0, 0, self.player_damaged)
                        for bullet in self.array_bullets:
                            bullet_rect = QRectF(bullet.x(), bullet.y(), bullet.size_x, bullet.size_y)
                            if not self.scene_boundingRect.intersects(bullet_rect):
                                self.bullet_delete.emit(bullet)
                                continue
                            if not enemy.isVisible():
                                break
                            if enemy_rect.intersects(bullet_rect):
                                self.bullet_delete.emit(bullet)
                                damage = bullet.damage + self.player.damage
                                self.deal_damage_enemy.emit(enemy, damage)
                                if enemy.hp <= 0:
                                    self.enemy_delete.emit(enemy)
                                    break
                    self.msleep(self.speed_update)
            self.finished.emit()

        def stop(self):
            self.is_running = False
            self.wait()

        @pyqtSlot(object)
        def receive_data(self, speed_update: int, scene_boundingRect, scene_boundingField, player, array_enemies,
                         array_bullets):
            self.speed_update = speed_update
            self.scene_boundingRect = scene_boundingRect
            self.scene_boundingField = scene_boundingField
            self.player = player
            self.array_enemies = array_enemies
            self.array_bullets = array_bullets

    def set_game_default(self):
        global chosen_player
        self.game_sec_time = 0
        self.msec = 0
        self.sec = 0
        self.min = 0
        enemies_file.difficult_koef = 1
        enemies_file.update_enemies_list()
        self.available_enemy_types.clear()
        self.available_enemy_types.append(enemies_file.list_of_types[0])
        self.set_player(self, self.player, self.players, chosen_player)
        self.player.current_bullet_type = bullets_file.default_bullet
        bullets_file.bullet_count = 1
        bullets_file.bullet_degree = 30
        bullets_file.first_arg_method = bullets_file.bullet_count
        bullets_file.second_arg_mothod = bullets_file.bullet_degree
        bullets_file.scale_x_koef = 1
        bullets_file.scale_y_koef = 1
        bullets_file.damage_koef = 1
        bullets_file.speed_koef = 1
        bullets_file.speed_shoot_koef = 1
        bullets_file.update_bullets_list()
        self.keys_txt.setPlainText('W,A,S,D - movement; C - shooting; F11 - toggle full screen')
        self.player.setPos(200, 300)
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

    def stop_game(self, bol: bool):
        if bol is True:
            self.game_timer.stop()
            self.stop_check()
        else:
            self.game_timer.start(16)
            self.start_check()

    def itemsBoundingRect(self):
        return QRectF(0, 0, self.width(), self.height() * (10 / 8))

    def boundingField(self):
        return QRectF(-self.width(), -100, (self.width() + 2 * self.width()), (self.height()) + 200)

    class Player(QGraphicsRectItem):
        def __init__(self):
            super().__init__()
            self.pixmap = QPixmap()
            # self.label = QLabel()
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
            painter.drawPixmap(self.rect().toRect(),self.pixmap)

        def update_size(self, size_x, size_y):
            self.setRect(0, 0, size_x, size_y)
            # self.label.resize(size_x,size_y)
            self.size_x = size_x
            self.size_y = size_y
            self.setTransformOriginPoint(self.rect().center())

    def set_player(self, scene, obj, players: list, player_type: int):
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

        obj.pixmap = QPixmap(players[player_type][8])
        obj.update_size(obj.size_x, obj.size_y)

        def move():
            if obj.timer.isActive() is False:
                if obj.speed_l < obj.step and obj.move_direction_L == 1:
                    obj.speed_l += (sqrt(obj.speed_l) * 0.2) + 0.1
                    if obj.speed_r >= obj.speed_l:
                        obj.speed_r -= obj.speed_l

                elif obj.move_direction_L == 0 and obj.speed_l > 0:
                    obj.speed_l -= 0.1
                if obj.speed_l < 0:
                    obj.speed_l = 0

                if obj.speed_r < obj.step and obj.move_direction_R == 1:
                    obj.speed_r += (sqrt(obj.speed_r) * 0.2) + 0.1
                    if obj.speed_l >= obj.speed_r:
                        obj.speed_l -= obj.speed_r

                elif obj.move_direction_R == 0 and obj.speed_r > 0:
                    obj.speed_r -= 0.1
                if obj.speed_r < 0:
                    obj.speed_r = 0

                if obj.speed_u < obj.step and obj.move_direction_U == 1:
                    obj.speed_u += (sqrt(obj.speed_u) * 0.2) + 0.1
                    if obj.speed_d >= obj.speed_u:
                        obj.speed_d -= obj.speed_u
                elif obj.move_direction_U == 0 and obj.speed_u > 0:
                    obj.speed_u -= 0.1
                if obj.speed_u < 0:
                    obj.speed_u = 0

                if obj.speed_d < obj.step and obj.move_direction_D == 1:
                    obj.speed_d += (sqrt(obj.speed_d) * 0.2) + 0.1
                    if obj.speed_u >= obj.speed_d:
                        obj.speed_u -= obj.speed_d
                elif obj.move_direction_D == 0 and obj.speed_d > 0:
                    obj.speed_d -= 0.1
                if obj.speed_d < 0:
                    obj.speed_d = 0

                obj.timer.start(int(obj.soap_koef * 10))

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

    def player_ch_direction(self, obj, ch_direction_timer, msec, direction, future_x, arrays: list):
        if ch_direction_timer.isActive() is False:
            ch_speed = round(sqrt(int(abs(future_x - obj.x()))), 2)
            if ch_speed < 0.3:
                ch_speed = 0.3
            if direction == 0:
                obj.moveBy(ch_speed, 0)
                for array in arrays:
                    for arr_obj in array:
                        arr_obj.moveBy(ch_speed, 0)
            else:
                obj.moveBy(-ch_speed, 0)
                for array in arrays:
                    for arr_obj in array:
                        arr_obj.moveBy(-ch_speed, 0)

            ch_direction_timer.timeout.connect(ch_direction_timer.stop)
            ch_direction_timer.start(msec)

    def update_scene(self, player, array_enemies, array_bullets):
        if self.view.isActiveWindow() is False:
            self.stack_widget.setCurrentIndex(2)
            self.stack_proxy_widget.setVisible(True)
            self.stop_game(True)
        if self.cards_timer.isActive() is False:
            self.stack_widget.setCurrentIndex(4)
            self.card_menu.random_cards()
            for card in self.card_menu.cards:
                card.button.clicked.connect(lambda: self.cards_timer.start(random.randint(15000, 30000)))
            self.stop_game(True)
            self.stack_proxy_widget.setVisible(True)
            return

        self.msec += 1
        self.draw_time_timer_text()

        if player.shoot == 1:
            if bullets_file.timer.isActive() is False:
                bullet = player.current_bullet_method(self, player.current_bullet_type, bullets_file.first_arg_method,
                                                      bullets_file.second_arg_mothod)
                bullets_file.timer.start(player.speed_shoot + bullet.speed_shoot)
        for array in [array_enemies, array_bullets]:
            for arr_obj in array:
                arr_obj.moveBy(player.speed_l - player.speed_r, 0)
                arr_obj.move()
        self.infinite_background(self.far_star_background_list,player,0.1)
        self.infinite_background(self.close_star_background_list,player,0.13)
        self.infinite_background(self.super_close_star_background_list,player,0.16)
        if enemies_file.timer.isActive() is False and len(enemies_file.array_enemies) < 20:# 30
            type_enemy = random.choice(self.available_enemy_types)
            enemy = type_enemy(self)
            enemies_file.timer.start(50)
        player.move()
        left_x, right_x = 200, self.width() - player.size_x - 200
        if int(player.x()) != right_x and player.direction == 0:
            self.player_ch_direction(player, self.player_ch_timer, 0, player.direction, right_x,
                                    [array_enemies, array_bullets])
        elif int(player.x()) != left_x and player.direction == 1:
            self.player_ch_direction(player, self.player_ch_timer, 0, player.direction, left_x,
                                    [array_enemies, array_bullets])
        self.draw_player_hp(player.hp, 70, 1, self.height() + 15, 25, 50,
                            QPixmap('../Game/images/health_point.png'))
        self.update()

    def infinite_background(self,array_backgrounds,player,move_koef):
        for background in array_backgrounds:
            # background.moveBy(0.2*(player.speed_l - player.speed_r),0)
            background.moveBy(move_koef*(player.speed_l - player.speed_r),0)
            if self.itemsBoundingRect().intersects(
                    QRectF(background.x(),background.y(),
                           background.boundingRect().width(),background.boundingRect().height())) is False:
                if background.x() > 0:
                    background.setX(background.x()-(background.boundingRect().width()*2)+0.5)
                elif background.x() < 0:
                    background.setX(background.x()+(background.boundingRect().width()*2)-0.5)

    def keyPressEvent(self, event):

        if event.text() in ['Ц', 'ц', 'W', 'w']:
            self.player.move_direction_U = 1

        if event.text() in ['Ф', 'ф', 'A', 'a']:
            self.player.move_direction_L = 1
            self.player.direction = 0
            self.player.setRotation(180)

        if event.text() in ['Ы', 'ы', 'S', 's']:
            self.player.move_direction_D = 1

        if event.text() in ['В', 'в', 'D', 'd']:
            self.player.move_direction_R = 1
            self.player.direction = 1
            self.player.setRotation(0)

        if event.text() in ['C', 'c', 'С', 'с']:
            self.player.shoot = 1

        if event.key() == Qt.Key.Key_Up:
            self.key_up_pressed = 1
        if event.key() == Qt.Key.Key_Down:
            self.key_down_pressed = 1

        if event.key() == Qt.Key.Key_K:
            self.stack_widget.setCurrentIndex(4)
            self.card_menu.random_cards()
            self.stop_game(True)
            self.stack_proxy_widget.setVisible(True)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            global full_screen
            if full_screen == 1:
                full_screen = 0
            else:
                full_screen = 1
        if event.key() == Qt.Key.Key_Escape:
            full_screen = 0

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

    class HpRect(QGraphicsRectItem):
        def __init__(self,rectf):
            super().__init__()
            self.setRect(rectf)
            self.pixmap = QPixmap()

        def paint(self, painter, option, widget = ...):
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            painter.drawPixmap(self.rect().toRect(), self.pixmap)
    def draw_player_hp(self, count_hp, x, between, y, w, h, pixmap):
        if 0 < len(self.hps) > count_hp:
            last_hp = self.hps[-1]
            self.hps.remove(last_hp)
            self.removeItem(last_hp)
        elif len(self.hps) < count_hp and len(self.hps) == 0:
            hp = self.HpRect(QRectF(0, 0, w, h))
            hp.pixmap = pixmap
            self.addItem(hp)
            hp.setZValue(4)
            hp.setPos(x, y)
            hp.size_x = w
            hp.size_y = h
            self.hps.append(hp)
        elif 0 < len(self.hps) < count_hp:
            last_hp = self.hps[-1]
            hp = self.HpRect(QRectF(0, 0, w, h))
            hp.pixmap = pixmap
            self.addItem(hp)
            hp.setZValue(4)
            hp.setPos(last_hp.x() + between + w-0.1, y)
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
            self.min += 1
            self.sec = 0
        else:
            text += f'{self.sec}:'
        if self.msec < 10:
            text += f'0{self.msec}'
        elif self.msec > 99:
            self.game_sec_time += 1
            self.sec += 1
            self.msec = 0
        else:
            text += f'{self.msec}'
        self.timer_text.setPlainText(text)

    def restart_game(self):
        self.set_game_default()
        self.stack_proxy_widget.setVisible(False)
        self.cards_timer.start(random.randint(10000, 15000))

    class MenuWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.pixmap = QPixmap()

        def paintEvent(self, a0):
            painter = QPainter(self)
            painter.drawPixmap(self.rect(),self.pixmap)

    def interface(self):
        far_star_background = self.addPixmap(QPixmap('../Game/images/far_star_background.png'))
        far_star_background.setPos(0, 0)
        far_star_background2 = self.addPixmap(QPixmap('../Game/images/far_star_background.png'))
        far_star_background2.setPos(-far_star_background2.boundingRect().width(), 0)
        far_star_background3 = self.addPixmap(QPixmap('../Game/images/far_star_background.png'))
        far_star_background3.setPos(far_star_background3.boundingRect().width(), 0)
        self.far_star_background_list.append(far_star_background)
        self.far_star_background_list.append(far_star_background2)
        self.far_star_background_list.append(far_star_background3)

        close_star_background = self.addPixmap(QPixmap('../Game/images/close_star_background.png'))
        close_star_background.setPos(0, 0)
        close_star_background2 = self.addPixmap(QPixmap('../Game/images/close_star_background.png'))
        close_star_background2.setPos(-close_star_background2.boundingRect().width(), 0)
        close_star_background3 = self.addPixmap(QPixmap('../Game/images/close_star_background.png'))
        close_star_background3.setPos(close_star_background3.boundingRect().width(), 0)
        self.close_star_background_list.append(close_star_background)
        self.close_star_background_list.append(close_star_background2)
        self.close_star_background_list.append(close_star_background3)

        super_close_star_background = self.addPixmap(QPixmap('../Game/images/s_close_star_background.png'))
        super_close_star_background.setPos(0,0)
        super_close_star_background2 = self.addPixmap(QPixmap('../Game/images/s_close_star_background.png'))
        super_close_star_background2.setPos(-super_close_star_background2.boundingRect().width(),0)
        super_close_star_background3 = self.addPixmap(QPixmap('../Game/images/s_close_star_background.png'))
        super_close_star_background3.setPos(super_close_star_background3.boundingRect().width(),0)
        self.super_close_star_background_list.append(super_close_star_background)
        self.super_close_star_background_list.append(super_close_star_background2)
        self.super_close_star_background_list.append(super_close_star_background3)

        info_bar = self.addRect(QRectF(0, self.height(), self.width(), ((self.height() * (10 / 8)) - self.height())),
                                QPen(Qt.PenStyle.NoPen), QBrush(QPixmap('../Game/images/info_bar.png')))
        info_bar.setZValue(4)
        self.keys_txt.setPos(30,((self.height() * (10 / 8))-45))
        self.keys_txt.setDefaultTextColor(QColor(255,255,255,128))
        self.keys_txt.setZValue(4.1)

        # left_cover = self.addRect(self.boundingField().x(),0,abs(self.boundingField().x()-self.boundingRect().x()),self.height() * (10 / 8),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
        # left_cover.setZValue(3)
        # right_cover = self.addRect(self.width(),0,self.boundingField().width(),self.height() * (10 / 8),QPen(Qt.PenStyle.NoPen),QBrush(QColor('black')))
        # right_cover.setZValue(3)
        hp_txt = self.addText('HP',QFont(main_font,35))
        hp_txt.setPos(25,self.height()+12)
        hp_txt.setDefaultTextColor(QColor(255,100,100))
        hp_txt.setZValue(4)
        self.hps = []
        self.timer_text = self.addText('00:00:00')
        self.timer_text.setDefaultTextColor(QColor('white'))
        self.timer_text.setFont(QFont(main_font, 40))
        self.timer_text.setPos(self.width() - 200, self.height()+15)
        self.timer_text.setZValue(4)

        widget = self.MenuWidget()
        widget.pixmap.load('../Game/images/page_menu_background.png')
        widget.setStyleSheet('padding: 7px;')
        widget.setGeometry(0, 0, Screen_Resolution[0], Screen_Resolution[1])
        self.stack_widget = QStackedWidget()
        self.stack_widget.setGeometry(0, 0, Screen_Resolution[0], Screen_Resolution[1])
        self.stack_widget.setStyleSheet('background-color: transparent')
        self.stack_widget.setParent(widget)
        main_menu = MainPage(self, self.stack_widget)
        self.stack_widget.addWidget(main_menu)
        ch_player_menu = ChoosePlayerPage(self, self.stack_widget)
        ch_player_menu.next_ship()
        self.stack_widget.addWidget(ch_player_menu)
        pause_menu = PausePage(self, self.stack_widget)
        self.stack_widget.addWidget(pause_menu)
        game_over_menu = GameOverPage(self, self.stack_widget)
        self.stack_widget.addWidget(game_over_menu)
        self.card_menu = CardPage(self, self.stack_widget)
        self.stack_widget.addWidget(self.card_menu)
        self.stack_proxy_widget = self.addWidget(widget)
        self.stack_proxy_widget.setZValue(5)

        pause_button = QPushButton('Pause')
        pause_button.move(10, 10)
        pause_button.setStyleSheet('''
        QPushButton {color: white; letter-spacing: 10px;
        text-align: left; margin: 0px; background-color: rgba(255,0,0,0);
        font-size: 30px; border:none;}
        QPushButton:hover {color: rgb(219,203,180)}''')
        pause_button.setFont(QFont(main_font))
        pause_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(2))
        pause_button.clicked.connect(lambda: self.stack_proxy_widget.setVisible(True))
        pause_button.clicked.connect(lambda: self.stop_game(True))
        self.pause_button = self.addWidget(pause_button)
        self.pause_button.setZValue(4)
        self.stack_widget.installEventFilter(self)

    def eventFilter(self, watched, event):
        if watched.isVisible():
            self.pause_button.setEnabled(False)
            return True
        elif not watched.isVisible():
            self.pause_button.setEnabled(True)
            return True
        return super().eventFilter(watched, event)


class ViewMenu(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1120, 600)
        self.setMinimumSize(1120, 600)
        self.showMaximized()
        self.game = SceneGame(self)
        self.setScene(self.game)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setStyleSheet('border:none; padding:0px;')

    def closeEvent(self, a0):
        self.game.stop_game(True)
        a0.accept()

    def resizeEvent(self, event):
        self.fitInView(QRectF(0, 0, Screen_Resolution[0]-3.3, Screen_Resolution[1]-3.3),
                       Qt.AspectRatioMode.IgnoreAspectRatio)

def toggle_full_screen(obj):
    if obj.isFullScreen() is False and full_screen == 1:
        obj.showFullScreen()
    elif obj.isFullScreen() is True and full_screen == 0:
        obj.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    font_path = '../Game/fonts/Amatic_SC/AmaticSC-Bold.ttf'
    main_font = FontLoader.load_font(font_path)
    view_game = ViewMenu()
    full_screen = 0
    timer = QTimer()
    timer.timeout.connect(lambda: toggle_full_screen(view_game))
    timer.start(10)
    view_game.show()
    sys.exit(app.exec())
