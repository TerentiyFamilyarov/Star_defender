import random
import sys
from math import ceil

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGraphicsItem, QGraphicsView, \
    QGraphicsScene, QWidget, QStackedWidget, QVBoxLayout
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush, QResizeEvent, QPalette
from PyQt6.QtCore import QTimer, Qt, QSize, QRectF, QPointF, QPropertyAnimation, QEasingCurve, QPoint, QEvent


class MovingPlayer(QGraphicsItem):
    def __init__(self, x=0, y=0, step=10, HP_P=3, x_size=50, y_size=50, width_window=1920, height_window=1080):
        super().__init__()
        self.step = step
        self.HP_P = HP_P
        self.x_size = x_size
        self.y_size = y_size
        self.setX(x)
        self.setY(y)

        self.move_direction_L = 0
        self.move_direction_R = 0
        self.move_direction_U = 0
        self.move_direction_D = 0
        self.shoot = 0

        self.width_window = width_window
        self.height_window = height_window

    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option=None, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(0, 0, 255))
        painter.drawRect(self.boundingRect())

    def move(self, move = 1):
        if move == 0:
            self.move_direction_L = 0
            self.move_direction_R = 0
            self.move_direction_U = 0
            self.move_direction_D = 0
        else:
            if self.x() - self.step < 0:
                self.setX(0)
            elif self.move_direction_L == 1:
                self.setX(self.x() - self.step)

            if self.x() + self.step > self.width_window - self.x_size:
                self.setX(self.width_window - self.x_size)
            elif self.move_direction_R == 1:
                self.setX(self.x() + self.step)

            if self.y() - self.step < 0:
                self.setY(0)
            elif self.move_direction_U == 1:
                self.setY(self.y() - self.step)

            if self.y() + self.step > self.height_window - self.y_size:
                self.setY(self.height_window - self.y_size)
            elif self.move_direction_D == 1:
                self.setY(self.y() + self.step)



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
    def __init__(self, x=0, y=0, x_size=30, y_size=30):
        super().__init__()
        self.step = 15
        self.x_size = x_size
        self.y_size = y_size
        self.setX(x)
        self.setY(y)

    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option=None, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(0, 255, 0))
        painter.drawRect(self.boundingRect())
        pass

    def move(self, ):
        # if self.x() <= 0:
        self.setX(self.x() + self.step)


class MovingEnemy(QGraphicsItem):
    def __init__(self, x=0, y=50, HP_E=3, step=1, x_size=70, y_size=70, width_window=1920, height_window=1080):
        super().__init__()
        self.step = step
        self.HP_E = HP_E
        self.x_size = x_size
        self.y_size = y_size
        self.width_window = width_window
        self.height_window = height_window
        self.setX(x)
        self.setY(y)

    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option=None, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(255, 0, 0))
        painter.drawRect(self.boundingRect())

    def move(self):
        if self.x() - self.step > 0:
            self.setX(self.x() - self.step)


