import random
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QPushButton
from PyQt6.QtGui import QPainter, QColor, QImage
from PyQt6.QtCore import QTimer, Qt, QRect

# константы

X_SIZE_PLAYER = 30
Y_SIZE_PLAYER = 20

X_SIZE_ENEMY = 30
Y_SIZE_ENEMY = 30

X_SIZE_BULLET = 15
Y_SIZE_BULLET = 5


class MovingPlayer:
    def __init__(self, x=0, y=0, step= 5, HP_P= 3):
        self.x = x
        self.y = y
        self.step = step
        self.HP_P = HP_P

        self.move_direction_L = 0
        self.move_direction_R = 0
        self.move_direction_U = 0
        self.move_direction_D = 0

    def move(self):
        if self.x - self.step < 0:
            self.x = 0
        elif self.move_direction_L == 1:
            self.x -= self.step

        if self.x + self.step > W - X_SIZE_PLAYER:
            self.x = W - X_SIZE_PLAYER
        elif self.move_direction_R == 1:
            self.x += self.step

        if self.y - self.step < 0:
            self.y = 0
        elif self.move_direction_U == 1:
            self.y -= self.step

        if self.y + self.step > H - Y_SIZE_PLAYER:
            self.y = H - Y_SIZE_PLAYER
        elif self.move_direction_D == 1:
            self.y += self.step

class Shooting:
    def __init__(self, b_x= 0, b_y=0):
        self.b_x = b_x
        self.b_y = b_y
        self.step = 5

    def move_bullet(self):
        self.b_x += self.step

