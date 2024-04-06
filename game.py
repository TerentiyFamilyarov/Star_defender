import random
import sys
from math import ceil

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGraphicsItem, QGraphicsView, \
    QGraphicsScene, QWidget, QStackedWidget, QVBoxLayout, QGraphicsRectItem
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush, QResizeEvent, QPalette, QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt, QSize, QRectF, QPointF, QPropertyAnimation, QEasingCurve, QPoint, QEvent, \
    QVariantAnimation


class MovingPlayer(QGraphicsItem):
    def __init__(self, mode = 0, width_window=1920, height_window=1080):
        super().__init__()
        # self.step = step
        # self.HP_P = HP_P
        # self.x_size = x_size
        # self.y_size = y_size
        # self.setX(x)
        # self.setY(y)

        self.mode = 0
        self.modifications()

        self.move_direction_L = 0
        self.move_direction_R = 0
        self.move_direction_U = 0
        self.move_direction_D = 0
        self.shoot = 0

        self.l_speed = 0
        self.r_speed = 0
        self.u_speed = 0
        self.d_speed = 0

        self.timer = QTimer()

        self.width_window = width_window
        self.height_window = height_window

    def modifications(self):
        if self.mode == 0:
            self.setX(0)
            self.setY(300)
            self.step_x = 8
            self.step_y = 8
            self.max_step = 8
            self.speed_shoot = 370
            self.damage = 2
            self.HP_P = 5
            self.x_size = 50
            self.max_x_size = 50
            self.y_size = 50
            self.max_y_size = 50

        elif self.mode == 1:
            self.setX(0)
            self.setY(300)
            self.step_x = 10
            self.step_y = 10
            self.max_step = 10
            self.speed_shoot = 300
            self.damage = 2
            self.HP_P = 2
            self.x_size = 50
            self.max_x_size = 50
            self.y_size = 50
            self.max_y_size = 50

        elif self.mode == 2:
            self.setX(0)
            self.setY(300)
            self.step_x = 5
            self.step_y = 5
            self.max_step = 5
            self.speed_shoot = 420
            self.damage = 3
            self.HP_P = 7
            self.x_size = 70
            self.max_x_size = 70
            self.y_size = 70
            self.max_y_size = 70


    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option=None, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.mode == 0:
            painter.setBrush(QColor(0, 0, 255))
            painter.drawRect(self.boundingRect())
        elif self.mode == 1:
            painter.drawImage(self.boundingRect(),QImage('low_fanist.jpg'))
        elif self.mode == 2:
            painter.drawImage(self.boundingRect(),QImage('low_2_nokia.jpg'))


    def new_move(self, move=1):
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
            self.timer.start(15)

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
        if self.x() - self.l_speed < 0:
            self.setX(0)
        else:
            self.setX(self.x() - self.l_speed)

        if self.x() + self.r_speed > self.width_window - self.x_size:
            self.setX(self.width_window - self.x_size)
        else:
            self.setX(self.x() + self.r_speed)

        if self.y() - self.u_speed < 0:
            self.setY(0)
        else:
            self.setY(self.y() - self.u_speed)

        if self.y() + self.d_speed > self.height_window - self.y_size:
            self.setY(self.height_window - self.y_size)
        else:
            self.setY(self.y() + self.d_speed)


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




class Shooting(QGraphicsItem):
    def __init__(self, x=0, y=0, step=15, x_size=30, y_size=10):
        super().__init__()
        self.setX(x)
        self.setY(y)
        self.mode = 0
        self.modifications(step, x_size, y_size)

        self.l_speed = 0
        self.r_speed = 0
        self.u_speed = 0
        self.d_speed = 0

    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option=None, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.mode == 1: painter.drawImage(self.boundingRect(), QImage('low_tesak.jpg'))
        elif self.mode == 2: painter.drawImage(self.boundingRect(), QImage('low_amogus.png'))
        else:
            painter.setBrush(QColor(0, 255, 0))
            painter.drawRect(self.boundingRect())
        pass

    def modifications(self, step, x_size, y_size):
            self.step_x = step
            self.step_y = step
            self.max_step_x = step
            self.max_step_y = step
            self.x_size = x_size
            self.max_x_size = x_size
            self.y_size = y_size
            self.max_y_size = y_size


    def move(self):

        self.r_speed = self.step_x

        # self.setX(self.x() - self.l_speed)
        #
        self.setX(self.x() + self.r_speed)
        #
        # self.setY(self.y() - self.u_speed)
        #
        # self.setY(self.y() + self.d_speed)



