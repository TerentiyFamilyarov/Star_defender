import random
import sys
from math import ceil

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QTimer, Qt


class MovingPlayer:
    def __init__(self, x=0, y=0, step=10, HP_P=3, x_size=50, y_size=50, width_window=1920, height_window=1080):
        self.x = x
        self.y = y
        self.step = step
        self.HP_P = HP_P
        self.x_size = x_size
        self.y_size = y_size

        self.move_direction_L = 0
        self.move_direction_R = 0
        self.move_direction_U = 0
        self.move_direction_D = 0

        self.width_window = width_window
        self.height_window = height_window

    def move(self):
        if self.x - self.step < 0:
            self.x = 0
        elif self.move_direction_L == 1:
            self.x -= self.step

        if self.x + self.step > self.width_window - self.x_size:
            self.x = self.width_window - self.x_size
        elif self.move_direction_R == 1:
            self.x += self.step

        if self.y - self.step < 0:
            self.y = 0
        elif self.move_direction_U == 1:
            self.y -= self.step

        if self.y + self.step > ceil(self.height_window * 0.8) - self.y_size:
            self.y = ceil(self.height_window * 0.8) - self.y_size
        elif self.move_direction_D == 1:
            self.y += self.step


class Shooting:
    def __init__(self, b_x=0, b_y=0, x_size=30, y_size=30):
        self.b_x = b_x
        self.b_y = b_y
        self.step = 16
        self.x_size = x_size
        self.y_size = y_size

    def move_bullet(self):
        self.b_x += self.step


