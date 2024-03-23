import random
import sys
from math import ceil

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGraphicsItem, QGraphicsView, \
    QGraphicsScene, QWidget, QStackedWidget, QVBoxLayout, QGraphicsRectItem
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush, QResizeEvent, QPalette, QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt, QSize, QRectF, QPointF, QPropertyAnimation, QEasingCurve, QPoint, QEvent, \
    QVariantAnimation

class MovingObject(QGraphicsItem):
    def __init__(self,typec,modifc,x,y,hp,damage,step,speed_shoot,size_x,size_y,window_x,window_y):
        super().__init__()
        self.type_object = {
            "player": {
                0:"default",
                1:"IShowSpeed",
                2:"BurgerKing"
            },
            "enemy": {
                0:"default",
                1:"tiny",
                2:"fat"
            },
            "bullet": {
                0:"default"
            }
        }
        self.list_key_keys = list(self.type_object[typec].keys())
        self.timer = QTimer()

        self.setX(x)
        self.setY(y)
        self.hp = hp
        self.primary_damage = damage
        self.step = step
        self.soap_koef = 25
        self.primary_speed_shoot = speed_shoot
        self.main_size_x = size_x
        self.main_size_y = size_y
        self.window_x = window_x
        self.window_y = window_y

        self.draw_color = QColor(0, 0, 255)
        self.modifications(typec, modifc)

        self.move_direction_L = 0
        self.move_direction_R = 0
        self.move_direction_U = 0
        self.move_direction_D = 0
        self.shoot = 0

        self.l_speed = 0
        self.r_speed = 0
        self.u_speed = 0
        self.d_speed = 0

    def modifications(self, chosen_type, chosen_config):
        if chosen_type == "player":
            if chosen_config == "default":
                self.step_x = self.step
                self.step_y = self.step
                self.soap_koef = 25
                self.max_step_x = self.step_x
                self.max_step_y = self.step_y
                self.speed_shoot = self.primary_speed_shoot
                self.damage = self.primary_damage
                self.HP_O = self.hp
                self.primary_HP_O = self.HP_O
                self.x_size = self.main_size_x
                self.max_x_size = self.x_size
                self.y_size = self.main_size_y
                self.max_y_size = self.y_size
                self.draw_color = QColor(0,0,255)
            elif chosen_config == "IShowSpeed":
                self.step_x = self.step + 6
                self.step_y = self.step + 6
                self.soap_koef = 40
                self.max_step_x = self.step_x
                self.max_step_y = self.step_y
                self.speed_shoot = self.primary_speed_shoot - 80
                self.damage = self.primary_damage * 0.5
                self.HP_O = self.hp - 2
                self.primary_HP_O = self.HP_O
                self.x_size = self.main_size_x - 10
                self.max_x_size = self.x_size
                self.y_size = self.main_size_y - 10
                self.max_y_size = self.y_size
                self.draw_color = QColor(200,150,0)
            elif chosen_config == "BurgerKing":
                self.step_x = self.step - 3
                self.step_y = self.step - 3
                self.soap_koef = 15
                self.max_step_x = self.step_x
                self.max_step_y = self.step_y
                self.speed_shoot = self.primary_speed_shoot + 50
                self.damage = self.primary_damage + 1
                self.HP_O = self.hp + 2
                self.primary_HP_O = self.HP_O
                self.x_size = self.main_size_x + 20
                self.max_x_size = self.x_size
                self.y_size = self.main_size_y + 20
                self.max_y_size = self.y_size
                self.draw_color = QColor(100,255,255)



        elif chosen_type == "enemy":
            if chosen_config == "default":
                self.step_x = self.step
                self.step_y = self.step
                self.max_step_x = self.step_x
                self.max_step_y = self.step_y
                self.speed_shoot = self.primary_speed_shoot
                self.damage = self.primary_damage
                self.HP_O = self.hp
                self.primary_HP_O = self.HP_O
                self.x_size = self.main_size_x
                self.max_x_size = self.x_size
                self.y_size = self.main_size_y
                self.max_y_size = self.y_size
                self.draw_color = QColor(255,0,0)
            elif chosen_config == "tiny":
                self.step_x = self.step + 2
                self.step_y = self.step + 2
                self.max_step_x = self.step_x
                self.max_step_y = self.step_y
                self.speed_shoot = self.primary_speed_shoot
                self.damage = self.primary_damage
                self.HP_O = self.hp - 2
                self.primary_HP_O = self.HP_O
                self.x_size = self.main_size_x - 30
                self.max_x_size = self.x_size
                self.y_size = self.main_size_y - 30
                self.max_y_size = self.y_size
            elif chosen_config == "fat":
                self.step_x = self.step - 0.5
                self.step_y = self.step - 0.5
                self.max_step_x = self.step_x
                self.max_step_y = self.step_y
                self.speed_shoot = self.primary_speed_shoot
                self.damage = self.primary_damage
                self.HP_O = self.hp + 2
                self.primary_HP_O = self.HP_O
                self.x_size = self.main_size_x + 20
                self.max_x_size = self.x_size
                self.y_size = self.main_size_y + 20
                self.max_y_size = self.y_size



        elif chosen_type == "bullet":
            if chosen_config == "default":
                self.step_x = self.step
                self.step_y = self.step
                self.max_step_x = self.step_x
                self.max_step_y = self.step_y
                self.speed_shoot = self.primary_speed_shoot
                self.damage = self.primary_damage
                self.HP_O = self.hp
                self.primary_HP_O = self.HP_O
                self.x_size = self.main_size_x
                self.max_x_size = self.x_size
                self.y_size = self.main_size_y
                self.max_y_size = self.y_size
                self.draw_color = QColor(0,255,0)


    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option=None, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.draw_color)
        painter.drawRect(self.boundingRect())


    def new_move(self, move=1, soap_move=1, window_borders=1):
        if soap_move == 1:
            if self.timer.isActive() is False:
                if self.l_speed < self.step_x and self.move_direction_L == 1:
                    self.l_speed += 1
                elif self.move_direction_L == 0 and self.l_speed > 0:
                    self.l_speed -= 1
                elif self.l_speed < 0:
                    self.l_speed = 0

                if self.r_speed < self.step_x and self.move_direction_R == 1:
                    self.r_speed += 1
                elif self.move_direction_R == 0 and self.r_speed > 0:
                    self.r_speed -= 1
                elif self.r_speed < 0:
                    self.r_speed = 0

                if self.u_speed < self.step_y and self.move_direction_U == 1:
                    self.u_speed += 1
                elif self.move_direction_U == 0 and self.u_speed > 0:
                    self.u_speed -= 1
                elif self.u_speed < 0:
                    self.u_speed = 0

                if self.d_speed < self.step_y and self.move_direction_D == 1:
                    self.d_speed += 1
                elif self.move_direction_D == 0 and self.d_speed > 0:
                    self.d_speed -= 1
                elif self.d_speed < 0:
                    self.d_speed = 0

                self.timer.timeout.connect(self.timer.stop)
                self.timer.start(self.soap_koef)
        else:
            if self.l_speed < self.step_x and self.move_direction_L == 1:
                self.l_speed = self.step_x
            elif self.move_direction_L == 0 and self.l_speed > 0:
                self.l_speed = 0

            if self.r_speed < self.step_x and self.move_direction_R == 1:
                self.r_speed = self.step_x
            elif self.move_direction_R == 0 and self.r_speed > 0:
                self.r_speed = 0

            if self.u_speed < self.step_y and self.move_direction_U == 1:
                self.u_speed = self.step_y
            elif self.move_direction_U == 0 and self.u_speed > 0:
                self.u_speed = 0

            if self.d_speed < self.step_y and self.move_direction_D == 1:
                self.d_speed = self.step_y
            elif self.move_direction_D == 0 and self.d_speed > 0:
                self.d_speed = 0

        if move == 0:
            self.move_direction_L = 0
            self.move_direction_R = 0
            self.move_direction_U = 0
            self.move_direction_D = 0
            self.shoot = 0
            self.l_speed = 0
            self.r_speed = 0
            self.u_speed = 0
            self.d_speed = 0

        if window_borders == 1:
            if self.x() - self.l_speed < 0:
                self.setX(0)
            else:
                self.setX(self.x() - self.l_speed)

            if self.x() + self.r_speed > self.window_x - self.x_size:
                self.setX(self.window_x - self.x_size)
            else:
                self.setX(self.x() + self.r_speed)

            if self.y() - self.u_speed < 0:
                self.setY(0)
            else:
                self.setY(self.y() - self.u_speed)

            if self.y() + self.d_speed > self.window_y - self.y_size:
                self.setY(self.window_y - self.y_size)
            else:
                self.setY(self.y() + self.d_speed)
        else:
            self.setX(self.x() - self.l_speed + self.r_speed)
            self.setY(self.y() - self.u_speed + self.d_speed)

    def keyPressEvent(self, event):
            if event.text() in ['Ц', 'ц', 'W', 'w']:
                self.move_direction_U = 1

            elif event.text() in ['Ф', 'ф', 'A', 'a']:
                self.move_direction_L = 1

            elif event.text() in ['Ы', 'ы', 'S', 's']:
                self.move_direction_D = 1

            elif event.text() in ['В', 'в', 'D', 'd']:
                self.move_direction_R = 1

            if event.text() in ['C', 'c', 'С', 'с']:
                self.shoot = 1

    def keyReleaseEvent(self, event):
            if event.text() in ['Ц', 'ц', 'W', 'w']:
                self.move_direction_U = 0

            elif event.text() in ['Ф', 'ф', 'A', 'a']:
                self.move_direction_L = 0

            elif event.text() in ['Ы', 'ы', 'S', 's']:
                self.move_direction_D = 0

            elif event.text() in ['В', 'в', 'D', 'd']:
                self.move_direction_R = 0

            if event.text() in ['C', 'c', 'С', 'с']:
                self.shoot = 0