class Chest(QGraphicsRectItem):
    def __init__(self, x=0, y=50, width_window=1920, height_window=1080):
        super().__init__()
        self.width_window = width_window
        self.height_window = height_window
        self.setX(x)
        self.setY(y)
        self.modifications()
        self.used_value = []

    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option=None, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(0,0,0))
        painter.drawRect(self.boundingRect())

    def spawn(self):
        rand_x = random.randint(self.width_window//4, self.width_window - self.x_size)
        self.setX(rand_x)
        rand_y = random.randint(0, self.height_window - self.y_size)
        self.setY(rand_y)

    def modifications(self, x_size=40, y_size=40):
        self.x_size = x_size
        self.y_size = y_size
        self.max_x_size = x_size
        self.max_y_size = y_size


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
        self.menu.start_game.paint(painter,,
        painter.fillRect(0,0,self.width(),self.height(),QColor(0,0,0,200))


class MovingEnemy(QGraphicsItem):
    def __init__(self, x=0, y=50, HP_E=3, step=1, x_size=70, y_size=70, width_window=1920, height_window=1080):
        super().__init__()
        self.width_window = width_window
        self.height_window = height_window
        self.setX(x)
        self.setY(y)
        self.mode = 0
        self.speed_shoot = 5000 # настоящ
        self.modifications(HP_E,step,self.speed_shoot,x_size,y_size)
        self.a = 100
        self.r = 239
        self.g = 223
        self.b = 200
        self.secret_mode = 0
        self.enemy_creator_msec = 1800

        self.l_speed = 0
        self.r_speed = 0
        self.u_speed = 0
        self.d_speed = 0

    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option=None, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.mode == -1:
            painter.setBrush(QColor(self.r,self.g,self.b,self.a))
            painter.drawRect(self.boundingRect())
        elif self.secret_mode == 1:
            painter.drawImage(self.boundingRect(), QImage('low_low_Nik Saltykov.jpg'))
        elif self.secret_mode == 2: painter.drawImage(self.boundingRect(), QImage('low_loot_bug.jpg'))
        elif self.mode == 0:
            painter.setBrush(QColor(255,0,0))
            painter.drawRect(self.boundingRect())
        elif self.mode == 1:
            painter.setBrush(QColor(255, 150, 150))
            painter.drawRect(self.boundingRect())
        elif self.mode == 2:
            painter.setBrush(QColor(200, 200, 150))
            painter.drawRect(self.boundingRect())
        elif self.mode == 3:
            painter.setBrush(QColor(150, 200, 150))
            painter.drawRect(self.boundingRect())
        elif self.mode == 4:
            painter.setBrush(QColor(150, 0, 0))
            painter.drawRect(self.boundingRect())
        elif self.mode == 5:
            painter.setBrush(QColor(0, 255, 0))
            painter.drawRect(self.boundingRect())

    def modifications(self, HP_E=3, step=1, speed_shoot=2000, x_size=70, y_size=70):
        if self.mode == -1:
            self.step_x = step + (random.randint(0, 3))
            self.x_size = random.randint(1, 10)
            self.y_size = self.x_size
            self.a = random.randint(150,255)
            self.r += random.randint(-20,21)
            self.g += random.randint(-20, 21)
            self.b += random.randint(-20, 21)

        elif self.mode == 0:
            self.step_x = step
            self.step_y = step
            self.max_step_x = step
            self.max_step_y = step
            self.HP_E = HP_E
            self.x_size = x_size
            self.max_x_size = x_size
            self.y_size = y_size
            self.max_y_size = y_size

        elif self.mode == 1:
            self.step_x = step+2
            self.step_y = step+2
            self.max_step_x = step+2
            self.max_step_y = step+2
            self.HP_E = HP_E-2
            self.x_size = x_size-20
            self.max_x_size = x_size-20
            self.y_size = y_size-20
            self.max_y_size = y_size-20

        elif self.mode == 2:
            self.step_x = step-0.2
            self.step_y = step-0.2
            self.max_step_x = step-0.2
            self.max_step_y = step-0.2
            self.HP_E = HP_E+4
            self.x_size = x_size+20
            self.max_x_size = x_size+20
            self.y_size = y_size+20
            self.max_y_size = y_size+20

        elif self.mode == 3:
            self.step_x = step
            self.step_y = step
            self.max_step_x = step
            self.max_step_y = step
            self.HP_E = HP_E
            self.x_size = x_size
            self.max_x_size = x_size
            self.y_size = y_size
            self.max_y_size = y_size
            self.shoot = 0
            self.main_speed_shoot = speed_shoot - 3000 # фальшивка
            self.bullet_enemy_timer = QTimer()

        elif self.mode == 4:
            self.step_x = step + 5
            self.step_y = step + 5
            self.max_step_x = step + 5
            self.max_step_y = step + 5
            self.HP_E = HP_E + 25
            self.x_size = x_size - 30
            self.max_x_size = x_size - 30
            self.y_size = y_size - 30
            self.max_y_size = y_size - 30


    def difficult(self, min, sec):
        if sec >= 30 or min >= 1:
            if min >= 1:
                self.enemy_creator_msec = 1750
            random_chance = random.randint(0,101)
            if random_chance <= 30:
                self.mode = 1
            else:
                self.mode = 0
        elif min >= 2:
            self.enemy_creator_msec = 1700
            random_chance = random.randint(0,101)
            if random_chance <= 15:
                self.mode = 2
            else:
                self.mode = 0
        elif min >= 1 and sec >= 30 or min >= 2:
            self.enemy_creator_msec = 1650
            random_chance = random.randint(0,101)
            if random_chance <= 25:
                self.mode = 3
            else:
                self.mode = 0

    def move(self):

            self.l_speed = self.step_x

            self.setX(self.x() - self.l_speed)
            #
            self.setX(self.x() + self.r_speed)
            #
            self.setY(self.y() - self.u_speed)
            #
            self.setY(self.y() + self.d_speed)




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
        self.setGeometry(0,0,700,375)
        # self.resize(1536,793)
        self.font = QFont()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_bg)
        self.timer.start(14)
        self.star_timer = QTimer()
        self.puls_timer = QTimer()
        self.switch = 0
        self.a = 16
        self.star = MovingEnemy()
        self.previous_size = QSize()
        self.stars = []



        self.current_page = -1
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
        self.current_player_txt = create_txt('mode: 0', 'color: green;', [500, 300, 150, 100])
        self.current_player_txt = create_txt('Speed', 'color: green;', [500, 300, 150, 100])
        self.current_player_txt = create_txt('Health', 'color: green;', [500, 300, 150, 100])

        self.current_player_txt = create_txt('About player', 'color: green;', [500, 300, 150, 100])
        self.start_1mode_button = QPushButton('back')
        self.start_1mode_button.setGeometry(100 // 3, 100 // 3, 80, 30)
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

        # choose effect page 6
        self.choose_effect_page = Func_Chest(self.start_game.player1, self.start_game.enemy,self.start_game, self)
        self.stackWidget.addWidget(self.choose_effect_page)
        # Включить полноэкранный режим
        # self.showFullScreen()
        self.showMaximized()


    def resizeEvent(self, event):
        pass
        if self.stackWidget.currentWidget() != self.start_game and self.stackWidget.currentWidget() != self.choose_effect_page:

            if self.stackWidget.currentWidget() != self.pause_page:
                self.start_game.player1.setPos(ceil(self.width() * 0.6), ceil(self.height() * 0.1))
                self.start_game.player1.x_size = ceil(self.width() * 0.13)
                self.start_game.player1.y_size = ceil(self.width() * 0.13)

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
            pro_x_star_speed = self.star.max_step_x / self.fullW
            self.star.step_x = round(self.width() * pro_x_star_speed, 1)
            self.star.width_window = self.width()
            self.star.height_window = self.height()
            for star in self.stars:
                pro_x_star_position = star.x() / previous_width
                pro_y_star_position = star.y() / previous_height
                star.setX(round(self.width() * pro_x_star_position, 1))
                star.setY(round(self.height() * pro_y_star_position, 1))

            self.previous_size = self.size()

    # Main menu
            self.Main_Title_txt.setGeometry(0, ceil(self.height()*0.1), self.width(), 100)
            # self.Main_Title_txt.setStyleSheet("font-family: Courier, monospace; color: rgba(200,200,200,50)")
            self.font.setPointSize(ceil(self.width()*0.07))
            self.Main_Title_txt.setFont(self.font)
            self.start_button.setGeometry(0, ceil(self.height()*0.7),ceil(self.width()*0.2), ceil(self.width()*0.03))
            self.start_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width()*0.02))
            self.start_button.setFont(self.font)
            self.exit_button.setGeometry(0, ceil(self.height()*0.79), ceil(self.width()*0.2), ceil(self.width()*0.03))
            self.exit_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(0,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.exit_button.setFont(self.font)

    # Choose mode
            self.choose_mode_txt.setGeometry(0, ceil(self.height() * 0.11), self.width(), 100)
            self.choose_mode_txt.setStyleSheet("font-family: Courier, monospace; color: rgb(200,200,200)")
            self.font.setPointSize(ceil(self.width() * 0.03))
            self.choose_mode_txt.setFont(self.font)
            self.start_1p_button.setGeometry(0, ceil(self.height() * 0.3), ceil(self.width() * 0.2), ceil(self.width() * 0.03))
            self.start_1p_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.start_1p_button.setFont(self.font)
            self.start_2p_button.setGeometry(0, ceil(self.height() * 0.39), ceil(self.width() * 0.2),
                                             ceil(self.width() * 0.03))
            self.start_2p_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.start_2p_button.setFont(self.font)
            self.choose_mode_back_button.setGeometry(0, ceil(self.height() * 0.48), ceil(self.width() * 0.2),
                                             ceil(self.width() * 0.03))
            self.choose_mode_back_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; word-spacing: -7px; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.choose_mode_back_button.setFont(self.font)

    # choose player
            self.choose_player_txt.setGeometry(0, ceil(self.height() * 0.12), self.width(), 100)
            self.choose_player_txt.setStyleSheet("font-family: Courier, monospace; color: rgb(200,200,200)")
            self.font.setPointSize(ceil(self.width() * 0.03))
            self.choose_player_txt.setFont(self.font)
            self.current_player_txt.setGeometry(ceil(self.width()*0.5), ceil(self.height() * 0.39), self.width(), 100)
            self.current_player_txt.setStyleSheet("font-family: Courier New, monospace; color: rgb(200,200,200)")
            self.font.setPointSize(ceil(self.width() * 0.023))
            self.current_player_txt.setFont(self.font)
            self.start_1mode_button.setGeometry(ceil(self.width()*0.75), ceil(self.height() * 0.1), ceil(self.width() * 0.1), ceil(self.width() * 0.03))
            self.start_1mode_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.start_1mode_button.setFont(self.font)
            self.start_2mode_button.setGeometry(ceil(self.width()*0.87), ceil(self.height() * 0.1), ceil(self.width() * 0.1),
                                                ceil(self.width() * 0.03))
            self.start_2mode_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.start_2mode_button.setFont(self.font)
            self.confirm_button.setGeometry(ceil(self.width()*0.75), ceil(self.height() * 0.29), ceil(self.width() * 0.2), ceil(self.width() * 0.03))
            self.confirm_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.confirm_button.setFont(self.font)
            self.choose_player_back_button.setGeometry(0, ceil(self.height() * 0.48), ceil(self.width() * 0.25), ceil(self.width() * 0.03))
            self.choose_player_back_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; word-spacing: -20px; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.choose_player_back_button.setFont(self.font)

    # game over
            self.game_over_txt.setGeometry(0, ceil(self.height() * 0.1), self.width(), 100)
            self.game_over_txt.setStyleSheet("font-family: Courier, monospace; color: Crimson")
            self.font.setPointSize(ceil(self.width() * 0.07))
            self.game_over_txt.setFont(self.font)
            self.retry_button.setGeometry(0, ceil(self.height() * 0.3), ceil(self.width() * 0.2),
                                             ceil(self.width() * 0.03))
            self.retry_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.retry_button.setFont(self.font)
            self.game_over_choose_player_button.setGeometry(0, ceil(self.height() * 0.39), ceil(self.width() * 0.3),
                                          ceil(self.width() * 0.03))
            self.game_over_choose_player_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; word-spacing: -7px; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.game_over_choose_player_button.setFont(self.font)
            self.game_over_main_menu_button.setGeometry(0, ceil(self.height() * 0.48), ceil(self.width() * 0.2),
                                                            ceil(self.width() * 0.03))
            self.game_over_main_menu_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; word-spacing: -7px; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.game_over_main_menu_button.setFont(self.font)

    # pause game
            self.pause_game_txt.setGeometry(0, ceil(self.height() * 0.1), self.width(), 100)
            self.pause_game_txt.setStyleSheet("font-family: Courier, monospace; color: rgb(200,200,200)")
            self.font.setPointSize(ceil(self.width() * 0.03))
            self.pause_game_txt.setFont(self.font)
            self.resume_button.setGeometry(0, ceil(self.height() * 0.3), ceil(self.width() * 0.2),
                                          ceil(self.width() * 0.03))
            self.resume_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.resume_button.setFont(self.font)
            self.pause_game_retry_button.setGeometry(0, ceil(self.height() * 0.39), ceil(self.width() * 0.2),
                                           ceil(self.width() * 0.03))
            self.pause_game_retry_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.pause_game_retry_button.setFont(self.font)
            self.pause_game_main_menu_button.setGeometry(0, ceil(self.height() * 0.48), ceil(self.width() * 0.25),
                                                     ceil(self.width() * 0.03))
            self.pause_game_main_menu_button.setStyleSheet(
                "QPushButton {font-family: Courier New, monospace; color: white; letter-spacing: 10px;"
                "             text-align: left; margin: 0px; background-color: rgba(255,0,0,0);}"
                "QPushButton:hover {color: rgb(219,203,180)}")
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.pause_game_main_menu_button.setFont(self.font)






    def create_star(self, msec):
        if self.star_timer.isActive() is False:
            enemy_y = random.randint(0, self.height())
            star = MovingEnemy(self.width(), enemy_y)
            star.mode = -1
            star.modifications(self.star.HP_E, self.star.step_x, self.star.x_size, self.star.y_size)
            self.stars.append(star)
            self.star_timer.start(msec)
            self.star_timer.timeout.connect(self.star_timer.stop)
    def update_bg(self):
        if self.stackWidget.currentWidget() != self.start_game:
            randomint = random.randint(0,101)
            if randomint <= 4:
                self.success = 1
            else:
                self.success = 0
            if self.success == 1:
                self.create_star(1)
            for star in self.stars:
                star.move()
                if star.x() <= 0 or star.step_x == 0:
                    self.stars.remove(star)
            if self.current_page != self.stackWidget.currentIndex():
                self.resizeEvent(None)
                self.current_page = self.stackWidget.currentIndex()
            self.update()
            # print(len(self.stars))

    def main_menu_button(self):
        main_menu_button = QPushButton('Main menu', self)
        main_menu_button.setGeometry(100 // 3, (100 // 3) + 200, 80, 30)
        main_menu_button.clicked.connect(lambda: self.stackWidget.setCurrentWidget(self.main_menu_page))
        return main_menu_button


    def restart_game(self):
        self.stackWidget.setCurrentWidget(self.start_game)
        self.start_game.game_restart(0)

    def onemode(self):
        if self.start_game.player1.mode > 0:
            self.start_game.player1.mode -= 1
        self.current_player_txt.setText(f'mode: {self.start_game.player1.mode}')
        if self.start_game.player1.mode == 1:
            self.current_player_txt.setText('Fanist 17000')
        elif self.start_game.player1.mode == 2:
            self.current_player_txt.setText('Psyho')

    def twomode(self):
        if self.start_game.player1.mode < 2:
            self.start_game.player1.mode += 1
        self.current_player_txt.setText(f'mode: {self.start_game.player1.mode}')
        if self.start_game.player1.mode == 1:
            self.current_player_txt.setText('Fanist 17000')
        elif self.start_game.player1.mode == 2:
            self.current_player_txt.setText('Psyho')

    def resume_game(self):
        self.stackWidget.setCurrentWidget(self.start_game)
        self.start_game.resizeEvent(None)
        self.start_game.count_restart_sec = 4
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(0,0,self.width(),self.height(),QColor('black'))
        if self.stackWidget.currentWidget()== self.main_menu_page:
            self.a = self.pulsation(self.a,15,70,self.puls_timer,100)
        self.Main_Title_txt.setStyleSheet(f"font-family: Courier, monospace; color: rgba(200,200,200,{self.a})")# вот она
        for star in self.stars:
            star.paint(painter,,
        if self.stackWidget.currentWidget() == self.choose_player_page:
            self.start_game.player1.paint(painter)

    def pulsation(self, a, a_low, a_high,timer, msec):
        if self.puls_timer.isActive() is False:
            if a > a_low and self.switch == 0:
                    a -= 1
                    if a == a_low:
                        self.switch = 1
            elif self.switch == 1:
                a += 1
                if a == a_high:
                    self.switch = 0
            timer.timeout.connect(self.puls_timer.stop)
            timer.start(msec)
        return a
























class StartGame(QWidget):
    def __init__(self, menu, game_begin=False):
        super().__init__()
        self.game_begin = game_begin
        self.menu = menu

        self.previous_size = QSize()

        self.count_restart_sec = 3

        self.mode = 0

        self.bullets = []
        self.enemies = []
        self.enemy_deserters = []

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

        self.bullet = Shooting()  # этот предатель существует, но не виден глазу

        self.enemy = MovingEnemy()  # этот предатель существует, но не виден глазу
        # думаю, что вполне возможно исп только один

        self.player1 = MovingPlayer()

        self.chest = Chest()

        self.chest_timer = QTimer()
        self.chests = []

    def boundingRect(self):
        return QRectF(-100,-100, (self.width()+200), (self.height()+200))

    def game_restart(self, mode_player):
        self.count_restart_sec = 1
        self.mode = mode_player

        self.previous_size = QSize()

        self.sec = 0
        self.min = 0
        # self.update_score()
        self.score_label.setText('00:00')

        self.bullets = []
        self.enemies = []
        self.enemy_deserters = []

        self.player1.modifications()


        self.resizeEvent(None)
        self.showMaximized()

    def resizeEvent(self, event):
        if self.game_begin is True:
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
            self.player1.width_window = (self.width())
            self.player1.height_window = (self.height() * 0.8)
            pro_x_player_position = self.player1.x() / previous_width
            pro_y_player_position = self.player1.y() / previous_height
            pro_x_player_speed = self.player1.max_step / self.fullW
            pro_y_player_speed = self.player1.max_step / self.fullH
            self.player1.setX(round(self.width() * pro_x_player_position, 1))
            self.player1.setY(round(self.height() * pro_y_player_position, 1))
            self.player1.step_x = round(self.width() * pro_x_player_speed, 1)
            self.player1.step_y = round(self.height() * pro_y_player_speed, 1)
            # сохранение позиции player1 при изменении экрана
            # (в процентном соотношении с округлением до 1 десятой)

            pro_x_chest_size = self.chest.max_x_size / self.fullW
            pro_y_chest_size = self.chest.max_y_size / self.fullH
            self.chest.x_size = int(self.width() * pro_x_chest_size)
            self.chest.y_size = int(self.height() * pro_y_chest_size)
            self.chest.width_window = self.width()
            self.chest.height_window = self.height()
            for chest in self.chests:
                chest.modifications(self.chest.x_size,self.chest.y_size)
                pro_x_chest_position = chest.x() / previous_width
                pro_y_chest_position = chest.y() / previous_height
                chest.setX(round(self.width() * pro_x_chest_position, 1))
                chest.setY(round(self.height() * pro_y_chest_position, 1))


            pro_x_enemy_size = self.enemy.max_x_size / self.fullW
            pro_y_enemy_size = self.enemy.max_y_size / self.fullH
            self.enemy.x_size = int(self.width() * pro_x_enemy_size)
            self.enemy.y_size = int(self.height() * pro_y_enemy_size)
            pro_x_enemy_speed = self.enemy.max_step_x / self.fullW
            self.enemy.step_x = round(self.width() * pro_x_enemy_speed, 1)
            pro_y_enemy_speed = self.enemy.max_step_y / self.fullH
            self.enemy.step_y = round(self.width() * pro_x_enemy_speed, 1)
            self.enemy.width_window = self.width()
            self.enemy.height_window = self.height()
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
            # self.enemy.difficult(self.min, self.sec)
            y_size = self.enemy.y_size
            enemy_y = random.randint(0, int(self.height() * 0.8) - y_size)
            enemy = MovingEnemy(self.width(), enemy_y)
            # сложность можно писать в MovingEnemy
            enemy.difficult(self.min, self.sec)
            enemy.modifications(self.enemy.HP_E,self.enemy.step_x, self.enemy.speed_shoot,self.enemy.x_size,self.enemy.y_size)
            if enemy.y()+enemy.y_size > int(self.height()*0.8):
                enemy.setY(int(self.height()*0.8)-enemy.y())
            if self.player1.mode == 1:
                enemy.secret_mode = 1
            elif self.player1.mode == 2:
                enemy.secret_mode = 2
            self.enemies.append(enemy)
            self.enemy_timer.start(msec)
            self.enemy_timer.timeout.connect(self.enemy_timer.stop)

        for enemy in self.enemies:
            if enemy.mode == 3:
                if enemy.bullet_enemy_timer.isActive() is False:
                    bullet_enemy = MovingEnemy(ceil(enemy.x()),
                                      (ceil(enemy.y() + enemy.y_size // 2) - self.enemy.y_size // 2),
                                      self.enemy.HP_E, self.enemy.step_x, self.enemy.x_size, self.enemy.y_size)
                    bullet_enemy.mode = 4
                    bullet_enemy.modifications(self.enemy.HP_E,self.enemy.step_x,self.enemy.x_size,self.enemy.y_size)
                    self.enemies.append(bullet_enemy)
                    enemy.bullet_enemy_timer.start(shoot_msec)
                    enemy.bullet_enemy_timer.timeout.connect(enemy.bullet_enemy_timer.stop)

    def create_bullet(self, msec1):
        if self.player1.shoot == 1 and self.bullet_timer1.isActive() is False:
            bullet = Shooting(ceil(self.player1.x() + self.player1.x_size),
                              (ceil(self.player1.y() + self.player1.y_size // 2)-self.bullet.y_size//2),
                              self.bullet.step_x, self.bullet.x_size, self.bullet.y_size)
            if self.player1.mode == 1:
                bullet.mode = 1
            elif self.player1.mode == 2:
                bullet.mode = 2
            self.bullets.append(bullet)
            self.bullet_timer1.start(msec1)
            self.bullet_timer1.timeout.connect(self.bullet_timer1.stop)

    def create_chest(self):
        if self.min >= 0:
            msec = random.randint(3000,45000)
            if self.chest_timer.isActive() is False:
                chest = Chest(0, 0, ceil(self.width()*0.9), ceil(self.height()*0.8))
                chest.modifications(self.chest.x_size,self.chest.y_size)
                chest.spawn()
                self.chests.append(chest)
                self.chest_timer.start(msec)
                self.chest_timer.timeout.connect(self.chest_timer.stop)

    def check_collision(self):
        if self.player1.HP_P <= 0:
            self.menu.stackWidget.setCurrentWidget(self.menu.game_over_page)
        # Проверяем столкновение пуль с врагами
        for enemy in self.enemies:
            for chest in self.chests:
                if self.player1.boundingRect().intersects(chest.boundingRect()):
                    self.menu.choose_effect_page.open()
                    self.menu.stackWidget.setCurrentWidget(self.menu.choose_effect_page)
                    self.chests.remove(chest)
                elif enemy.boundingRect().intersects(chest.boundingRect()):
                    self.menu.choose_effect_page.enemy_open()
                    self.chests.remove(chest)
            if self.player1.boundingRect().intersects(enemy.boundingRect()):
                if enemy.mode != 4 and enemy.mode != 5:
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
                elif enemy.mode == 4:
                    enemy.r_speed = enemy.step_x * 4
                    enemy.u_speed = random.randint(0, (int(enemy.step_y)*2)+1)
                    enemy.d_speed = random.randint(0, (int(enemy.step_y)*2)+1)
                    enemy.mode = 5
                    self.enemy_deserters.append(enemy)
            for deserter in self.enemy_deserters:
                if enemy != deserter:
                    if deserter.boundingRect().intersects(enemy.boundingRect()):
                        enemy.HP_E -= 1
                        self.enemy_deserters.remove(deserter)
                        self.enemies.remove(deserter)
                    if self.boundingRect().contains(deserter.boundingRect()) is False:
                        self.enemy_deserters.remove(deserter)

            if enemy.x() <= -enemy.x_size:
                self.enemies.remove(enemy)
                self.player1.HP_P -= 1  # Уменьшение здоровья игрока
                continue
            if self.boundingRect().contains(enemy.boundingRect()) is False:
                self.enemies.remove(enemy)
            for bullet in self.bullets:
                if bullet.x() + bullet.x_size > self.width():
                    self.bullets.remove(bullet)
                    continue
                if enemy.x() <= self.width() - (enemy.x_size // 2):
                        if enemy.boundingRect().intersects(bullet.boundingRect()):
                            self.bullets.remove(bullet)
                            enemy.HP_E -= self.player1.damage
                            if enemy.HP_E <= 0:
                                self.enemies.remove(enemy)


    def updateScene(self):
        self.restart_timer_txt.setText(f'{self.count_restart_sec}')
        if self.restart_timer.isActive() is False:
            if self.count_restart_sec > 1:
                self.restart_timer.start(1000)
                self.count_restart_sec -= 1

        if self.menu.stackWidget.currentWidget() == self and self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
            if self.isActiveWindow() is True:
                self.create_bullet(self.player1.speed_shoot)
                self.create_enemy(self.enemy.enemy_creator_msec, self.enemy.speed_shoot)
                self.create_chest()
                self.player1.new_move()
                for bullet in self.bullets:
                    bullet.move()
                for enemy in self.enemies:
                    enemy.move()
                self.check_collision()
                # print(self.player1.x_size,' ',self.player1.y_size)
            else: self.player1.new_move(0)
        else: self.player1.new_move(0)
        # self.chest.used_value///////////////////////////////////////////////////////////////////////////////

        self.update()

    def keyPressEvent(self, event):
        if self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
            self.player1.keyPressEvent(event)
            if event.text() == 'p':
                # self.stackWidget.setCurrentIndex(3)
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

        for i in range(self.player1.HP_P):
            painter.fillRect(ceil(self.width() * 0.05) + i * (ceil(self.width() * 0.01) + 2),
                                 ceil(self.height() * 0.82),
                                 ceil(self.width() * 0.01), ceil(self.width() * 0.03), QColor(200, 100, 100))
        for chest in self.chests:
            chest.paint(painter,,
        self.player1.paint(painter)
        for bullet in self.bullets:
            bullet.paint(painter,,
        for enemy in self.enemies:
            enemy.paint(painter,,
        # painter.fillRect(0,0,self.width(),self.height(), QColor(0,0,0,100))
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