import random
import sys
from time import sleep

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QPushButton
from PyQt6.QtGui import QPainter, QColor, QImage
from PyQt6.QtCore import QTimer, Qt, QRect

# константы
W = 1000
H = 600
X_SIZE_PLAYER = 30
Y_SIZE_PLAYER = 20

X_SIZE_ENEMY = 30
Y_SIZE_ENEMY = 30

X_SIZE_BULLET = 15
Y_SIZE_BULLET = 5


class MovingPlayer:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.step = 5
        self.HP_P = 3

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
    def __init__(self, x=W, y=0, HP_E=3):
        self.x = x
        self.y = y
        self.step = 1
        self.HP_E = HP_E

    def move(self):
        self.x -= self.step


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        # pause_button = QPushButton('Пауза', self)
        # # pause_button.clicked.connect(self.pause_game)
        # pause_button.setGeometry(10, 10, 80, 30)

        self.enemies = []
        self.enemy_timer = QTimer()
        self.enemy_timer.timeout.connect(self.create_enemy)
        self.enemy_timer.start(1500)  # Создавать врага каждые 2 секунды

        self.bullets = []
        self.shoot = 0
        self.bullet_timer = QTimer()
        self.bullet_timer.timeout.connect(self.create_bullet)
        self.bullet_timer.start(300)

        # self.hit_timer = QTimer()
        # self.hit_timer.timeout.connect(self.player_hit)
        # self.hit_timer.start(10)

        self.score = 0
        self.score_label = QLabel(self)
        self.score_label.setText("SCORE: 0")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.score_label.setStyleSheet("font-size: 24px; color: royalblue;")
        self.score_label.setGeometry(0, 0,400,50)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(20)  # Вызывать обновление игры каждые 20 миллисекунд

    def initUI(self):
        self.setWindowTitle('Star Defender')
        self.setGeometry(100, 100, W, H)

        self.player = MovingPlayer(10, H // 2)

        self.enemy = MovingEnemy()


    def update_score(self):
        self.score += 1
        self.score_label.setText(f"SCORE: {self.score}")

    def create_enemy(self):
        enemy_y = random.randint(0, H - Y_SIZE_ENEMY)
        enemy = MovingEnemy(W, enemy_y)
        self.enemies.append(enemy)
        self.update()  # Обновляем графическое окно после добавления нового врага

    def create_bullet(self):
        if self.shoot == 1:
            bullet = Shooting(self.player.x + X_SIZE_PLAYER, self.player.y + Y_SIZE_PLAYER//2)
            self.bullets.append(bullet)

            self.update()


    def update_game(self):

        # if self.paused:
        #     return

        self.player.move()

        # Удалить за границей экрана
        bullets_remove = []
        for bullet in self.bullets:
            bullet.move_bullet()
            if bullet.b_x > W+X_SIZE_BULLET:
                bullets_remove.append(bullet)

        # Удалить за границей экрана
        enemies_to_remove = []
        for enemy in self.enemies:
            enemy.move()
            if enemy.x < -X_SIZE_ENEMY:
                enemies_to_remove.append(enemy)


        for bullet in bullets_remove:
            self.bullets.remove(bullet)
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)


        self.check_collision()
        self.update()

    def check_collision(self):
        player_rect = QRect(self.player.x, self.player.y, X_SIZE_PLAYER, Y_SIZE_PLAYER)

        # Проверяем столкновение игрока с врагами
        for enemy in self.enemies:
            enemy_rect = QRect(enemy.x, enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY)
            if player_rect.intersects(enemy_rect):
                self.player.HP_P -= 1  # Уменьшение здоровья игрока
                if self.player.HP_P <= 0:
                    self.game_over()
                self.enemies.remove(enemy)

        # Проверяем столкновение пуль с врагами
        bullets_to_remove = []
        enemies_to_remove = []
        for bullet in self.bullets:
            bullet_rect = QRect(bullet.b_x, bullet.b_y, X_SIZE_BULLET, Y_SIZE_BULLET)
            for enemy in self.enemies:
                enemy_rect = QRect(enemy.x, enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY)
                if bullet_rect.intersects(enemy_rect):
                    bullets_to_remove.append(bullet)
                    enemy.HP_E -= 1
                    if enemy.HP_E <= 0:
                        self.update_score()  # Обновление счета
                        enemies_to_remove.append(enemy)
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

    def game_over(self):
        self.score_rect = QLabel(self)
        self.score_rect.setText("YOU Destroyed!")
        self.score_rect.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_rect.setStyleSheet("font-size: 24px; color: Red;")
        self.score_rect.setGeometry(W//4, H//4, W//2, H//4)
        self.score_rect.show()
        retry_button = QPushButton('Retry', self)
        # resume_button.clicked.connect(self.resume_game)
        retry_button.setGeometry(W//3, H//3, 80, 30)
        self.timer.stop()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W or event.text() == 'ц':
            self.player.move_direction_U = 1
        elif event.key() == Qt.Key.Key_S or event.text() == 'ы':
            self.player.move_direction_D = 1
        elif event.key() == Qt.Key.Key_A or event.text() == 'ф':
            self.player.move_direction_L = 1
        elif event.key() == Qt.Key.Key_D or event.text() == 'в':
            self.player.move_direction_R = 1
        if event.key() == Qt.Key.Key_Space:
            self.shoot = 1


    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_W or event.text() == 'ц':
            self.player.move_direction_U = 0
        elif event.key() == Qt.Key.Key_S or event.text() == 'ы':
            self.player.move_direction_D = 0
        elif event.key() == Qt.Key.Key_A or event.text() == 'ф':
            self.player.move_direction_L = 0
        elif event.key() == Qt.Key.Key_D or event.text() == 'в':
            self.player.move_direction_R = 0
        if event.key() == Qt.Key.Key_Space:
            self.shoot = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(0, 0, W, H, QColor(153, 255, 153))  # Очищаем окно, закрашивая его зеленым

        painter.drawImage(QRect(self.player.x, self.player.y, X_SIZE_PLAYER, Y_SIZE_PLAYER), QImage('player.png'))
        if self.player.HP_P <= 0:
            painter.fillRect(W//4,H//4, W//2, H//2, QColor(102, 51, 0))

        for bullet in self.bullets:
            painter.drawImage(QRect(bullet.b_x, bullet.b_y, X_SIZE_BULLET, Y_SIZE_BULLET), QImage('bullet.png'))

        for enemy in self.enemies:
            painter.drawImage(QRect(enemy.x, enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY), QImage('enemy.png'))



if __name__ == '__main__':
    app = QApplication([])
    game_window = GameWindow()
    game_window.show()
    sys.exit(app.exec())