class MovingEnemy:
    def __init__(self, x=1000, y=0, HP_E=3, step=1, x_size=60, y_size=60):
        self.x = x
        self.y = y
        self.step = step
        self.HP_E = HP_E
        self.x_size = x_size
        self.y_size = y_size

    def move(self):
        self.x -= self.step


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Papa pewa gemma body')
        self.setGeometry(0, 0, 100, 100)

        self.score = 0

        # Main menu
        self.Main_Title = QLabel(self)
        self.Main_Title.setText("STAR DEFENDER")
        self.Main_Title.setStyleSheet("font-size: 50px; color: Green; text-align: right;")
        self.Main_Title.setGeometry(100 // 4, 0, 100 // 2, 100)
        # Choose mode
        self.choose_mode_txt = QLabel(self)
        self.choose_mode_txt.setText("CHOOSE MODE")
        self.choose_mode_txt.setStyleSheet("font-size: 50px; color: Green; text-align: right;")
        self.choose_mode_txt.setGeometry(100 // 4, 0, 100 // 2, 100)
        # Game over
        self.game_over_txt = QLabel(self)
        self.game_over_txt.setText("YOU DESTROYED !")
        self.game_over_txt.setStyleSheet("font-size: 50px; color: red;")
        self.game_over_txt.setGeometry(0, 0, 100, 100)
        # Pause
        self.pause_game_txt = QLabel(self)
        self.pause_game_txt.setText("PAUSE")
        self.pause_game_txt.setStyleSheet("font-size: 50px; color: Green;")
        self.pause_game_txt.setGeometry(0, 0, 100, 100)
        # showTXTs
        self.score_label = QLabel(self)
        self.score_label.setText(f"SCORE: {self.score}")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.score_label.setStyleSheet("font-size: 32px; color: white;")
        self.Player1_HP = QLabel(self)
        self.Player1_HP.setText("HP")
        self.Player1_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player1_HP.setStyleSheet("font-size: 32px; color: rgb(255,155,155);")
        # buttons
        self.start_button = QPushButton('Start', self)
        self.start_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.start_button.clicked.connect(self.choosing)
        self.exit_button = QPushButton('Exit', self)
        self.exit_button.setGeometry(100 // 3, (100 // 3) + 100, 80, 30)
        self.exit_button.clicked.connect(self.close)
        self.start_1p_button = QPushButton('1 PLAYER', self)
        self.start_1p_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.start_1p_button.clicked.connect(self.one_p_mode)
        self.start_2p_button = QPushButton('2 PLAYER', self)
        self.start_2p_button.setGeometry(100 // 3, (100 // 3) + 100, 80, 30)
        self.start_2p_button.clicked.connect(self.two_p_mode)
        self.retry_button = QPushButton('Retry', self)
        self.retry_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.retry_button.clicked.connect(self.Retry_game)
        self.main_menu_button = QPushButton('Main menu', self)
        self.main_menu_button.setGeometry(100 // 3, (100 // 3) + 100, 80, 30)
        self.main_menu_button.clicked.connect(self.Main_menu)
        self.resume_button = QPushButton('Resume', self)
        self.resume_button.setGeometry(100 // 3, 100 // 3, 80, 30)
        self.resume_button.clicked.connect(self.Resume_game)

        # Включить полноэкранный режим
        self.showMaximized()
        self.resizeEvent(None)

        self.Main_Game(1)

    def Hide_all_pages(self):
        self.Main_Game(0)
        self.Choose_Mode(0)
        self.Pause_game(0)
        self.game_over(0)
        self.show_TXTs(0)

    def resizeEvent(self, event):

        self.fullW = self.width()
        self.fullH = self.height()

        self.Main_Title.setGeometry(self.fullW // 3, 0, self.fullW // 2, self.fullH // 2)
        self.start_button.setGeometry(self.fullW // 3, self.fullH // 3, 80, 30)
        self.exit_button.setGeometry(self.fullW // 3, (self.fullH // 3) + 100, 80, 30)

        self.choose_mode_txt.setGeometry(0, 0, self.fullW, self.fullH)
        self.start_1p_button.setGeometry(self.fullW // 3, self.fullH // 3, 80, 30)
        self.start_2p_button.setGeometry(self.fullW // 3, (self.fullH // 3) + 100, 80, 30)

        self.game_over_txt.setGeometry(self.fullW // 3, 0, self.fullW // 2, self.fullH // 2)
        self.retry_button.setGeometry(self.fullW // 3, self.fullH // 3, 80, 30)
        self.main_menu_button.setGeometry(self.fullW // 3, (self.fullH // 3) + 100, 80, 30)

        self.pause_game_txt.setGeometry(0, 0, self.fullW, self.fullH)
        self.resume_button.setGeometry(self.fullW // 3, self.fullH // 3, 80, 30)
        # self.resume_main_menu_button.setGeometry(self.fullW // 3, (self.fullH // 3) + 100, 80, 30)

        self.score_label.setGeometry(ceil(self.fullW * 0.85), ceil(self.fullH * 0.81), X_INFO_BAR, 50)

        self.Player1_HP.setGeometry(ceil(self.fullW * 0.01), ceil(self.fullH * 0.81), X_SIZE_PLAYER_TXT, 100)

    def Main_Game(self, main_menu_show=1):

        if main_menu_show == 1:
            self.game_started = 0
            self.Game_Continuous(0)
            self.Hide_all_pages()
            self.Main_Title.show()
            self.start_button.show()
            self.exit_button.show()

        else:
            self.Main_Title.hide()
            self.start_button.hide()
            self.exit_button.hide()
            self.start_button.clearFocus()
            self.exit_button.clearFocus()

    def choosing(self):
        self.Choose_Mode(1)

    def Choose_Mode(self, show=1):
        self.choose_show = show
        if show == 1:
            self.Hide_all_pages()
            self.choose_mode_txt.show()
            self.start_1p_button.show()
            self.start_2p_button.show()
            self.main_menu_button.show()
            self.main_menu_button.setGeometry(self.fullW // 3, (self.fullH // 3) + 200, 80, 30)

        else:
            self.choose_mode_txt.hide()
            self.start_1p_button.hide()
            self.start_2p_button.hide()
            self.main_menu_button.hide()
            self.start_1p_button.clearFocus()
            self.start_2p_button.clearFocus()
            self.main_menu_button.clearFocus()

    def one_p_mode(self):
        self.StartGame(0)

    def two_p_mode(self):
        self.StartGame(1)

    def game_over(self, game_over_show=1):

        if game_over_show == 1:
            self.game_started = 0
            self.Game_Continuous(0)
            self.Hide_all_pages()
            self.game_over_txt.show()
            self.retry_button.show()
            self.main_menu_button.show()

        else:
            self.game_over_txt.hide()
            self.retry_button.hide()
            self.main_menu_button.hide()
            self.retry_button.clearFocus()
            self.main_menu_button.clearFocus()

    def Retry_game(self):
        self.StartGame()
        self.score = 0  # отобразить счет после паузы правильно нада а щас не правильно

    def Main_menu(self):
        self.Main_Game(1)

    def Pause_game(self, game_pause_show=1):
        self.pause = game_pause_show
        if game_pause_show == 1:
            # self.game_started = 0
            self.Game_Continuous(0)
            self.Hide_all_pages()
            self.pause_game_txt.show()
            self.resume_button.show()
            self.main_menu_button.show()

        else:
            self.pause_game_txt.hide()
            self.resume_button.hide()
            self.main_menu_button.hide()
            self.resume_button.clearFocus()
            self.main_menu_button.clearFocus()

    def Resume_game(self):
        self.game_started = 1
        self.Game_Continuous(1)
        self.Pause_game(0)
        self.show_TXTs(1)

    def Game_Continuous(self, continue_game=1):

        self.enemy_timer = QTimer()
        self.enemy_timer.timeout.connect(self.create_enemy)

        self.bullet_timer1 = QTimer()

        self.bullet_timer2 = QTimer()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)

        if continue_game == 1:
            self.enemy_timer.start(1800)
            self.timer.start(16)  # Вызывать обновление игры каждые 20 миллисекунд

        else:
            self.enemy_timer.stop()
            self.timer.stop()

    def show_TXTs(self, show=1):

        if show == 1:
            self.score_label.show()
            self.Player1_HP.show()
        else:
            self.score_label.hide()
            self.Player1_HP.hide()

    def StartGame(self, mode=0):
        self.mode = mode
        self.game_started = 1

        if self.game_started == 1:
            self.Hide_all_pages()
            self.show_TXTs(1)
            self.Game_Continuous(1)

            self.score = -1
            self.update_score()

            self.enemies = []

            self.bullets = []
            self.shoot1 = 0
            self.shoot2 = 0

            self.bullet = Shooting()

            self.enemy = MovingEnemy()

            width = self.fullW
            height = self.fullH

            self.player1 = MovingPlayer(220, 50, 10, 5,50,50,width,height)
            self.player2 = MovingPlayer(220, self.fullH - 500, 10,3,50,50,width,height)

    def update_score(self):
        self.score += 1
        self.score_label.setText(f"SCORE: {self.score}")

    def create_enemy(self):
        y_size = self.enemy.y_size
        enemy_y = random.randint(0, ceil(self.fullH * 0.8) - y_size)
        enemy = MovingEnemy(self.player1.x + 1500, enemy_y)
        if self.score != 0:
            if self.score % 5 == 0:
                enemy.step += 1
            if self.score % 10 == 0:
                enemy.HP_E += 5
                enemy.x_size *= 2
                enemy.y_size *= 2

        self.enemies.append(enemy)

    def create_bullet(self):
        if self.shoot1 == 1 and self.bullet_timer1.isActive() is False:
            bullet = Shooting(self.player1.x + self.player1.x_size, self.player1.y + self.player1.y_size // 2)
            self.bullets.append(bullet)
            self.bullet_timer1.start(400)
            self.bullet_timer1.timeout.connect(self.bullet_timer1.stop)

        if self.shoot2 == 1 and self.bullet_timer2.isActive() is False:
            bullet = Shooting(self.player2.x + self.player2.x_size, self.player2.y + self.player2.y_size // 2)
            self.bullets.append(bullet)
            self.bullet_timer2.start(400)
            self.bullet_timer2.timeout.connect(self.bullet_timer2.stop)

    def update_game(self):

        self.player1.move()
        if self.mode == 1: self.player2.move()

        self.create_bullet()

        for bullet in self.bullets:
            bullet.move_bullet()
            if bullet.b_x > self.fullW + self.bullet.x_size:
                self.bullets.remove(bullet)

        for enemy in self.enemies:
            enemy.move()

        self.check_collision()
        self.update()

    def check_collision(self):

        # Проверяем столкновение игрока с врагами
        for enemy in self.enemies:
            if enemy.x < ceil(self.fullW * 0.2):
                self.player1.HP_P -= 1  # Уменьшение здоровья игрока
                if self.player1.HP_P <= 0:
                    self.game_over(1)

                self.enemies.remove(enemy)

        # Проверяем столкновение пуль с врагами
        for bullet in self.bullets:
            for enemy in self.enemies:
                if enemy.x < X_INFO_BAR:
                    self.enemies.remove(enemy)
                if enemy.x <= self.fullW - enemy.x_size:
                    if (bullet.b_x + self.bullet.x_size) >= enemy.x:
                        if (enemy.y <= bullet.b_y <= (enemy.y + enemy.y_size) or enemy.y <= (
                                bullet.b_y + self.bullet.y_size) <= (enemy.y + enemy.y_size)):
                            self.bullets.remove(bullet)
                            enemy.HP_E -= 1
                            if enemy.HP_E <= 0:
                                self.update_score()  # Обновление счета
                                self.enemies.remove(enemy)

    def keyPressEvent(self, event):
        if self.game_started == 1:
            if event.text() in ['W', 'w', 'Ц', 'ц']:
                self.player1.move_direction_U = 1
            elif event.text() in ['S', 's', 'Ы', 'ы']:
                self.player1.move_direction_D = 1
            elif event.text() in ['C', 'c', 'С', 'с']:
                self.shoot1 = 1

            if event.text() == 'p':
                self.game_over(1)

            if event.key() == Qt.Key.Key_Escape:  # кнопку надо ограничить в свое нажатии, можно прям в меню ее нажать
                self.Pause_game(1)

            if self.mode == 1:
                if event.key() == Qt.Key.Key_Up:
                    self.player2.move_direction_U = 1
                elif event.key() == Qt.Key.Key_Down:
                    self.player2.move_direction_D = 1
                if event.key() == Qt.Key.Key_M:
                    self.shoot2 = 1

    def keyReleaseEvent(self, event):
        if self.game_started == 1:
            if event.text() in ['W', 'w', 'Ц', 'ц']:
                self.player1.move_direction_U = 0
            elif event.text() in ['S', 's', 'Ы', 'ы']:
                self.player1.move_direction_D = 0
            elif event.text() in ['C', 'c', 'С', 'с']:
                self.shoot1 = 0

            if event.text() == 'p':
                s = 0

            if event.key() == Qt.Key.Key_Escape:
                s = 0

            if self.mode == 1:
                if event.key() == Qt.Key.Key_Up:
                    self.player2.move_direction_U = 0
                elif event.key() == Qt.Key.Key_Down:
                    self.player2.move_direction_D = 0
                if event.key() == Qt.Key.Key_M:
                    self.shoot2 = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.game_started == 1:

            painter.fillRect(0, 0, self.fullW, self.fullH,
                             QColor(153, 255, 153))  # Очищаем окно, закрашивая его зеленым
            painter.fillRect(0, 0, ceil(self.fullW * 0.2), self.fullH, QColor(150, 140, 130))
            painter.fillRect(0, ceil(self.fullH * 0.8), self.fullW, self.fullH, QColor(100, 100, 100))

            # painter.drawImage(QRect(self.player1.x, self.player1.y, X_SIZE_PLAYER, Y_SIZE_PLAYER), QImage('player.png'))
            # painter.drawImage(QRect(self.player2.x, self.player2.y, X_SIZE_PLAYER, Y_SIZE_PLAYER), QImage('player.png'))
            painter.fillRect(self.player1.x, self.player1.y, self.player1.x_size, self.player1.y_size,
                             QColor('skyblue'))
            if self.mode == 1: painter.fillRect(self.player2.x, self.player2.y, self.player2.x_size,
                                                self.player2.y_size, QColor('green'))

            for bullet in self.bullets:
                # painter.drawImage(QRect(bullet.b_x, bullet.b_y, X_SIZE_BULLET, Y_SIZE_BULLET), QImage('bullet.png'))
                painter.fillRect(bullet.b_x, bullet.b_y, self.bullet.x_size, self.bullet.y_size, QColor(100, 100, 100))

            for enemy in self.enemies:
                # painter.drawImage(QRect(enemy.x, enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY), QImage('enemy.png'))
                painter.fillRect(enemy.x, enemy.y, enemy.x_size, enemy.y_size, QColor(255, 255, 255))

            for i in range(self.player1.HP_P):
                # painter.drawImage(QRect(40+i*30, H + 12, X_SIZE_PLAYER_HP, X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))
                painter.fillRect(ceil(self.fullW * 0.04) + i * (X_SIZE_PLAYER_HP + 2), ceil(self.fullH * 0.81),
                                 X_SIZE_PLAYER_HP, Y_SIZE_PLAYER_HP, QColor(200, 100, 100))
            # for i in range(self.player2.HP_P):
            #     painter.drawImage(QRect(30 + X_SIZE_PLAYER_TXT + X_SIZE_PLAYER_HP*self.player2.HP_P + 33 + i * 30, H + 12, X_SIZE_PLAYER_HP, X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))

        else:
            painter.fillRect(0, 0, self.fullW, self.fullH, QColor(123, 123, 123))



# W = 1539-200
# H = 793-200
X_SIZE_PLAYER_HP = 15
Y_SIZE_PLAYER_HP = 50
X_SIZE_PLAYER_TXT = 50
X_INFO_BAR = 200

if __name__ == '__main__':
    app = QApplication([])
    game_window = GameWindow()
    game_window.show()
    sys.exit(app.exec())