def create_page(this_page, addwidgets: list):
    page = QVBoxLayout(this_page)
    for i in range(len(addwidgets)):
        page.addWidget(addwidgets[i])
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
        # Main menu 0
        main_menu_page = QWidget()
        main_menu_page.setStyleSheet('background-color: grey')
        self.Main_Title = QLabel()
        Main_Title_txt = create_txt('STAR DEFENDER', 'font-size: 50px; color: Green; text-align: right;',
                                    [100 // 4, 0, 100 // 2, 100])
        self.start_button = QPushButton('Start')
        self.start_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.start_button.clicked.connect(lambda: self.stackWidget.setCurrentIndex(1))
        self.exit_button = QPushButton('Exit')
        self.exit_button.setGeometry(100 // 3, (100 // 3) + 100, 80, 30)
        self.exit_button.clicked.connect(self.close)
        create_page(main_menu_page, [Main_Title_txt, self.start_button, self.exit_button])
        self.stackWidget.addWidget(main_menu_page)

        # Choose mode 1
        choose_menu_page = QWidget()
        choose_mode_txt = create_txt('CHOOSE MODE', 'font-size: 50px; color: Green; text-align: right;',
                                     [100 // 4, 0, 100 // 2, 100])
        self.start_1p_button = QPushButton('1 PLAYER')
        self.start_1p_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.start_1p_button.clicked.connect(self.restart_game)
        self.start_2p_button = QPushButton('2 PLAYER')
        self.start_2p_button.setGeometry(100 // 3, (100 // 3) + 100, 80, 30)
        create_page(choose_menu_page, [choose_mode_txt, self.start_1p_button,
                                       self.start_2p_button, self.main_menu_button()])
        self.stackWidget.addWidget(choose_menu_page)

        # Game over 2
        game_over_page = QWidget()
        game_over_txt = create_txt('YOU DESTROYED !', 'font-size: 50px; color: red;',
                                   [0, 0, 100, 100])
        self.retry_button = QPushButton('Retry', self)
        self.retry_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.retry_button.clicked.connect(self.restart_game)
        create_page(game_over_page, [game_over_txt, self.retry_button, self.main_menu_button()])
        self.stackWidget.addWidget(game_over_page)

        # Pause 3
        pause_page = QWidget()
        pause_game_txt = create_txt('PAUSE', 'font-size: 50px; color: Green;', [0, 0, 100, 100])
        self.resume_button = QPushButton('Resume', self)
        self.resume_button.clicked.connect(lambda: self.stackWidget.setCurrentIndex(4))
        self.resume_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        create_page(pause_page, [pause_game_txt, self.resume_button, self.main_menu_button()])
        self.stackWidget.addWidget(pause_page)


        # Game page 4
        self.start_game = StartGame(self.stackWidget,True,True)
        self.stackWidget.addWidget(self.start_game)
        # Включить полноэкранный режим

        self.showMaximized()

    def resizeEvent(self, event):
        old_width = 200
        old_height = 125

        if self.width() < 700:
            old_width = 700
            old_height = 375
            # self.resize(old_width, old_height)

        if self.width() > old_width:
            old_height += ((self.width() - old_width) // 2)
            old_width = self.width()
        if self.height() > old_height:
            old_width += ((self.height() - old_height) // 1)
            old_height = self.height()
        self.resize(old_width, old_height)

    def main_menu_button(self):
        main_menu_button = QPushButton('Main menu', self)
        main_menu_button.setGeometry(100 // 3, (100 // 3) + 200, 80, 30)
        main_menu_button.clicked.connect(lambda: self.stackWidget.setCurrentIndex(0))
        return main_menu_button


    def restart_game(self):
        self.stackWidget.setCurrentIndex(4)
        self.start_game.game_restart()





class StartGame(QWidget):
    def __init__(self, stakWidget, game_begin=False, ZA_Wardo=True):
        super().__init__()
        self.game_begin = game_begin
        self.stackWidget = stakWidget

        self.mode = 0

        self.previous_size = QSize()

        self.bullets = []
        self.enemies = []

        self.score = -1

        self.font = QFont()
        self.score_label = QLabel(self)
        self.score_label.setText(f"SCORE: {self.score}")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.score_label.setStyleSheet("color: white;")
        self.Player1_HP = QLabel(self)
        self.Player1_HP.setText("HP")
        self.Player1_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player1_HP.setStyleSheet("color: rgb(255,155,155);")


        self.update_score()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScene)
        self.timer.start(16)
        self.enemy_timer = QTimer(self)
        self.bullet_timer1 = QTimer(self)

        self.bullet = Shooting()  # этот предатель существует, но не виден глазу
        self.Main_bullet = Shooting()  # этот предатель существует, но не виден глазу

        self.Main_enemy = MovingEnemy()  # этот предатель существует, но не виден глазу
        self.enemy = MovingEnemy()  # этот предатель существует, но не виден глазу
        # думаю, что вполне возможно исп только один

        self.Main_player = MovingPlayer()  # этот предатель существует, но не виден глазу

        self.player1 = MovingPlayer(0, 0, 10, 5, 50, 50)

    def game_restart(self):
        self.mode = 0

        self.previous_size = QSize()

        self.score = -1
        self.update_score()

        self.bullets = []
        self.enemies = []

        self.player1.setX(0)
        self.player1.setY(0)
        self.player1.HP_P = 5

        self.resizeEvent(None)
        self.showMaximized()

    def resizeEvent(self, event):
        if self.game_begin is True:
            previous_width = 1536
            previous_height = 793
            current_size = self.size()
            # print('Current size ',current_size)
            if self.previous_size.isValid():
                previous_width = self.previous_size.width()
                previous_height = self.previous_size.height()
                # print(f"Previous size: {previous_width} x {previous_height}")

            self.score_label.setGeometry(ceil(self.width() * 0.85), ceil(self.height() * 0.81),
                                         ceil(self.width() * 0.14), 50)
            self.font.setPointSize(ceil(self.width() * 0.02))
            self.score_label.setFont(self.font)

            self.Player1_HP.setGeometry(ceil(self.width() * 0.01), ceil(self.width() * 0.81), ceil(self.width() * 0.04),
                                        100)
            self.Player1_HP.setFont(self.font)

            self.player1.x_size = ceil(self.width() * 0.04)
            self.player1.y_size = ceil(self.width() * 0.04)
            self.player1.width_window = (self.width() * 0.2)
            self.player1.height_window = (self.height() * 0.8)
            pro_x_player_position = self.player1.x() / previous_width
            pro_y_player_position = self.player1.y() / previous_height
            pro_x_player_speed = self.player1.step / previous_width
            self.player1.setX(round(self.width() * pro_x_player_position, 1))
            self.player1.setY(round(self.height() * pro_y_player_position, 1))
            self.player1.step = round(self.width() * pro_x_player_speed, 1)  # нужно найти размер полного экрана
            # сохранение позиции player1 при изменении экрана
            # (в процентном соотношении с округлением до 1 десятой)
            self.enemy.x_size = ceil((self.width() * 0.04) + 10)
            self.enemy.y_size = ceil((self.width() * 0.04) + 10)
            pro_x_enemy_speed = self.enemy.step / previous_width
            self.enemy.step = round(self.width() * pro_x_enemy_speed, 1)  # нужно найти размер полного экрана
            self.enemy.width_window = self.width()
            self.enemy.height_window = self.height()
            for enemy in self.enemies:
                enemy.x_size = ceil((self.width() * 0.04) + 10)
                enemy.y_size = ceil((self.width() * 0.04) + 10)
                pro_x_enemy_position = enemy.x() / previous_width
                pro_y_enemy_position = enemy.y() / previous_height
                enemy.setX(round(self.width() * pro_x_enemy_position, 1))
                enemy.setY(round(self.height() * pro_y_enemy_position, 1))
                enemy.step = round(self.width() * pro_x_enemy_speed, 1)  # нужно найти размер полного экрана

            self.bullet.x_size = ceil((self.width() * 0.02))
            self.bullet.y_size = ceil((self.width() * 0.02))
            # self.bullet.width_window = self.fullW
            # self.bullet.height_window = self.fullH
            pro_x_bullet_speed = self.bullet.step / previous_width
            self.bullet.step = round(self.width() * pro_x_bullet_speed, 1)  # нужно найти размер полного экрана
            for bullet in self.bullets:
                bullet.x_size = ceil((self.width() * 0.02))
                bullet.y_size = ceil((self.width() * 0.02))
                pro_x_bullet_position = bullet.x() / previous_width
                pro_y_bullet_position = bullet.y() / previous_height
                bullet.setX(round(self.width() * pro_x_bullet_position, 1))
                bullet.setY(round(self.height() * pro_y_bullet_position, 1))
                bullet.step = round(self.width() * pro_x_bullet_speed, 1)  # нужно найти размер полного экрана
            self.previous_size = current_size
            self.paintEvent(event)

    def update_score(self):
        self.score += 1
        self.score_label.setText(f"SCORE: {self.score}")

    def create_enemy(self, msec):
        if self.enemy_timer.isActive() is False:
            y_size = self.enemy.y_size
            enemy_y = random.randint(0, int(self.height() * 0.8) - y_size)
            enemy = MovingEnemy(self.width(), enemy_y, self.enemy.HP_E, self.enemy.step, self.enemy.x_size,
                                self.enemy.y_size)
            # сложность можно писать в MovingEnemy
            self.enemies.append(enemy)
            self.enemy_timer.start(msec)
            self.enemy_timer.timeout.connect(self.enemy_timer.stop)

    def create_bullet(self, msec1):
        if self.player1.shoot == 1 and self.bullet_timer1.isActive() is False:
            bullet = Shooting(ceil(self.player1.x() + self.player1.x_size),
                              ceil(self.player1.y() + self.player1.y_size // 2), self.bullet.x_size, self.bullet.y_size)
            self.bullets.append(bullet)
            self.bullet_timer1.start(msec1)
            self.bullet_timer1.timeout.connect(self.bullet_timer1.stop)

    def check_collision(self):
        # Проверяем столкновение пуль с врагами
        for enemy in self.enemies:
            if enemy.x() < (self.width() * 0.2):
                self.enemies.remove(enemy)
                self.player1.HP_P -= 1  # Уменьшение здоровья игрока
                if self.player1.HP_P <= 0:
                    self.stackWidget.setCurrentIndex(2)
                    break
                continue
            for bullet in self.bullets:
                if bullet.x() + bullet.x_size > self.width():
                    self.bullets.remove(bullet)
                    continue
                if enemy.x() <= self.width() - (enemy.x_size // 2):
                    if enemy.boundingRect().intersects(bullet.boundingRect()):
                        self.bullets.remove(bullet)
                        enemy.HP_E -= 1
                        if enemy.HP_E <= 0:
                            self.update_score()  # Обновление счета
                            self.enemies.remove(enemy)

    def updateScene(self):
        if self.stackWidget.currentIndex() == 4:
            self.create_bullet(500)
            self.create_enemy(1800)
            self.player1.move()
            for bullet in self.bullets:
                bullet.move()
            for enemy in self.enemies:
                enemy.move()
            self.check_collision()
        else: self.player1.move(0)
        self.update()

    def keyPressEvent(self, event):
        if self.game_begin is True:
            self.player1.keyPressEvent(event)
            if event.text() == 'p':
                self.stackWidget.setCurrentIndex(2)
                pass
            if event.key() == Qt.Key.Key_Escape:  # кнопку надо ограничить в свое нажатии, можно прям в меню ее нажать
                self.stackWidget.setCurrentIndex(3)
                pass

    def keyReleaseEvent(self, event):
        self.player1.keyReleaseEvent(event)

        if event.text() == 'p':
                s = 0

        if event.key() == Qt.Key.Key_Escape:
                s = 0

    def paintEvent(self, event):
        if self.game_begin is True:
            painter = QPainter(self)
            painter.fillRect(0, 0, self.width(), self.height(),
                             QColor(50, 50, 50))  # Очищаем окно, закрашивая его зеленым
            painter.fillRect(0, 0, ceil(self.width() * 0.2), self.height(), QColor(150, 140, 130))
            painter.fillRect(0, ceil(self.height() * 0.8), self.width(), self.height(), QColor(100, 100, 100))

            for i in range(self.player1.HP_P):
                painter.fillRect(ceil(self.width() * 0.05) + i * (ceil(self.width() * 0.01) + 2),
                                 ceil(self.height() * 0.82),
                                 ceil(self.width() * 0.01), ceil(self.width() * 0.03), QColor(200, 100, 100))
            self.player1.paint(painter)
            for bullet in self.bullets:
                bullet.paint(painter)
            for enemy in self.enemies:
                enemy.paint(painter)


# возможно для перемещ кнопок можно использовать QWidget
# есть баг - если постоянно увеличивать и уменьшать экран то погрешность движения накапливается.




if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_window = Menu()
    game_window.show()
    sys.exit(app.exec())
