import random
import sys

from PyQt6.QtCore import QRectF, QTimer, QSize
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsRectItem, QMainWindow

from game import MovingPlayer


class Chest(QGraphicsRectItem):
    def __init__(self, x=0, y=50, width_window=1920, height_window=1080):
        super().__init__()
        self.width_window = width_window
        self.height_window = height_window
        self.setX(x)
        self.setY(y)
        self.x_size = 40
        self.y_size = 40
        self.used_value = []

    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option=None, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(0,0,0))
        painter.drawRect(self.boundingRect())

    def spawn(self):
        rand_x = random.randint(self.width_window//2, self.width_window - self.x_size)
        self.setX(rand_x)
        rand_y = random.randint(0, self.height_window - self.y_size)
        self.setY(rand_y)


class Func_Chest(QWidget):
    def __init__(self, player, main_window):
        super().__init__()
        self.main_window = main_window
        self.player = player
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
                "Speed_Up": 5.2,
                "Very_slow": 0.1
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
        self.main_window.resizeEvent(None)

    def first_button(self):
        self.use_card(self.cards, self.type_cards_1, self.effect_card_1)
        self.close() # не знаю как будет работать с QStackedWidget, возможно нужно будет просто переключится

    def second_button(self):
        self.use_card(self.cards, self.type_cards_2, self.effect_card_2)
        self.close()

    def third_button(self):
        self.use_card(self.cards, self.type_cards_3, self.effect_card_3)
        self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(QRectF(0,0,self.width(), self.height()), QColor(100,100,100))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.previous_size = QSize()
        self.player = MovingPlayer()
        self.chest = Chest(0,0,1000,600)
        # self.chest.spawn()
        self.player.width_window = 1000
        self.player.height_window = 600
        self.init_ui()
    def init_ui(self):
        # layout = QVBoxLayout()

        self.label = QLabel(str(self.player.step),self)
        # self.label.show()
        # layout.addWidget(self.label)

        self.label2 = QLabel(str(self.player.HP_P),self)
        self.label2.move(70,0)
        # self.label2.show()
        # layout.addWidget(self.label2)

        self.func_chest = Func_Chest(self.player, self)

        # self.func_chest.open()
        #
        # self.func_chest.show()

        # layout.addWidget(self.chest.button_one)
        # layout.addWidget(self.chest.button_two)
        # layout.addWidget(self.chest.button_three)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_g)
        self.timer.start(20)

        self.timer_chest = QTimer()
        self.chests = []

        # self.button_increase = QPushButton(f'{self.chest.effect_card_1}')
        # self.button_increase.clicked.connect(self.increase_number)
        # layout.addWidget(self.button_increase)
        #
        # self.button_decrease = QPushButton(f'{self.chest.effect_card_2}')
        # self.button_decrease.clicked.connect(self.decrease_number)
        # layout.addWidget(self.button_decrease)
        #
        # self.button_multiply = QPushButton(f'{self.chest.effect_card_3}')
        # self.button_multiply.clicked.connect(self.multiply_number)
        # layout.addWidget(self.button_multiply)



    def resizeEvent(self, event):
        self.fullW = 1536
        self.fullH = 793
        if self.isMaximized() is True:
            self.fullW = self.width()
            self.fullH = self.height()

        previous_width = 1536
        previous_height = 793
        current_size = self.size()
        # print('Current size ',current_size)
        if self.previous_size.isValid():
            previous_width = self.previous_size.width()
            previous_height = self.previous_size.height()

        pro_x_player_size = self.player.max_x_size / self.fullW
        pro_y_player_size = self.player.max_y_size / self.fullH
        self.player.x_size = int(self.width() * pro_x_player_size)
        self.player.y_size = int(self.height() * pro_y_player_size)
        self.player.width_window = (self.width())
        self.player.height_window = (self.height() * 0.8)
        pro_x_player_position = self.player.x() / previous_width
        pro_y_player_position = self.player.y() / previous_height
        pro_x_player_speed = self.player.max_step / self.fullW
        self.player.setX(round(self.width() * pro_x_player_position, 1))
        self.player.setY(round(self.height() * pro_y_player_position, 1))
        self.player.step = round(self.width() * pro_x_player_speed, 1)  # нужно найти размер полного экрана


        # self.setLayout(layout)

    def update_g(self):
        if self.isActiveWindow() is True:
            self.player.new_move()
            self.label.setText(str(self.player.step))
            self.label2.setText(str(self.player.HP_P))
            self.check_chest()
            self.create_enemy(10000)
        else:
            self.player.new_move(0)
        self.update()


    def create_enemy(self, msec):
        if self.timer_chest.isActive() is False:
            chest = Chest(0,0, 600,600)
            chest.spawn()
            self.chests.append(chest)
            self.timer_chest.start(msec)
            self.timer_chest.timeout.connect(self.timer_chest.stop)

    def check_chest(self):
        for chest in self.chests:
            if self.player.boundingRect().intersects(chest.boundingRect()):
                self.func_chest.open()
                self.func_chest.show()
                self.chests.remove(chest)


    def keyPressEvent(self, event):
        self.player.keyPressEvent(event)
    def keyReleaseEvent(self, event):
        self.player.keyReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.player.paint(painter)
        for chest in self.chests:
            chest.paint(painter,,


    # def use_card(self, cards: dict, type_card: str, effect: str):
    #     if type_card == 'speed_cards':
    #         self.player.step *= cards[type_card][effect]
    #     elif type_card == 'hp_cards':
    #         self.player.HP_P += cards[type_card][effect]
    #
    #
    # def increase_number(self):
    #     self.use_card(self.chest.cards, self.chest.type_cards_1, self.chest.effect_card_1)
    #     self.label.setText(str(self.player.step))
    #     self.label2.setText(str(self.player.HP_P))
    #
    # def decrease_number(self):
    #     self.use_card(self.chest.cards, self.chest.type_cards_2, self.chest.effect_card_2)
    #     self.label.setText(str(self.player.step))
    #     self.label2.setText(str(self.player.HP_P))
    #
    # def multiply_number(self):
    #     self.use_card(self.chest.cards, self.chest.type_cards_3, self.chest.effect_card_3)
    #     self.label.setText(str(self.player.step))
    #     self.label2.setText(str(self.player.HP_P))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