class MovingEnemy:
    def __init__(self, x=1000, y=0, HP_E = 3, step = 1):
        self.x = W
        self.y = y
        self.step = step
        self.HP_E = HP_E

    def move(self):
        self.x -= self.step


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.initUI()

        self.HPs_Player_TXT()

        self.enemies = []
        self.enemy_timer = QTimer()
        self.enemy_timer.timeout.connect(self.create_enemy)
        self.enemy_timer.start(1800)  # Создавать врага каждые 2 секунды

        self.bullets1 = []
        self.shoot1 = 0
        self.bullet_timer1 = QTimer()
        self.bullet_timer1.timeout.connect(self.create_bullet1)
        self.bullet_timer1.start(700)

        self.bullets2 = []
        self.shoot2 = 0
        self.bullet_timer2 = QTimer()
        self.bullet_timer2.timeout.connect(self.create_bullet2)
        self.bullet_timer2.start(400)

        self.score = 0
        self.score_label = QLabel(self)
        self.score_label.setText("SCORE: 0")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.score_label.setStyleSheet("font-size: 32px; color: white;")
        self.score_label.setGeometry(W -200, H + 10,200,50)

        self.delete = QTimer()
        self.delete.timeout.connect(self.Delete_OverWindow)
        self.delete.start(1000)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(20)  # Вызывать обновление игры каждые 20 миллисекунд

        self.enemyHP_E = int(self.enemy.HP_E + 0.5 * self.score)
        self.enemystep = self.enemy.step + 5 * self.score

    def initUI(self):
        self.setWindowTitle('Star Defender')
        self.setGeometry(0, 0, W, H+100)

        self.player1 = MovingPlayer(10, 50, 3, 5)
        self.player2 = MovingPlayer(100, H - 50, 7, 3)

        self.enemy = MovingEnemy()

    def HPs_Player_TXT(self):

        self.Player1_HP = QLabel(self)
        self.Player1_HP.setText("P1")
        self.Player1_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player1_HP.setStyleSheet("font-size: 32px; color: skyblue;")
        self.Player1_HP.setGeometry(10, H + 10, X_SIZE_PLAYER_TXT, 100)
        self.Player1_HP.show()

        self.Player2_HP = QLabel(self)
        self.Player2_HP.setText("P2")
        self.Player2_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player2_HP.setStyleSheet("font-size: 32px; color: tomato;")
        self.Player2_HP.setGeometry(30 + X_SIZE_PLAYER_TXT + X_SIZE_PLAYER_HP*self.player2.HP_P, H + 10, X_SIZE_PLAYER_TXT, 100)
        self.Player2_HP.show()



    def update_score(self):
        self.score += 1
        self.score_label.setText(f"SCORE: {self.score}")

    def create_enemy(self):
        enemy_y = random.randint(0, H - Y_SIZE_ENEMY)
        enemy = MovingEnemy(W, enemy_y, self.enemyHP_E, self.enemystep)
        self.enemies.append(enemy)


    def create_bullet1(self):
        if self.shoot1 == 0:
            bullet = Shooting(self.player1.x + X_SIZE_PLAYER, self.player1.y + Y_SIZE_PLAYER//2)
            self.bullets1.append(bullet)
    def create_bullet2(self):
        if self.shoot2 == 0:
            bullet = Shooting(self.player2.x + X_SIZE_PLAYER, self.player2.y + Y_SIZE_PLAYER // 2)
            self.bullets2.append(bullet)


    def Delete_OverWindow(self):#баг обновл игры раз в 1 сек

            # Удалить за границей экрана
        for bullet in self.bullets1:
            bullet.move_bullet()
            if bullet.b_x > W+X_SIZE_BULLET:
                self.bullets1.remove(bullet)
        for bullet in self.bullets2:
            bullet.move_bullet()
            if bullet.b_x > W+X_SIZE_BULLET:
                self.bullets2.remove(bullet)

            # Удалить за границей экрана
        for enemy in self.enemies:
            enemy.move()
            if enemy.x < -X_SIZE_ENEMY:
                self.enemies.remove(enemy)

    def update_game(self):

        self.player1.move()
        self.player2.move()



        self.check_collision()
        self.update()

    def check_collision(self):
        player1_rect = QRect(self.player1.x, self.player1.y, X_SIZE_PLAYER, Y_SIZE_PLAYER)
        player2_rect = QRect(self.player2.x, self.player2.y, X_SIZE_PLAYER, Y_SIZE_PLAYER)

        # Проверяем столкновение игрока с врагами
        for enemy in self.enemies:
            enemy_rect = QRect(enemy.x, enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY)
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
            bullet_rect = QRect(bullet.b_x, bullet.b_y, X_SIZE_BULLET, Y_SIZE_BULLET)
            for enemy in self.enemies:
                enemy_rect = QRect(enemy.x, enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY)
                if bullet_rect.intersects(enemy_rect):
                    self.bullets1.remove(bullet)
                    enemy.HP_E -= 2
                    if enemy.HP_E <= 0:
                        self.update_score()  # Обновление счета
                        self.enemies.remove(enemy)

        for bullet in self.bullets2:
            bullet_rect = QRect(bullet.b_x, bullet.b_y, X_SIZE_BULLET, Y_SIZE_BULLET)
            for enemy in self.enemies:
                enemy_rect = QRect(enemy.x, enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY)
                if bullet_rect.intersects(enemy_rect):
                    self.bullets2.remove(bullet)
                    enemy.HP_E -= 1
                    if enemy.HP_E <= 0:
                        self.update_score()  # Обновление счета
                        self.enemies.remove(enemy)

    def game_over(self):
        self.score_rect = QLabel(self)
        self.score_rect.setText("YOU Destroyed!")
        self.score_rect.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_rect.setStyleSheet("font-size: 24px; color: Red;")
        self.score_rect.setGeometry(W//4, H//4, W//2, H//4)
        self.score_rect.show()
        retry_button = QPushButton('Retry', self)
        retry_button.setGeometry(W//3, H//3, 80, 30)
        self.timer.stop()

    def keyPressEvent(self, event):
        if event.text() in ['A', 'a', 'Ф', 'ф']:
            self.player1.move_direction_U = 1
        elif event.text() in ['D', 'd', 'В', 'в']:
            self.player1.move_direction_D = 1
        elif event.text() in ['S', 's', 'Ы', 'ы']:
            self.shoot1 = 1

        if event.key() == Qt.Key.Key_Left:
            self.player2.move_direction_U = 1
        elif event.key() == Qt.Key.Key_Right:
            self.player2.move_direction_D = 1
        if event.key() == Qt.Key.Key_Down:
            self.shoot2 = 1




    def keyReleaseEvent(self, event):
        if event.text() in ['A', 'a', 'Ф', 'ф']:
            self.player1.move_direction_U = 0
        elif event.text() in ['D', 'd', 'В', 'в']:
            self.player1.move_direction_D = 0
        elif event.text() in ['S', 's', 'Ы', 'ы']:
            self.shoot1 = 0

        if event.key() == Qt.Key.Key_Left:
            self.player2.move_direction_U = 0
        elif event.key() == Qt.Key.Key_Right:
            self.player2.move_direction_D = 0
        if event.key() == Qt.Key.Key_Down:
            self.shoot2 = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(0, 0, W, H, QColor(153, 255, 153))  # Очищаем окно, закрашивая его зеленым
        painter.fillRect(0, H, W , 100, QColor(100,100,100))

        painter.drawImage(QRect(self.player1.x, self.player1.y, X_SIZE_PLAYER, Y_SIZE_PLAYER), QImage('player.png'))
        painter.drawImage(QRect(self.player2.x, self.player2.y, X_SIZE_PLAYER, Y_SIZE_PLAYER), QImage('player.png'))
        if self.player1.HP_P <= 0 or self.player2.HP_P <= 0:
            painter.fillRect(W//4, H//4, W//2, H//2, QColor(102, 51, 0))

        for bullet in self.bullets1:
            painter.drawImage(QRect(bullet.b_x, bullet.b_y, X_SIZE_BULLET, Y_SIZE_BULLET), QImage('bullet.png'))
        for bullet in self.bullets2:
            painter.drawImage(QRect(bullet.b_x, bullet.b_y, X_SIZE_BULLET, Y_SIZE_BULLET), QImage('bullet.png'))

        for enemy in self.enemies:
            painter.drawImage(QRect(enemy.x, enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY), QImage('enemy.png'))

        for i in range(self.player1.HP_P):
            painter.drawImage(QRect(40+i*30, H + 12, X_SIZE_PLAYER_HP, X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))
        for i in range(self.player2.HP_P):
            painter.drawImage(QRect(30 + X_SIZE_PLAYER_TXT + X_SIZE_PLAYER_HP*self.player2.HP_P + 33 + i * 30, H + 12, X_SIZE_PLAYER_HP, X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))


W = 1500
H = 600
X_SIZE_PLAYER_HP = 50
X_SIZE_PLAYER_TXT = 50

if __name__ == '__main__':
    app = QApplication([])
    game_window = GameWindow()
    game_window.show()
    sys.exit(app.exec())
