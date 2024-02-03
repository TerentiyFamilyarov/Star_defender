import random
import sys

import Bullets
import Constants
import Enemy

import Player
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QPainter, QColor, QImage
from PyQt6.QtCore import QTimer, Qt, QRect


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.Main_menu()
    def Main_menu(self):
        self.initUI()

        self.layout = QVBoxLayout()

        self.game_started = False

        self.button_player = QPushButton("1 Player", self)
        self.button_player.clicked.connect(self.Start_Game)
        self.layout.addWidget(self.button_player)
        self.button_player.setGeometry(100, 400, 80, 30)

        self.button_players = QPushButton("2 Players", self)
        self.button_players.clicked.connect(self.Start_Game)
        self.layout.addWidget(self.button_players)
        self.button_players.setGeometry(100, 500, 80, 30)

        self.button_exit = QPushButton("Exit", self)
        self.button_exit.clicked.connect(self.close)
        self.layout.addWidget(self.button_exit)
        self.button_exit.setGeometry(100, 600, 80, 30)

        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)



    def Start_Game(self):
        self.game_started = True

        self.button_player.hide()
        self.button_players.hide()
        self.button_exit.hide()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(20)

        self.player1 = Player.MovingPlayer(10, 50, 5, 5)
        self.player1.Disaster =0 # сделать типа массивом чтобы было несколько бедствий


        self.HPs_Player_TXT(True)

        self.timer_time_score_s = 0
        self.timer_time_score_m = 0
        self.timer_time = QTimer()
        self.timer_time.timeout.connect(self.update_time)
        self.timer_time.start(1000)
        self.timer_txt = QLabel(self)
        self.timer_txt.setText("TIME: 0 s")
        self.timer_txt.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.timer_txt.setStyleSheet("font-size: 32px; color: black;")
        self.timer_txt.setGeometry(Constants.W -200, Constants.H + 10,200,50)
        self.timer_txt.show()

        self.difficult_timer = QTimer()
        self.difficult_timer.timeout.connect(self.update_difficult)
        self.difficult_timer.start(1000)

        self.bullets1 = []
        self.shoot1 = 0
        self.bullet_timer1 = QTimer()
        self.bullet_timer1.timeout.connect(self.create_bullet1)
        self.bullet_timer1.start(1000)


        self.enemy = Enemy.MovingEnemy()
        self.enemies = []
        self.enemy_timer = QTimer()
        self.enemy_timer.timeout.connect(self.create_enemy)
        self.enemy_timer.start(1800)  # Создавать врага в милисек

    def initUI(self):
        self.setWindowTitle('Star Defender')
        self.setGeometry(100, 100, Constants.W, Constants.H+100)




    def HPs_Player_TXT(self, show = False):

        self.Player1_HP = QLabel(self)
        self.Player1_HP.setText("P1")
        self.Player1_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player1_HP.setStyleSheet("font-size: 32px; color: skyblue;")
        self.Player1_HP.setGeometry(10, Constants.H + 10, Constants.X_SIZE_PLAYER_TXT, 100)


        if show == True:
            self.Player1_HP.show()


    def update_time(self):
        self.timer_time_score_s += 1
        if self.timer_time_score_s == 60:
            self.timer_time_score_s = 0
            self.timer_time_score_m += 1

        if self.timer_time_score_m > 0:
            self.timer_txt.setText(f'TIME: {self.timer_time_score_m} m {self.timer_time_score_s} s')
        else: self.timer_txt.setText(f"TIME: {self.timer_time_score_s} s")


    def update_difficult(self):
        # self.enemy.HP_E = int(self.score ) #сложность. почему-то возможно только инт, выяснить надо
        # self.enemy.step = int(self.score )
        s=0

    def create_bullet1(self):
        bullet = Bullets.Shooting(self.player1.x + Constants.X_SIZE_PLAYER, self.player1.y + Constants.Y_SIZE_PLAYER // 2)
        self.bullets1.append(bullet)

    def create_enemy(self):
        enemy_y = random.randint(0, Constants.H - Constants.Y_SIZE_ENEMY)
        enemy = Enemy.MovingEnemy(Constants.W, enemy_y, self.enemy.HP_E, self.enemy.step)
        self.enemies.append(enemy)

    def update_game(self):

        self.player1.move()
        if self.player1.Disaster == 'UWindy': self.player1.move_up()

        # Удалить за границей экрана
        for bullet in self.bullets1:
            bullet.move_bullet()
            if bullet.b_x > Constants.W + Constants.X_SIZE_BULLET:
                self.bullets1.remove(bullet)


        self.check_collision()
        self.update()

    def check_collision(self):
        player1_rect = QRect(self.player1.x, self.player1.y, Constants.X_SIZE_PLAYER, Constants.Y_SIZE_PLAYER)

        # Удалить за границей экрана
        for enemy in self.enemies:
            enemy.move()
            enemy_rect = QRect(enemy.x, enemy.y, Constants.X_SIZE_ENEMY, Constants.Y_SIZE_ENEMY)
            if enemy.x < -Constants.X_SIZE_ENEMY:
                self.enemies.remove(enemy)
                # Проверяем столкновение игрока с врагами
            if player1_rect.intersects(enemy_rect):
                self.player1.HP_P -= 1  # Уменьшение здоровья игрока
                if self.player1.HP_P <= 0:
                    self.game_over()
                self.enemies.remove(enemy)


        # Проверяем столкновение пуль с врагами
        for bullet in self.bullets1:
            bullet_rect = QRect(bullet.b_x, bullet.b_y, Constants.X_SIZE_BULLET, Constants.Y_SIZE_BULLET)
            for enemy in self.enemies:
                enemy_rect = QRect(enemy.x, enemy.y, Constants.X_SIZE_ENEMY, Constants.Y_SIZE_ENEMY)
                if enemy.x <= Constants.W-Constants.X_SIZE_ENEMY:
                    if bullet_rect.intersects(enemy_rect):
                        self.bullets1.remove(bullet)
                        enemy.HP_E -= 2
                        if enemy.HP_E <= 0:
                            self.enemies.remove(enemy)


    def game_over(self):
        self.timer.stop()
        DeathWindow()
        death_window.show()


    def keyPressEvent(self, event):
        if self.game_started == True:
            self.player1.keyPressEvent(event)
        if event.text() == 'p':
            self.game_over()

    def keyReleaseEvent(self, event):
        self.player1.keyReleaseEvent(event)

    def paintEvent(self, event):
        if self.game_started == True:
            painter = QPainter(self)

            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            painter.fillRect(0, 0, Constants.W, Constants.H, QColor(153, 255, 153))  # Очищаем окно, закрашивая его зеленым
            painter.fillRect(0, Constants.H, Constants.W , 100, QColor(100,100,100))

            painter.drawImage(QRect(self.player1.x, self.player1.y, Constants.X_SIZE_PLAYER, Constants.Y_SIZE_PLAYER), QImage('player.png'))

            for bullet in self.bullets1:
                painter.drawImage(QRect(bullet.b_x, bullet.b_y, Constants.X_SIZE_BULLET, Constants.Y_SIZE_BULLET), QImage('bullet.png'))

            for enemy in self.enemies:
                painter.drawImage(QRect(enemy.x, enemy.y, Constants.X_SIZE_ENEMY, Constants.Y_SIZE_ENEMY), QImage('enemy.png'))

            for i in range(self.player1.HP_P):
                painter.fillRect(50+i*30, Constants.H + 20, Constants.X_SIZE_PLAYER_HP, Constants.Y_SIZE_PLAYER_HP, QColor(255,255,255))
                # painter.drawImage(QRect(40+i*30, Constants.H + 12, Constants.X_SIZE_PLAYER_HP, Constants.X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))


class DeathWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Over")
        self.setFixedSize(400, 300)

        self.Game = GameWindow()

        self.layout = QVBoxLayout(self)

        self.death_txt = QLabel(self)
        self.death_txt.setText("YOU Destroyed!")
        self.death_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.death_txt.setStyleSheet("font-size: 24px; color: Red;")
        self.layout.addWidget(self.death_txt)

        self.button_retry = QPushButton('Retry', self)
        self.button_retry.clicked.connect(self.start_game)
        self.layout.addWidget(self.button_retry)

        self.button_main_menu = QPushButton('Main menu', self)
        self.button_main_menu.clicked.connect(self.main_menu)
        self.layout.addWidget(self.button_main_menu)

        self.setLayout(self.layout)
        self.show()

    def start_game(self):
        self.Game.Start_Game()

    def main_menu(self):
        self.Game.Main_menu()



if __name__ == '__main__':
    app = QApplication([])
    game_window = GameWindow()
    death_window = DeathWindow()
    death_window.hide()
    game_window.show()
    sys.exit(app.exec())
