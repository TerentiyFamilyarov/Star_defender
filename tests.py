import random
import sys
from time import sleep

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPainter, QColor, QImage
from PyQt6.QtCore import QTimer, Qt, QRect

# константы
W = 1000
H = 600
X_SIZE_PLAYER = 30
Y_SIZE_PLAYER = 20

X_SIZE_ENEMY = 40
Y_SIZE_ENEMY = 30

X_SIZE_BULLET = 20
Y_SIZE_BULLET = 10


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
    def __init__(self, x=W, y=0):
        self.x = x
        self.y = y
        self.step = 1

    def move(self):
        self.x -= self.step


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.enemies = []
        self.enemy_timer = QTimer()
        self.enemy_timer.timeout.connect(self.create_enemy)
        self.enemy_timer.start(2000)  # Создавать врага каждые 2 секунды

        self.bullets = []
        self.shoot = 0
        self.bullet_timer = QTimer()
        self.bullet_timer.timeout.connect(self.create_bullet)
        self.bullet_timer.start(200)

        self.hit_timer = QTimer()
        self.hit_timer.timeout.connect(self.player_hit)
        self.hit_timer.start(1000)

        self.game_over_label = QLabel(self)
        self.game_over_label.setText("Game Over")
        self.game_over_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_over_label.setStyleSheet("font-size: 24px; color: red;")
        self.game_over_label.setGeometry(0, 0, W, H)
        self.game_over_label.hide()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(20)  # Вызывать обновление игры каждые 20 миллисекунд

    def initUI(self):
        self.setWindowTitle('Star Defender')
        self.setGeometry(100, 100, W, H)

        self.player = MovingPlayer(10, H // 2)

        self.enemy = MovingEnemy()


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

    def player_hit(self):
        player_pos_x = [self.player.x, self.player.x + X_SIZE_PLAYER]
        player_pos_y = [self.player.y, self.player.y + Y_SIZE_PLAYER]

        enemy_pos_x = [self.enemy.x, self.enemy.x + X_SIZE_ENEMY]
        enemy_pos_y = [self.enemy.y, self.enemy.y + Y_SIZE_ENEMY]



    def update_game(self):
        self.player.move()

        bullets_remove = []
        for bullet in self.bullets:
            bullet.move_bullet()
            if bullet.b_x > W+X_SIZE_BULLET:
                bullets_remove.append(bullet)
        for bullet in bullets_remove:
            self.bullets.remove(bullet)

        enemies_to_remove = []
        for enemy in self.enemies:
            enemy.move()
            if enemy.x < -X_SIZE_ENEMY:
                enemies_to_remove.append(enemy)
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

        if self.player.HP_P <= 0:
            self.game_over_label.show()

        self.update()

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
        if event.key() == Qt.Key.Key_H:
            self.player.HP_P -=1


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
        if event.key() == Qt.Key.Key_H:
            self.player.HP_P -=0

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(0, 0, W, H, QColor(153, 255, 153))  # Очищаем окно, закрашивая его зеленым

        painter.drawImage(QRect(self.player.x, self.player.y, X_SIZE_PLAYER, Y_SIZE_PLAYER), QImage('player.png'))

        for bullet in self.bullets:
            painter.drawImage(QRect(bullet.b_x, bullet.b_y, X_SIZE_BULLET, Y_SIZE_BULLET), QImage('bullet.png'))

        for enemy in self.enemies:
            painter.drawImage(QRect(enemy.x, enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY), QImage('enemy.png'))



if __name__ == '__main__':
    app = QApplication([])
    game_window = GameWindow()
    game_window.show()
    sys.exit(app.exec())