class Card(QPushButton):
    def __init__(self):
        super().__init__()
        self.modifications()
        self.setGeometry(0, 0, self.x_size, self.y_size)
        self.txt_chosen_object_1, self.txt_effect_1, self.chosen_object_1, self.effect_1 = self.random_effect()
        self.effect_power_1 = random.randint(0, 6)
        self.setText(f"{self.txt_chosen_object_1} {self.txt_effect_1} + {self.effect_power_1}%")
        self.setStyleSheet("text-align: top"
                           "")
        self.clicked.connect(self.close)

    def modifications(self, x_size=200, y_size=500):
        self.x_size = x_size
        self.y_size = y_size
        self.max_x_size = x_size
        self.max_y_size = y_size

    def random_effect(self):
        robject = {
            "Player": "player1",
            "Enemies": "enemy",
            "Bullets": "bullet"
        }
        chobject = random.choice(list(robject.keys()))
        if chobject == "Player":
            effects = {
                "Speed": "step",
                "Speed shoot": "speed_shoot",
                "Hp": "HP_O",
                "Size": "x_size",
                "Damage": "damage",
                "Soap Coefficient":"soap_koef"
            }
        else:
            effects = {
                "Speed": "step",
                "Speed shoot": "speed_shoot",
                "Hp": "HP_O",
                "Size": "x_size",
                "Damage": "damage",
            }
        effect = random.choice(list(effects.keys()))
        return chobject, effect, robject[chobject], effects[effect]





