import random
import sys

import Bullets
import Constants
import Enemy

import Player
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QPushButton
from PyQt6.QtGui import QPainter, QColor, QImage
from PyQt6.QtCore import QTimer, Qt, QRect


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.HPs_Player_TXT()

        self.score = 0
        self.score_label = QLabel(self)
        self.score_label.setText("SCORE: 0")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.score_label.setStyleSheet("font-size: 32px; color: white;")
        self.score_label.setGeometry(Constants.W -200, Constants.H + 10,200,50)

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

        self.enemies = []
        self.enemy_timer = QTimer()
        self.enemy_timer.timeout.connect(self.create_enemy)
        self.enemy_timer.start(1800)  # Создавать врага каждые 2 секунды


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(20)  # Вызывать обновление игры каждые 20 миллисекунд

    def initUI(self):
        self.setWindowTitle('Star Defender')
        self.setGeometry(0, 0, Constants.W, Constants.H+100)

        self.player1 = Player.MovingPlayer(10, 50, 3, 5)
        self.player2 = Player.MovingPlayer(100, Constants.H - 50, 7, 1)


    def HPs_Player_TXT(self):

        self.Player1_HP = QLabel(self)
        self.Player1_HP.setText("P1")
        self.Player1_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player1_HP.setStyleSheet("font-size: 32px; color: skyblue;")
        self.Player1_HP.setGeometry(10, Constants.H + 10, Constants.X_SIZE_PLAYER_TXT, 100)
        self.Player1_HP.show()

        self.Player2_HP = QLabel(self)
        self.Player2_HP.setText("P2")
        self.Player2_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player2_HP.setStyleSheet("font-size: 32px; color: tomato;")
        self.Player2_HP.setGeometry(30 + Constants.X_SIZE_PLAYER_TXT + Constants.X_SIZE_PLAYER_HP*self.player2.HP_P,
                                    Constants.H + 10, Constants.X_SIZE_PLAYER_TXT, 100)
        self.Player2_HP.show()



    def update_score(self):
        self.score += 1
        self.score_label.setText(f"SCORE: {self.score}")

    def create_bullet1(self):
        bullet = Bullets.Shooting(self.player1.x + Constants.X_SIZE_PLAYER, self.player1.y + Constants.Y_SIZE_PLAYER // 2)
        self.bullets1.append(bullet)

    def create_bullet2(self):
        bullet = Bullets.Shooting(self.player2.x + Constants.X_SIZE_PLAYER, self.player2.y + Constants.Y_SIZE_PLAYER // 2)
        self.bullets2.append(bullet)

    def create_enemy(self):
        enemy_y = random.randint(0, Constants.H - Constants.Y_SIZE_ENEMY)
        enemy = Enemy.MovingEnemy(Constants.W, enemy_y)
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
                if bullet_rect.intersects(enemy_rect):
                    self.bullets2.remove(bullet)
                    enemy.HP_E -= 1
                    if enemy.HP_E <= 0:
                        self.update_score()  # Обновление счета
                        self.enemies.remove(enemy)

    def game_over(self):
        self.timer.stop()
        self.score_rect = QLabel(self)
        self.score_rect.setText("YOU Destroyed!")
        self.score_rect.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_rect.setStyleSheet("font-size: 24px; color: Red;")
        self.score_rect.setGeometry(Constants.W//4, Constants.H//4, Constants.W//2, Constants.H//4)
        self.score_rect.show()
        retry_button = QPushButton('Retry', game_window)
        retry_button.clicked.connect(papapewagemmbody)
        retry_button.setGeometry(Constants.W//3, Constants.H//3, 80, 30)
        retry_button.show()


    def keyPressEvent(self, a0):
        self.player1.keyPressEvent(a0)
        self.player2.keyPressEvent(a0)

    def keyReleaseEvent(self, a0):
        self.player1.keyReleaseEvent(a0)
        self.player2.keyReleaseEvent(a0)

    def paintEvent(self, event):
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
            painter.drawImage(QRect(40+i*30, Constants.H + 12, Constants.X_SIZE_PLAYER_HP, Constants.X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))
        for i in range(self.player2.HP_P):
            painter.drawImage(QRect(30 + Constants.X_SIZE_PLAYER_TXT + Constants.X_SIZE_PLAYER_HP*self.player2.HP_P
                                    + 33 + i * 30, Constants.H + 12, Constants.X_SIZE_PLAYER_HP, Constants.X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))

        if self.player1.HP_P <= 0 or self.player2.HP_P <= 0:
            painter.fillRect(Constants.W//4, Constants.H//4, Constants.W//2, Constants.H//2, QColor(102, 51, 0))


if __name__ == '__main__':
    app = QApplication([])
    game_window = GameWindow()
    game_window.show()
    sys.exit(app.exec())
