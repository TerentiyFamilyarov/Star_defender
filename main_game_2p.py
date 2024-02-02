import random
import sys

import Bullets
import Constants
import Enemy

import Player
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QPainter, QColor, QImage
from PyQt6.QtCore import QTimer, Qt, QRect

import Player2


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.Main_menu()
    def Main_menu(self):
        self.initUI()

        self.layout = QVBoxLayout()

        self.game_started = False
        self.game_REstarted = False

        self.button_start = QPushButton("Начать игру", self)
        self.button_start.clicked.connect(self.Start_Game)
        self.layout.addWidget(self.button_start)

        self.button_exit = QPushButton("Выход", self)
        self.button_exit.clicked.connect(self.close)
        self.layout.addWidget(self.button_exit)

        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)



    def Start_Game(self):

        self.game_started = True

        self.button_start.hide()
        self.button_exit.hide()
        if self.game_REstarted:
            self.button_retry.hide()
            self.death_txt.hide()

        self.game_REstarted = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(20)

        self.player1 = Player.MovingPlayer(10, 50, 3, 5)
        self.player2 = Player2.MovingPlayer(100, Constants.H - 50, 7, 1)

        self.HPs_Player_TXT(True)


        self.score = 0
        self.score_txt = QLabel(self)
        self.score_txt.setText("SCORE: 0")
        self.score_txt.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.score_txt.setStyleSheet("font-size: 32px; color: black;")
        self.score_txt.setGeometry(Constants.W -200, Constants.H + 10,200,50)
        self.score_txt.show()

        self.difficult_timer = QTimer()
        self.difficult_timer.timeout.connect(self.update_difficult)
        self.difficult_timer.start(1000)

        self.bullets1 = []
        self.shoot1 = 0
        self.bullet_timer1 = QTimer()
        self.bullet_timer1.timeout.connect(self.create_bullet1)
        self.bullet_timer1.start(2000)

        self.bullets2 = []
        self.shoot2 = 0
        self.bullet_timer2 = QTimer()
        self.bullet_timer2.timeout.connect(self.create_bullet2)
        self.bullet_timer2.start(800)

        self.enemy = Enemy.MovingEnemy()
        self.enemies = []
        self.enemy_timer = QTimer()
        self.enemy_timer.timeout.connect(self.create_enemy)
        self.enemy_timer.start(1800)  # Создавать врага в милисек

    def initUI(self):
        self.setWindowTitle('Star Defender')
        self.setGeometry(20, 30, Constants.W, Constants.H+100)




    def HPs_Player_TXT(self, show = False):

        self.show = show

        self.Player1_HP = QLabel(self)
        self.Player1_HP.setText("P1")
        self.Player1_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player1_HP.setStyleSheet("font-size: 32px; color: skyblue;")
        self.Player1_HP.setGeometry(10, Constants.H + 10, Constants.X_SIZE_PLAYER_TXT, 100)

        self.Player2_HP = QLabel(self)
        self.Player2_HP.setText("P2")
        self.Player2_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player2_HP.setStyleSheet("font-size: 32px; color: tomato;")
        self.Player2_HP.setGeometry(Constants.X_SIZE_PLAYER_HP*self.player1.HP_P,
                                    Constants.H + 10, Constants.X_SIZE_PLAYER_TXT, 100)
        if self.show == True:
            self.Player1_HP.show()
            self.Player2_HP.show()

    def update_score(self):
        self.score += 1
        self.score_txt.setText(f"SCORE: {self.score}")

    def update_difficult(self):
        # self.enemy.HP_E = int(self.score ) #сложность. почему-то возможно только инт, выяснить надо
        # self.enemy.step = int(self.score )
        s=0

    def create_bullet1(self):
        bullet = Bullets.Shooting(self.player1.x + Constants.X_SIZE_PLAYER, self.player1.y + Constants.Y_SIZE_PLAYER // 2)
        self.bullets1.append(bullet)

    def create_bullet2(self):
        bullet = Bullets.Shooting(self.player2.x + Constants.X_SIZE_PLAYER, self.player2.y + Constants.Y_SIZE_PLAYER // 2)
        self.bullets2.append(bullet)

    def create_enemy(self):
        enemy_y = random.randint(0, Constants.H - Constants.Y_SIZE_ENEMY)
        enemy = Enemy.MovingEnemy(Constants.W, enemy_y, self.enemy.HP_E, self.enemy.step)
        self.enemies.append(enemy)

    def update_game(self):

        self.player1.move()
        self.player2.move()

        # Удалить за границей экрана
        for bullet in self.bullets1:
            bullet.move_bullet()
            if bullet.b_x > Constants.W + Constants.X_SIZE_BULLET:
                self.bullets1.remove(bullet)

        for bullet in self.bullets2:
            bullet.move_bullet()
            if bullet.b_x > Constants.W + Constants.X_SIZE_BULLET:
                self.bullets2.remove(bullet)


        self.check_collision()
        self.update()

    def check_collision(self):
        player1_rect = QRect(self.player1.x, self.player1.y, Constants.X_SIZE_PLAYER, Constants.Y_SIZE_PLAYER)
        player2_rect = QRect(self.player2.x, self.player2.y, Constants.X_SIZE_PLAYER, Constants.Y_SIZE_PLAYER)

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

            if player2_rect.intersects(enemy_rect):
                self.player2.HP_P -= 1  # Уменьшение здоровья игрока
                if self.player2.HP_P <= 0:
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
                            self.update_score()  # Обновление счета
                            self.enemies.remove(enemy)

        for bullet in self.bullets2:
            bullet_rect = QRect(bullet.b_x, bullet.b_y, Constants.X_SIZE_BULLET, Constants.Y_SIZE_BULLET)
            for enemy in self.enemies:
                enemy_rect = QRect(enemy.x, enemy.y, Constants.X_SIZE_ENEMY, Constants.Y_SIZE_ENEMY)
                if enemy.x <= Constants.W - Constants.X_SIZE_ENEMY:
                    if bullet_rect.intersects(enemy_rect):
                        self.bullets2.remove(bullet)
                        enemy.HP_E -= 1
                        if enemy.HP_E <= 0:
                            self.update_score()  # Обновление счета
                            self.enemies.remove(enemy)

    def game_over(self):
        self.game_started = False
        self.game_REstarted = True

        self.Player1_HP.hide()
        self.Player2_HP.hide()
        self.score_txt.hide()

        self.timer.stop()

        self.death_txt = QLabel(self)
        self.death_txt.setText("YOU Destroyed!")
        self.death_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.death_txt.setStyleSheet("font-size: 24px; color: Red;")
        self.death_txt.setGeometry(Constants.W//4, Constants.H//4, Constants.W//2, Constants.H//4)
        self.death_txt.show()

        self.button_retry = QPushButton('Retry')
        self.button_retry.clicked.connect(self.Start_Game)
        self.button_retry.setGeometry(Constants.W//3, Constants.H//3, 80, 30)
        self.layout.addWidget(self.button_retry)

        self.button_main_menu = QPushButton('Main menu')
        self.button_main_menu.clicked.connect(self.Main_menu)
        self.button_main_menu.setGeometry(Constants.W // 3, Constants.H // 2, 80, 30)
        self.layout.addWidget(self.button_main_menu)


    def keyPressEvent(self, event):
      if self.game_started == True:
        self.player1.keyPressEvent(event)
        self.player2.keyPressEvent(event)
        if event.text() == 'k':
            self.game_over()

    def keyReleaseEvent(self, event):
        self.player1.keyReleaseEvent(event)
        self.player2.keyReleaseEvent(event)

    def paintEvent(self, event):
        if self.game_started == True:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            painter.fillRect(0, 0, Constants.W, Constants.H, QColor(153, 255, 153))  # Очищаем окно, закрашивая его зеленым
            painter.fillRect(0, Constants.H, Constants.W , 100, QColor(100,100,100))

            painter.drawImage(QRect(self.player1.x, self.player1.y, Constants.X_SIZE_PLAYER, Constants.Y_SIZE_PLAYER), QImage('player.png'))
            painter.drawImage(QRect(self.player2.x, self.player2.y, Constants.X_SIZE_PLAYER, Constants.Y_SIZE_PLAYER), QImage('player.png'))


            for bullet in self.bullets1:
                painter.drawImage(QRect(bullet.b_x, bullet.b_y, Constants.X_SIZE_BULLET, Constants.Y_SIZE_BULLET), QImage('bullet.png'))
            for bullet in self.bullets2:
                painter.drawImage(QRect(bullet.b_x, bullet.b_y, Constants.X_SIZE_BULLET, Constants.Y_SIZE_BULLET), QImage('bullet.png'))

            for enemy in self.enemies:
                painter.drawImage(QRect(enemy.x, enemy.y, Constants.X_SIZE_ENEMY, Constants.Y_SIZE_ENEMY), QImage('enemy.png'))

            for i in range(self.player1.HP_P):
                painter.fillRect(50+i*30, Constants.H + 20, Constants.X_SIZE_PLAYER_HP, Constants.Y_SIZE_PLAYER_HP, QColor(255,255,255))
                # painter.drawImage(QRect(40+i*30, Constants.H + 12, Constants.X_SIZE_PLAYER_HP, Constants.X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))
            for i in range(self.player2.HP_P):
                painter.fillRect(Constants.X_SIZE_PLAYER_HP*self.player1.HP_P + 40 + i*30
                                    , Constants.H + 20, Constants.X_SIZE_PLAYER_HP, Constants.Y_SIZE_PLAYER_HP, QColor(255,255,100))
                # painter.drawImage(QRect(Constants.X_SIZE_PLAYER_HP*self.player1.HP_P + 30 + i*30
                #                         , Constants.H + 12, Constants.X_SIZE_PLAYER_HP, Constants.X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))



if __name__ == '__main__':
    app = QApplication([])
    game_window = GameWindow()
    game_window.show()
    sys.exit(app.exec())