class Func_Chest(QWidget):
    def __init__(self, player, enemy, resize_window, menu):
        super().__init__()
        self.resize_window = resize_window
        self.menu = menu
        self.player = player
        self.enemy = enemy
        self.x_size = 40
        self.y_size = 40
        self.type_cards_1 = ''
        self.effect_card_1 = ''
        self.value_card_1 = 0
        self.type_cards_2 = ''
        self.effect_card_2 = ''
        self.value_card_2 = 0
        self.type_cards_3 = ''
        self.effect_card_3 = ''
        self.value_card_3 = 0

        self.button_one = QPushButton(f'{self.effect_card_1}', self)
        self.button_one.clicked.connect(self.first_button)

        self.button_two = QPushButton(f'{self.effect_card_2}', self)
        self.button_two.move(0,50)
        self.button_two.clicked.connect(self.second_button)

        self.button_three = QPushButton(f'{self.effect_card_3}', self)
        self.button_three.move(0,100)
        self.button_three.clicked.connect(self.third_button)

    def open(self):
        self.storage()
        for i in range(3):
            random_type_cards = random.choice(list(self.cards))
            random_effect = random.choice(list(self.cards[random_type_cards]))
            effect_value = self.cards[random_type_cards][random_effect]
            if i == 0:
                self.type_cards_1 = random_type_cards
                self.effect_card_1 = random_effect
                self.value_card_1 = effect_value
            elif i == 1:
                self.type_cards_2 = random_type_cards
                self.effect_card_2 = random_effect
                self.value_card_2 = effect_value
            elif i == 2:
                self.type_cards_3 = random_type_cards
                self.effect_card_3 = random_effect
                self.value_card_3 = effect_value
        self.button_one.setText(f'{self.effect_card_1}')
        self.button_two.setText(f'{self.effect_card_2}')
        self.button_three.setText(f'{self.effect_card_3}')


    def storage(self):
        self.cards = {
            "speed_cards": {
                "Slow_down": 0.9,
                "Speed_Up": 1.1,
                "Very_slow": 0.5
            },
            "hp_cards": {
                "Fat_player": 2,
                "Tiny_player": -2
            }
        }

    def use_card(self, cards: dict, type_card: str, effect: str):
        if type_card == 'speed_cards':
            self.player.max_step *= cards[type_card][effect]
        elif type_card == 'hp_cards':
            self.player.HP_P += cards[type_card][effect]
        self.resize_window.resizeEvent(None)
        self.menu.stackWidget.setCurrentWidget(self.menu.start_game)

    def first_button(self):
        self.use_card(self.cards, self.type_cards_1, self.effect_card_1)


    def second_button(self):
        self.use_card(self.cards, self.type_cards_2, self.effect_card_2)
        self.close()

    def third_button(self):
        self.use_card(self.cards, self.type_cards_3, self.effect_card_3)
        self.close()

    def enemy_open(self):
        self.enemy_storage()
        random_type_cards = random.choice(list(self.enemy_cards))
        random_effect = random.choice(list(self.enemy_cards[random_type_cards]))
        effect_value = self.enemy_cards[random_type_cards][random_effect]
        if random_type_cards == 'speed_cards':
            self.enemy.max_step_x *= self.enemy_cards[random_type_cards][random_effect]
        elif random_type_cards == 'hp_cards':
            self.enemy.HP_E += self.enemy_cards[random_type_cards][random_effect]
        self.resize_window.resizeEvent(None)

    def enemy_storage(self):
        self.enemy_cards = {
            "speed_cards": {
                "Speed_Up": 1.1,
                "Very_Speed_Up": 1.5
            },
            "hp_cards": {
                "Fat_enemy": 1,
            }
        }

    def paintEvent(self, event):
        painter = QPainter(self)
        self.menu.start_game.paint(painter)
        painter.fillRect(0,0,self.width(),self.height(),QColor(0,0,0,200))




def create_page(this_page, addwidgets: list):
    page = QVBoxLayout(this_page)
    for i in range(len(addwidgets)):
        page.addChildWidget(addwidgets[i])
    return page


def create_txt(name: str, style: str, geometry: list):
    txt = QLabel()
    txt.setText(name)
    txt.setStyleSheet(style)
    txt.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
    return txt

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stackWidget = QStackedWidget()
        self.setCentralWidget(self.stackWidget)
        self.setMinimumSize(1120,600)
        self.setGeometry(0,0,700,375)
        self.font = QFont()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_bg)
        self.timer.start(14)
        self.star_timer = QTimer()
        self.puls_timer = QTimer()
        self.switch = 0
        self.a = 16
        self.previous_size = QSize()
        self.stars = []

        # Main menu 0
        self.main_menu_page = QWidget()
        self.Main_Title_txt = create_txt('STAR DEFENDER', '',
                                    [0, 0, 370, 50])
        self.start_button = QPushButton('Start')
        self.start_button.setGeometry(self.width()//2, self.height()-200, 200, 40)
        self.start_button.clicked.connect(lambda: self.stackWidget.setCurrentWidget(self.choose_menu_page))
        self.exit_button = QPushButton('Exit')
        self.exit_button.setGeometry(100 // 3, (100 // 3) + 100, 80, 30)
        self.exit_button.clicked.connect(self.close)
        create_page(self.main_menu_page, [self.Main_Title_txt, self.start_button, self.exit_button])
        self.stackWidget.addWidget(self.main_menu_page)

        # Choose mode 1
        self.choose_menu_page = QWidget()
        self.choose_mode_txt = create_txt('CHOOSE MODE', '',
                                     [100 // 4, 0, 100 // 2, 100])
        self.start_1p_button = QPushButton('Solo')
        self.start_1p_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.start_1p_button.clicked.connect(lambda: self.stackWidget.setCurrentWidget(self.choose_player_page))
        self.start_2p_button = QPushButton('2Players')
        self.start_2p_button.setGeometry(100 // 3, (100 // 3) + 100, 80, 30)
        self.choose_mode_back_button = QPushButton('Main menu')
        self.choose_mode_back_button.clicked.connect(lambda: self.stackWidget.setCurrentWidget(self.main_menu_page))
        self.choose_mode_back_button.setGeometry(100 // 3, (100 // 3) + 200, 80, 30)
        create_page(self.choose_menu_page, [self.choose_mode_txt, self.start_1p_button,
                                       self.start_2p_button, self.choose_mode_back_button])
        self.stackWidget.addWidget(self.choose_menu_page)

        # Choose player mode 2
        self.choose_player_page = QWidget()
        self.choose_player_txt = create_txt('CHOOSE PLAYER', '',
                                       [100 // 4, 0, 100 // 2, 100])
        self.current_player_txt = create_txt('About player', 'color: green;', [500, 300, 150, 100])
        self.current_player_txt.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.start_1mode_button = QPushButton('back')
        self.start_1mode_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.chosen_config = 0
        self.start_1mode_button.clicked.connect(self.onemode)
        self.start_2mode_button = QPushButton('next')
        self.start_2mode_button.clicked.connect(self.twomode)
        self.start_2mode_button.setGeometry(100 // 3, (100 // 3) + 100, 80, 30)
        self.confirm_button = QPushButton('Play')
        self.confirm_button.clicked.connect(self.restart_game)
        self.confirm_button.setGeometry(100 // 3, (100 // 3) + 300, 80, 30)
        self.choose_player_back_button = QPushButton('Go to mode')
        self.choose_player_back_button.clicked.connect(lambda: self.stackWidget.setCurrentWidget(self.choose_menu_page))
        self.choose_player_back_button.setGeometry(100 // 3, (100 // 3) + 200, 80, 30)
        create_page(self.choose_player_page,
                    [self.choose_player_txt, self.current_player_txt, self.start_1mode_button, self.start_2mode_button,
                     self.confirm_button, self.choose_player_back_button])

        self.stackWidget.addWidget(self.choose_player_page)

        # Game over 3
        self.game_over_page = QWidget()
        self.game_over_txt = create_txt('YOU DESTROYED !', '',
                                   [0, 0, 100, 100])
        self.retry_button = QPushButton('Retry', self)
        self.retry_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.retry_button.clicked.connect(self.restart_game)
        self.game_over_main_menu_button = QPushButton('Main menu')
        self.game_over_main_menu_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.game_over_main_menu_button.clicked.connect(lambda: self.stackWidget.setCurrentWidget(self.main_menu_page))
        self.game_over_choose_player_button = QPushButton('Choose player')
        self.game_over_choose_player_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.game_over_choose_player_button.clicked.connect(lambda: self.stackWidget.setCurrentWidget(self.choose_player_page))
        create_page(self.game_over_page, [self.game_over_txt, self.retry_button, self.game_over_choose_player_button,
                                          self.game_over_main_menu_button])
        self.stackWidget.addWidget(self.game_over_page)

        # Pause 4
        self.pause_page = QWidget()
        self.pause_game_txt = create_txt('PAUSE', '', [0, 0, 100, 100])
        self.resume_button = QPushButton('Resume', self)
        self.resume_button.clicked.connect(self.resume_game)
        self.resume_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.pause_game_main_menu_button = self.main_menu_button()
        self.pause_game_main_menu_button.setGeometry(100 // 3, (100 // 3)+100, 80, 30)
        self.pause_game_retry_button = QPushButton('Restart')
        self.pause_game_retry_button.clicked.connect(lambda: self.stackWidget.setCurrentWidget(self.choose_player_page))
        self.pause_game_retry_button.setGeometry(100 // 3, (100 // 3)+200, 80, 30)
        create_page(self.pause_page, [self.pause_game_txt, self.resume_button, self.pause_game_retry_button,
                                      self.pause_game_main_menu_button])
        self.stackWidget.addWidget(self.pause_page)


        # Game page 5
        self.start_game = StartGame(self,True)
        self.stackWidget.addWidget(self.start_game)
        self.twomode() # для того чтобы 1 перс был сначала

        # choose effect page 6
        self.choose_card_page = QWidget()
        self.card_button = Card()
        obj_1 = getattr(self.start_game, self.card_button.chosen_object_1)
        # setattr(obj_1, f"{self.card_button.effect_1}",getattr(obj_1, f"{self.card_button.effect_1}")*(self.card_button.effect_power_1/100))
        self.card_button.clicked.connect(lambda: (self.stackWidget.setCurrentWidget(self.start_game), setattr(obj_1, f"{self.card_button.effect_1}",
                                                 ceil(getattr(obj_1, self.card_button.effect_1) *
                                                 (self.card_button.effect_power_1/100)))))
        # self.card_button.clicked.connect(lambda: setattr(obj_1, f"{self.card_button.effect_1}",
        #                                          getattr(obj_1, self.card_button.effect_1) *
        #                                          (self.card_button.effect_power_1/100)))

        create_page(self.choose_card_page, [self.card_button])
        self.stackWidget.addWidget(self.choose_card_page)
        # Включить полноэкранный режим
        self.showMaximized()

    def resizeEvent(self, event):
        pass
        if self.stackWidget.currentWidget() != self.start_game and self.stackWidget.currentWidget() != self.choose_card_page:

            if self.stackWidget.currentWidget() != self.pause_page:
                self.start_game.player1.window_x = self.width()
                self.start_game.player1.window_y = self.height()
                self.start_game.player1.setX(self.width() * 0.6)
                self.start_game.player1.setY(self.height() * 0.1)
                self.start_game.player1.x_size = (self.width() * 0.13)
                self.start_game.player1.y_size = (self.width() * 0.13)

            previous_width = 1536
            previous_height = 793
            if self.previous_size.isValid():
                previous_width = self.previous_size.width()
                previous_height = self.previous_size.height()

            self.fullW = 1536
            self.fullH = 793
            if self.isMaximized() is True:
                self.fullW = self.width()
                self.fullH = self.height()
            for star in self.stars:
                pro_x_star_speed = star.max_step_x / self.fullW
                star.step_x = round(self.width() * pro_x_star_speed, 1)
                pro_x_star_position = star.x() / previous_width
                pro_y_star_position = star.y() / previous_height
                star.setX(round(self.width() * pro_x_star_position, 1))
                star.setY(round(self.height() * pro_y_star_position, 1))

            self.previous_size = self.size()

    # Main menu
            self.Main_Title_txt.setGeometry(0, ceil(self.height()*0.1), self.width(), 150)
            self.Main_Title_txt.setStyleSheet("font-family: Courier, monospace; color: rgba(200,200,200,50); letter-spacing: 15px;")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2)*0.08))
            self.Main_Title_txt.setFont(self.font)
            self.start_button.setGeometry(0, ceil(self.height()*0.7),ceil(self.width()*0.2), ceil(self.width()*0.03))
            self.start_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2)*0.02))
            self.start_button.setFont(self.font)
            self.exit_button.setGeometry(0, ceil(self.height()*0.79), ceil(self.width()*0.2), ceil(self.width()*0.03))
            self.exit_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(0,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.exit_button.setFont(self.font)

    # Choose mode
            self.choose_mode_txt.setGeometry(0, ceil(self.height() * 0.11), self.width(), 100)
            self.choose_mode_txt.setStyleSheet("font-family: Courier, monospace; color: rgb(200,200,200)")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.03))
            self.choose_mode_txt.setFont(self.font)
            self.start_1p_button.setGeometry(0, ceil(self.height() * 0.3), ceil(self.width() * 0.2), ceil(self.width() * 0.03))
            self.start_1p_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.start_1p_button.setFont(self.font)
            self.start_2p_button.setGeometry(0, ceil(self.height() * 0.39), ceil(self.width() * 0.2),
                                             ceil(self.width() * 0.03))
            self.start_2p_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.start_2p_button.setFont(self.font)
            self.choose_mode_back_button.setGeometry(0, ceil(self.height() * 0.48), ceil(self.width() * 0.25),
                                             ceil(self.width() * 0.03))
            self.choose_mode_back_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; word-spacing: -7px; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.choose_mode_back_button.setFont(self.font)

    # choose player
            self.choose_player_txt.setGeometry(0, ceil(self.height() * 0.12), self.width(), 100)
            self.choose_player_txt.setStyleSheet("font-family: Courier, monospace; color: rgb(200,200,200)")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.03))
            self.choose_player_txt.setFont(self.font)
            self.current_player_txt.setGeometry(ceil(self.width()*0.5), ceil(self.height() * 0.45), self.width(), self.height()-self.y())
            self.current_player_txt.setStyleSheet("font-family: Courier New, monospace; color: rgb(200,200,200)")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.023))
            self.current_player_txt.setFont(self.font)
            self.start_1mode_button.setGeometry(ceil(self.width()*0.75), ceil(self.height() * 0.1), ceil(self.width() * 0.1), ceil(self.width() * 0.03))
            self.start_1mode_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.start_1mode_button.setFont(self.font)
            self.start_2mode_button.setGeometry(ceil(self.width()*0.87), ceil(self.height() * 0.1), ceil(self.width() * 0.1),
                                                ceil(self.width() * 0.03))
            self.start_2mode_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.start_2mode_button.setFont(self.font)
            self.confirm_button.setGeometry(ceil(self.width()*0.75), ceil(self.height() * 0.29), ceil(self.width() * 0.2), ceil(self.width() * 0.03))
            self.confirm_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.confirm_button.setFont(self.font)
            self.choose_player_back_button.setGeometry(0, ceil(self.height() * 0.48), ceil(self.width() * 0.25), ceil(self.width() * 0.03))
            self.choose_player_back_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; word-spacing: -20px; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.choose_player_back_button.setFont(self.font)

    # game over
            self.game_over_txt.setGeometry(0, ceil(self.height() * 0.1), self.width(), 100)
            self.game_over_txt.setStyleSheet("font-family: Courier, monospace; color: Crimson")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.07))
            self.game_over_txt.setFont(self.font)
            self.retry_button.setGeometry(0, ceil(self.height() * 0.3), ceil(self.width() * 0.2),
                                             ceil(self.width() * 0.03))
            self.retry_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.retry_button.setFont(self.font)
            self.game_over_choose_player_button.setGeometry(0, ceil(self.height() * 0.39), ceil(self.width() * 0.35),
                                          ceil(self.width() * 0.03))
            self.game_over_choose_player_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; word-spacing: -7px; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.game_over_choose_player_button.setFont(self.font)
            self.game_over_main_menu_button.setGeometry(0, ceil(self.height() * 0.48), ceil(self.width() * 0.25),
                                                            ceil(self.width() * 0.03))
            self.game_over_main_menu_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; word-spacing: -7px; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.game_over_main_menu_button.setFont(self.font)

    # pause game
            self.pause_game_txt.setGeometry(0, ceil(self.height() * 0.1), self.width(), 100)
            self.pause_game_txt.setStyleSheet("font-family: Courier, monospace; color: rgb(200,200,200)")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.03))
            self.pause_game_txt.setFont(self.font)
            self.resume_button.setGeometry(0, ceil(self.height() * 0.3), ceil(self.width() * 0.2),
                                          ceil(self.width() * 0.03))
            self.resume_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.resume_button.setFont(self.font)
            self.pause_game_retry_button.setGeometry(0, ceil(self.height() * 0.39), ceil(self.width() * 0.2),
                                           ceil(self.width() * 0.03))
            self.pause_game_retry_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.pause_game_retry_button.setFont(self.font)
            self.pause_game_main_menu_button.setGeometry(0, ceil(self.height() * 0.48), ceil(self.width() * 0.25),
                                                     ceil(self.width() * 0.03))
            self.pause_game_main_menu_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(((self.width()+(self.height()*1.78))/2) * 0.02))
            self.pause_game_main_menu_button.setFont(self.font)






    def create_star(self, msec):
        if self.star_timer.isActive() is False and len(self.stars) < 100:
            rand_y = random.randint(0, self.height() - 10)
            rand_step = random.randint(1, 8)
            x_size = random.randint(1, 5)
            y_size = x_size
            a = 255
            r = random.randint(219, 255)
            g = random.randint(203, 244)
            b = random.randint(190, 221)
            star = MovingObject("enemy", "default", self.width(), rand_y, 0, 0, rand_step, 0,
                                     x_size, y_size, self.width(), self.height())
            star.draw_color = QColor(a, r, g, b)
            self.stars.append(star)
            self.star_timer.start(msec)
            self.star_timer.timeout.connect(self.star_timer.stop)

    def reborn_star(self, star):
        star.x_size = random.randint(1, 4)
        star.y_size = star.x_size
        star.setX(self.width()+star.x_size)
        rand_y = random.randint(0, self.height() - 10)
        star.setY(rand_y)
        a = 255
        r = random.randint(219, 255)
        g = random.randint(203, 244)
        b = random.randint(190, 221)
        star.draw_color = QColor(a, r, g, b)
    def update_bg(self):
        if self.stackWidget.currentWidget() != self.start_game:
            randomint = random.randint(0,101)
            if randomint <= 4:
                self.create_star(1)
            for star in self.stars:
                star.move_direction_L = 1
                star.new_move(1, 0, 0)
                if star.x() <= -star.x_size:
                    self.reborn_star(star)
            self.update()

    def main_menu_button(self):
        main_menu_button = QPushButton('Main menu', self)
        main_menu_button.setGeometry(100 // 3, (100 // 3) + 200, 80, 30)
        main_menu_button.clicked.connect(lambda: self.stackWidget.setCurrentWidget(self.main_menu_page))
        return main_menu_button


    def restart_game(self):
        self.stackWidget.setCurrentWidget(self.start_game)
        self.start_game.game_restart(0)

    def onemode(self):
        self.chosen_config -= 1
        maxx = self.start_game.player1.list_key_keys[-1]
        if self.chosen_config < 0:
            self.chosen_config = self.start_game.player1.list_key_keys[-1]
        elif self.chosen_config > maxx:
            self.chosen_config = 0
        self.start_game.player1.modifications("player",
                                              self.start_game.player1.type_object["player"][self.chosen_config])
        self.current_player_txt.setText(f"Name: {self.start_game.player1.type_object["player"][self.chosen_config]} \n"
                                        f"Health: {self.start_game.player1.primary_HP_O} \n"
                                        f"Speed: {self.start_game.player1.max_step_x} \n"
                                        f"Soap move: {self.start_game.player1.soap_koef} \n"
                                        f"Damage: {self.start_game.player1.damage} \n"
                                        f"Speed shoot: {self.start_game.player1.speed_shoot} \n"
                                        f"Size: {self.start_game.player1.max_x_size}")


    def twomode(self):
        self.chosen_config += 1
        maxx = self.start_game.player1.list_key_keys[-1]
        if self.chosen_config < 0:
            self.chosen_config = self.start_game.player1.list_key_keys[-1]
        elif self.chosen_config > maxx:
            self.chosen_config = 0
        self.start_game.player1.modifications("player",
                                              self.start_game.player1.type_object["player"][self.chosen_config])
        self.current_player_txt.setText(f"Name: {self.start_game.player1.type_object["player"][self.chosen_config]} \n"
                                        f"Health: {self.start_game.player1.primary_HP_O} \n"
                                        f"Speed: {self.start_game.player1.max_step_x} \n"
                                        f"Soap move: {self.start_game.player1.soap_koef} \n"
                                        f"Damage: {self.start_game.player1.damage} \n"
                                        f"Speed shoot: {self.start_game.player1.speed_shoot} \n"
                                        f"Size: {self.start_game.player1.max_x_size}")

    def resume_game(self):
        self.stackWidget.setCurrentWidget(self.start_game)
        self.start_game.resizeEvent(None)
        self.start_game.count_restart_sec = 4

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(0,0,self.width(),self.height(),QColor('black'))
        for star in self.stars:
            star.paint(painter)
        if self.stackWidget.currentWidget() == self.choose_player_page:
            if self.start_game.player1.x() != (self.width() * 0.6):
                self.start_game.player1.setX((self.width() * 0.6))
            if self.start_game.player1.y() != (self.width() * 0.1):
                self.start_game.player1.setY((self.height() * 0.1))
            if self.start_game.player1.x_size != self.width() * 0.13:
                self.start_game.player1.x_size = (self.width() * 0.13)
                self.start_game.player1.y_size = (self.width() * 0.13)
            # позиция не та
            self.start_game.player1.paint(painter)
























class StartGame(QWidget):
    def __init__(self, menu, game_begin=False):
        super().__init__()
        self.game_begin = game_begin
        self.menu = menu

        self.previous_size = QSize()

        self.count_restart_sec = 3

        self.mode = 0



        self.sec = -1
        self.min = 0

        self.font = QFont()
        self.score_label = QLabel(self)
        self.score_label.setText('00:00')
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.score_label.setStyleSheet("color: white;")
        self.Player1_HP = QLabel(self)
        self.Player1_HP.setText("HP")
        self.Player1_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player1_HP.setStyleSheet("color: rgb(255,155,155);")

        self.restart_timer_txt = QLabel(self)
        self.restart_timer_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)



        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScene)
        self.timer.start(16)
        self.enemy_timer = QTimer(self)
        self.bullet_timer1 = QTimer(self)

        self.timer_time = QTimer()
        self.timer_time.timeout.connect(self.update_score)
        self.timer_time.start(1000)

        self.restart_timer = QTimer()
        self.restart_timer.timeout.connect(self.restart_timer.stop)

        self.bullet = MovingObject("bullet", "default", 0, 0, 1, 1, 15,
                                   0, 20, 5, self.width(), self.height())  # этот предатель существует, но не виден глазу

        self.enemy = MovingObject("enemy", "default", 0, 0, 3, 1, 1,
                                  0, 65, 65, self.width(), self.height())  # этот предатель существует, но не виден глазу
        # думаю, что вполне возможно исп только один

        self.player1 = MovingObject("player", "default", 0, 0, 3, 1, 10, 370,
                                    45, 45, self.width(), self.height())

        self.game_restart(0)

    def boundingRect(self):
        return QRectF(-100, -100, (self.width()+200), (self.height()+200))

    def game_restart(self, mode_player):
        self.count_restart_sec = 1
        self.mode = mode_player

        self.previous_size = QSize()

        self.sec = -1
        self.min = 0
        self.score_label.setText('00:00')

        self.player1.HP_O = self.player1.primary_HP_O
        self.player1.setPos(10,300)
        self.bullets = []
        self.enemies = []
        self.enemy_deserters = []

        self.resizeEvent(None)
        self.showMaximized()

    def resizeEvent(self, event):
        if self.menu.stackWidget.currentWidget() == self:
            print(self.size())
            self.fullW = 1536
            self.fullH = 793
            if self.isMaximized() is True:
                self.fullW = self.width()
                self.fullH = self.height()


            previous_width = 1536
            previous_height = 793
            current_size = self.size()
            if self.previous_size.isValid():
                previous_width = self.previous_size.width()
                previous_height = self.previous_size.height()

            self.score_label.setGeometry(ceil(self.width() * 0.85), ceil(self.height() * 0.81),
                                         ceil(self.width() * 0.14), 50)
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.score_label.setFont(self.font)

            self.Player1_HP.setGeometry(ceil(self.width() * 0.01), ceil(self.height() * 0.81), ceil(self.width() * 0.04),
                                        100)
            self.Player1_HP.setFont(self.font)

            pro_x_player_size = self.player1.max_x_size / self.fullW
            pro_y_player_size = self.player1.max_y_size / self.fullH
            self.player1.x_size = int(self.width() * pro_x_player_size)
            self.player1.y_size = int(self.height() * pro_y_player_size)
            self.player1.window_x = (self.width())
            self.player1.window_y = (self.height() * 0.8)
            pro_x_player_position = self.player1.x() / previous_width
            pro_y_player_position = self.player1.y() / previous_height
            pro_x_player_speed = self.player1.max_step_x / self.fullW
            pro_y_player_speed = self.player1.max_step_y / self.fullH
            self.player1.setX(round(self.width() * pro_x_player_position, 1))
            self.player1.setY(round(self.height() * pro_y_player_position, 1))
            self.player1.step_x = round(self.width() * pro_x_player_speed, 1)
            self.player1.step_y = round(self.height() * pro_y_player_speed, 1)
            # сохранение позиции player1 при изменении экрана
            # (в процентном соотношении с округлением до 1 десятой)

            pro_x_enemy_size = self.enemy.max_x_size / self.fullW
            pro_y_enemy_size = self.enemy.max_y_size / self.fullH
            self.enemy.x_size = int(self.width() * pro_x_enemy_size)
            self.enemy.y_size = int(self.height() * pro_y_enemy_size)
            pro_x_enemy_speed = self.enemy.max_step_x / self.fullW
            self.enemy.step_x = round(self.width() * pro_x_enemy_speed, 1)
            pro_y_enemy_speed = self.enemy.max_step_y / self.fullH
            self.enemy.step_y = round(self.width() * pro_x_enemy_speed, 1)
            self.enemy.window_x = self.width()
            self.enemy.window_y = self.height()
            for enemy in self.enemies:
                enemy.x_size = int(self.width() * pro_x_enemy_size)
                enemy.y_size = int(self.height() * pro_y_enemy_size)
                pro_x_bullet_position = enemy.x() / previous_width
                pro_y_bullet_position = enemy.y() / previous_height
                enemy.setX(round(self.width() * pro_x_bullet_position, 1))
                enemy.setY(round(self.height() * pro_y_bullet_position, 1))
                enemy.step_x = round(self.width() * pro_x_enemy_speed, 1)
                enemy.step_y = round(self.width() * pro_y_enemy_speed, 1)


            pro_x_bullet_size = self.bullet.max_x_size / self.fullW
            pro_y_bullet_size = self.bullet.max_y_size / self.fullH
            self.bullet.x_size = int(self.width() * pro_x_bullet_size)
            self.bullet.y_size = int(self.height() * pro_y_bullet_size)
            # self.bullet.width_window = self.fullW
            # self.bullet.height_window = self.fullH
            pro_x_bullet_speed = self.bullet.max_step_x / self.fullW
            pro_y_bullet_speed = self.bullet.max_step_y / self.fullW
            self.bullet.step_x = round(self.width() * pro_x_bullet_speed, 1)
            self.bullet.step_y = round(self.width() * pro_y_bullet_speed, 1)
            for bullet in self.bullets:
                bullet.x_size = int(self.width() * pro_x_bullet_size)
                bullet.y_size = int(self.height() * pro_y_bullet_size)
                pro_x_bullet_position = bullet.x() / previous_width
                pro_y_bullet_position = bullet.y() / previous_height
                bullet.setX(round(self.width() * pro_x_bullet_position, 1))
                bullet.setY(round(self.height() * pro_y_bullet_position, 1))
                bullet.step_x = round(self.width() * pro_x_bullet_speed, 1)
                bullet.step_y = round(self.width() * pro_y_bullet_speed, 1)
            self.previous_size = current_size
            self.paintEvent(event)

            self.restart_timer_txt.setGeometry(0, ceil(self.height() * 0.1), self.width(), 150)
            self.restart_timer_txt.setStyleSheet("font-family: Courier, monospace; color: rgb(200,200,200)")
            self.font.setPointSize(ceil(self.width() * 0.1))
            self.restart_timer_txt.setFont(self.font)

    def update_score(self):
        if self.menu.stackWidget.currentWidget() == self and self.count_restart_sec >= 1 and self.restart_timer.isActive() is False:
            self.sec += 1
            if self.sec > 59:
                self.min += 1
                self.sec = 0
            if self.sec < 10 and self.min < 10:
                self.score_label.setText(f"0{self.min}:0{self.sec}")
            elif self.min < 10:
                self.score_label.setText(f"0{self.min}:{self.sec}")
            elif self.sec < 10:
                self.score_label.setText(f"{self.min}:0{self.sec}")
            else:
                self.score_label.setText(f"{self.min}:{self.sec}")

    def create_enemy(self, msec, shoot_msec):
        if self.enemy_timer.isActive() is False:
            y_size = self.enemy.y_size
            enemy_y = random.randint(0, int(self.height() * 0.8) - y_size)
            enemy = MovingObject("enemy","default",self.width(),enemy_y,self.enemy.hp,self.enemy.damage,
                                 self.enemy.step,self.enemy.speed_shoot,self.enemy.x_size,self.enemy.y_size,
                                 self.width(),self.height())
            if enemy.y()+enemy.y_size > int(self.height()*0.8):
                enemy.setY(int(self.height()*0.8)-enemy.y())
            self.enemies.append(enemy)
            self.enemy_timer.start(msec)
            self.enemy_timer.timeout.connect(self.enemy_timer.stop)

    def create_bullet(self, msec1):
        if self.player1.shoot == 1 and self.bullet_timer1.isActive() is False:
            bullet = MovingObject("bullet","default",ceil(self.player1.x() + self.player1.x_size),
                                  (ceil(self.player1.y() + self.player1.y_size // 2)-self.bullet.y_size//2),
                                  self.bullet.hp, self.bullet.damage, self.bullet.step, self.bullet.speed_shoot,
                                  self.bullet.x_size, self.bullet.y_size, self.width(), self.height())
            self.bullets.append(bullet)
            self.bullet_timer1.start(msec1)
            self.bullet_timer1.timeout.connect(self.bullet_timer1.stop)

    def check_collision(self):
        if self.player1.HP_O <= 0:
            self.menu.stackWidget.setCurrentWidget(self.menu.game_over_page)
        # Проверяем столкновение пуль с врагами
        for enemy in self.enemies:
            if self.player1.boundingRect().intersects(enemy.boundingRect()):
                    if self.player1.x() + self.player1.x_size//2 < enemy.x():
                        self.player1.l_speed = self.player1.step_x*1.2
                        self.player1.r_speed = 0
                    elif self.player1.x() + self.player1.x_size//2 > enemy.x() + enemy.x_size:
                        self.player1.r_speed = self.player1.step_x*1.2
                        self.player1.l_speed = 0
                    elif self.player1.y() + self.player1.y_size//2 < enemy.y(): # Отталкивание игрока от врага
                        self.player1.u_speed = self.player1.step_y*1.2
                        self.player1.d_speed = 0
                    elif self.player1.y() + self.player1.y_size//2 > enemy.y() + enemy.y_size:
                        self.player1.d_speed = self.player1.step_y*1.2
                        self.player1.u_speed = 0

            if enemy.x() <= -enemy.x_size:
                self.player1.HP_O -= enemy.damage  # Уменьшение здоровья игрока
                self.enemies.remove(enemy)
                continue
            if self.boundingRect().contains(enemy.boundingRect()) is False:
                self.enemies.remove(enemy)
            for bullet in self.bullets:
                if self.boundingRect().contains(bullet.boundingRect()) is False:
                    self.bullets.remove(bullet)
                    continue
                if enemy.x() <= self.width() - (enemy.x_size // 2):
                        if enemy.boundingRect().intersects(bullet.boundingRect()):
                            bullet.HP_O -= 1
                            if bullet. HP_O <= 0:
                                self.bullets.remove(bullet)
                            enemy.HP_O -= (self.bullet.damage * self.player1.damage)
                            if enemy.HP_O <= 0:
                                self.enemies.remove(enemy)


    def updateScene(self):
        self.restart_timer_txt.setText(f'{self.count_restart_sec}')
        if self.restart_timer.isActive() is False:
            if self.count_restart_sec > 1:
                self.restart_timer.start(1000)
                self.count_restart_sec -= 1

        if self.menu.stackWidget.currentWidget() == self and self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
            if self.sec == 3:
                self.menu.stackWidget.setCurrentWidget(self.menu.choose_card_page)
                self.sec +=1
            self.create_bullet(self.player1.speed_shoot)
            self.create_enemy(2000-(10*self.min), self.enemy.speed_shoot)
            self.player1.new_move()
            for bullet in self.bullets:
                bullet.move_direction_R = 1
                bullet.new_move(1,0,0)
            for enemy in self.enemies:
                enemy.move_direction_L = 1
                enemy.new_move(1,0,0)
            self.check_collision()
        else: self.player1.new_move(0)
        if self.isActiveWindow() is False and self.menu.stackWidget.currentWidget() == self:
            self.menu.stackWidget.setCurrentWidget(self.menu.pause_page)
        self.update()

    def keyPressEvent(self, event):
        if self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
            self.player1.keyPressEvent(event)
            if event.text() == 'p':
                pass
            if event.key() == Qt.Key.Key_Escape:  # кнопку надо ограничить в свое нажатии, можно прям в меню ее нажать
                self.menu.stackWidget.setCurrentWidget(self.menu.pause_page)
                pass

    def keyReleaseEvent(self, event):
        self.player1.keyReleaseEvent(event)

        if event.text() == 'p':
                s = 0

        if event.key() == Qt.Key.Key_Escape:
                s = 0

    def paint(self, painter):
        painter.fillRect(0, 0, self.width(), self.height(),
                             QColor(50, 50, 50))  # Очищаем окно, закрашивая его зеленым
        painter.fillRect(0, ceil(self.height() * 0.8), self.width(), self.height(), QColor(100, 100, 100))

        for i in range(self.player1.HP_O):
            painter.fillRect(ceil(self.width() * 0.05) + i * (ceil(self.width() * 0.01) + 2),
                                 ceil(self.height() * 0.82),
                                 ceil(self.width() * 0.01), ceil(self.width() * 0.03), QColor(200, 100, 100))
        self.player1.paint(painter)
        for bullet in self.bullets:
            bullet.paint(painter)
        for enemy in self.enemies:
            enemy.paint(painter)
        if self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
            self.restart_timer_txt.hide()
        else:
            self.restart_timer_txt.show()
            painter.fillRect(0,0,self.width(),self.height(), QColor(0,0,0,200))

    def paintEvent(self, event):
        painter = QPainter(self)
        self.paint(painter)




# возможно для перемещ кнопок можно использовать QWidget/// ахах забей, все проще - вместо addWidget -> addChildWidget
# есть баг - если постоянно увеличивать и уменьшать экран то погрешность движения накапливается.

# как изменть параметры после поднятия сундука. решай

# скалирование от высоты и ширины одновременно

# повышать сложность с помощью сундуков, то есть когда враг поднимает сундук, то усиливает свое братство


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_window = Menu()
    game_window.show()
    sys.exit(app.exec())