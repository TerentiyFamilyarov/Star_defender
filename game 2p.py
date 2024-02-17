import random
import sys
from math import ceil

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGraphicsItem, QGraphicsView, \
    QGraphicsScene, QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush, QResizeEvent
from PyQt6.QtCore import QTimer, Qt, QSize, QRectF, QPointF, QPropertyAnimation, QEasingCurve, QPoint


class MovingPlayer(QGraphicsItem):
    def __init__(self, p_x=0, p_y=0, step=10, HP_P=3, x_size=50, y_size=50, width_window=1920, height_window=1080):
        super().__init__()
        self.p_x = p_x
        self.p_y = p_y
        self.step = step
        self.HP_P = HP_P
        self.x_size = x_size
        self.y_size = y_size
        self.setX(p_x)
        self.setY(p_y)

        self.move_direction_L = 0
        self.move_direction_R = 0
        self.move_direction_U = 0
        self.move_direction_D = 0

        self.width_window = width_window
        self.height_window = height_window

    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option, widget = ...):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(0, 0, 255))
        painter.drawRect(self.boundingRect())

    def advance(self, phase):
        if phase == 0:
            return

        if self.p_x > 0 and self.move_direction_L == 1:
            self.setX(self.x() - self.step)
            self.p_x = self.x()

        if self.x() + self.x_size <= self.width_window and self.move_direction_R == 1:
            self.setX(self.x() + self.step)
            self.p_x = self.x()

        if self.p_y > 0 and self.move_direction_U == 1:
            self.setY(self.y() - self.step)
            self.p_y = self.y()

        if self.y() + self.y_size <= self.height_window and self.move_direction_D == 1:
            self.setY(self.y() + self.step)
            self.p_y = self.y()


class Shooting(QGraphicsItem):
    def __init__(self, b_x=0, b_y=0, x_size=30, y_size=30):
        super().__init__()
        self.b_x = b_x
        self.b_y = b_y
        self.step = 16
        self.x_size = x_size
        self.y_size = y_size
        self.setX(b_x)
        self.setY(b_y)

    def boundingRect(self):
        return QRectF(self.x(), self.y(), self.x_size, self.y_size)

    def paint(self, painter, option, widget=...):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(0, 255, 0))
        painter.drawRect(self.boundingRect())
        pass

    def advance(self, phase):
        if phase == 0:
            return

        # if self.x() <= 0:
        self.setX(self.x() + self.step)
        self.b_x = self.x()


class MovingEnemy(QWidget):
    def __init__(self, parent=None,e_x=0, e_y=50, HP_E=3, step=1, x_size=60, y_size=60,width_window=1920, height_window=1080):
        super().__init__(parent)
        self.step = step
        self.HP_E = HP_E
        self.x_size = x_size
        self.y_size = y_size
        self.width_window = width_window
        self.height_window = height_window
        self.e_x = e_x
        self.e_y = e_y

        self.child = QWidget(self)
        self.child.setStyleSheet("background-color:red;border-radius:15px;")
        self.setGeometry(self.e_x,self.e_y,60,60)
        self.anim = QPropertyAnimation(self.child, b"pos")
        # self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        # self.anim.setEndValue(QPoint(400, 400))
        # self.anim.setDuration(1500)
        # self.anim.start()


    # def boundingRect(self):
    #     return QRectF(self.e_x, self.e_y, self.x_size, self.y_size)

    # def paint(self, painter, option, widget = ...):
    #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    #     painter.setBrush(QColor(255, 0, 0))
    #     painter.drawRect(self.e_x, self.e_y, self.x_size, self.y_size)
    #     pass


    def advance(self, phase):
        if phase == 0:
            return

        self.e_x -= self.step
        self.child.move(self.e_x, self.e_y)


class GameWindow(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Papa pewa gemma body')
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.game_started = 0
        self.score = 0
        self.previous_size = QSize()

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
        self.font = QFont()
        self.score_label = QLabel(self)
        self.score_label.setText(f"SCORE: {self.score}")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.score_label.setStyleSheet("color: white;")
        self.Player1_HP = QLabel(self)
        self.Player1_HP.setText("HP")
        self.Player1_HP.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Player1_HP.setStyleSheet("color: rgb(255,155,155);")
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
        self.setSceneRect(0,0,200,125)
        self.showMaximized()
        self.setBackgroundBrush(QColor('rgb(20,20,20)'))

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

        previous_width = 1536
        previous_height = 793
        current_size = self.size()
        if self.previous_size.isValid():
            previous_width = self.previous_size.width()
            previous_height = self.previous_size.height()
            print(f"Previous size: {previous_width} x {previous_height}")


        if self.game_started == 1:
            self.enemy.width_window = self.fullW
            self.enemy.height_window = self.fullH

            self.player1.x_size = ceil(self.fullW*0.04)
            self.player1.y_size = ceil(self.fullW*0.04)
            self.player1.width_window = self.fullW
            self.player1.height_window = self.fullH
            # self.player1.x = ceil(self.fullW * (self.player1.x / previous_height))
            self.player1.p_y = ceil(self.fullH*(self.player1.p_y / previous_height))

            for bullet in self.bullets:
                bullet.x_size = ceil(self.fullW*0.02)
                bullet.y_size = ceil(self.fullW*0.02)
                bullet.b_x = ceil(self.fullW*(bullet.b_x / previous_width))
                bullet.b_y = ceil(self.fullH*(bullet.b_y / previous_height))

            for self.enemy in self.enemies:
                self.enemy.x_size = ceil(self.fullW*0.05)
                self.enemy.y_size = ceil(self.fullW*0.05)
                self.enemy.e_x = ceil(self.fullW*(self.enemy.e_x / previous_width))
                self.enemy.e_y = ceil(self.fullH*(self.enemy.e_y / previous_height))
                self.enemy.step = self.enemy.step*(self.fullW / previous_width)


        self.previous_size = current_size


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

        self.score_label.setGeometry(ceil(self.fullW * 0.85), ceil(self.fullH * 0.81), ceil(self.fullW*0.14), 50)
        self.font.setPointSize(ceil(self.width() * 0.02))
        self.score_label.setFont(self.font)

        self.Player1_HP.setGeometry(ceil(self.fullW * 0.01), ceil(self.fullH * 0.81), ceil(self.fullW*0.04), 100)
        self.Player1_HP.setFont(self.font)


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
        self.timer.timeout.connect(self.updateScene)

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
            self.player1 = MovingPlayer(220, 50, 10, 5,50,50)
            self.player2 = MovingPlayer(220, self.fullH - 500, 10,3,50,50,width,height)
            self.scene().addItem(self.player1)
            # self.scene().addItem(self.player2)

            self.resizeEvent(None)

    def update_score(self):
        self.score += 1
        self.score_label.setText(f"SCORE: {self.score}")

    def create_enemy(self):
        # self.enemy.x_size = ceil(self.fullW * 0.05)
        # self.enemy.y_size = ceil(self.fullW * 0.05)
        # self.enemy.x = ceil(self.fullW * (self.enemy.x / self.previous_size.width()))
        # self.enemy.y = ceil(self.fullH * (self.enemy.y / self.previous_size.height()))

        y_size = self.enemy.y_size
        enemy_y = random.randint(0, self.height() - y_size)
        enemy = MovingEnemy(self,600, enemy_y,self.enemy.HP_E,self.enemy.step,self.enemy.x_size,self.enemy.y_size)
        # сложность можно писать в MovingEnemy
        enemy.show()
        self.enemies.append(enemy)
        pass

    def create_bullet(self):
        if self.shoot1 == 1 and self.bullet_timer1.isActive() is False:
            bullet = Shooting(self.player1.p_x + self.player1.x_size, self.player1.p_y + self.player1.y_size // 2,self.bullet.x_size,self.bullet.y_size)
            self.scene().addItem(bullet)
            self.bullets.append(bullet)
            self.bullet_timer1.start(400)
            self.bullet_timer1.timeout.connect(self.bullet_timer1.stop)

        if self.shoot2 == 1 and self.bullet_timer2.isActive() is False:
            bullet = Shooting(self.player2.p_x + self.player2.x_size, self.player2.p_y + self.player2.y_size // 2)
            self.scene().addItem(bullet)
            self.bullets.append(bullet)
            self.bullet_timer2.start(400)
            self.bullet_timer2.timeout.connect(self.bullet_timer2.stop)
        pass

    def update_game(self):
        # if self.mode == 1: self.player2.move()
        #

        # for enemy in self.enemies:
        #     enemy.move_enemy()

        # self.check_collision()
        # self.scene().update()
        pass

    def updateScene(self, **kwargs):
        self.create_bullet()
        self.scene().update()
        self.scene().advance()
        self.check_collision()



    def check_collision(self):

        # Проверяем столкновение игрока с врагами
        for enemy in self.enemies:
            if enemy.e_x < ceil(self.fullW * 0.2):
                self.player1.HP_P -= 1  # Уменьшение здоровья игрока
                if self.player1.HP_P <= 0:
                    self.game_over(1)

                self.enemy.close()
                self.enemies.remove(enemy)

        # Проверяем столкновение пуль с врагами
        for bullet in self.bullets:
            for enemy in self.enemies:
                if enemy.e_x < X_INFO_BAR:
                    enemy.deleteLater()
                    self.enemies.remove(enemy)
                if enemy.e_x <= self.fullW - enemy.x_size:
                    if (bullet.b_x + self.bullet.x_size) >= enemy.e_x:
                        if (enemy.e_y <= bullet.b_y <= (enemy.e_y + enemy.y_size) or enemy.e_y <= (
                                bullet.b_y + self.bullet.y_size) <= (enemy.e_y + enemy.y_size)):
                            bullet.deleteLater()
                            self.bullets.remove(bullet)
                            enemy.HP_E -= 1
                            if enemy.HP_E <= 0:
                                self.update_score()  # Обновление счета
                                enemy.deleteLater()
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

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    #     if self.game_started == 1:
    #
    #         painter.fillRect(0, 0, self.fullW, self.fullH,
    #                          QColor(153, 255, 153))  # Очищаем окно, закрашивая его зеленым
    #         painter.fillRect(0, 0, ceil(self.fullW * 0.2), self.fullH, QColor(150, 140, 130))
    #         painter.fillRect(0, ceil(self.fullH * 0.8), self.fullW, self.fullH, QColor(100, 100, 100))
    #
    #         # painter.drawImage(QRect(self.player1.x, self.player1.y, X_SIZE_PLAYER, Y_SIZE_PLAYER), QImage('player.png'))
    #         # painter.drawImage(QRect(self.player2.x, self.player2.y, X_SIZE_PLAYER, Y_SIZE_PLAYER), QImage('player.png'))
    #         painter.fillRect(ceil(self.fullW*0.14), self.player1.y, self.player1.x_size, self.player1.y_size,
    #                          QColor('skyblue'))
    #         if self.mode == 1: painter.fillRect(self.player2.x, self.player2.y, self.player2.x_size,
    #                                             self.player2.y_size, QColor('green'))
    #
    #         for bullet in self.bullets:
    #             # painter.drawImage(QRect(bullet.b_x, bullet.b_y, X_SIZE_BULLET, Y_SIZE_BULLET), QImage('bullet.png'))
    #             painter.fillRect(bullet.b_x, bullet.b_y, self.bullet.x_size, self.bullet.y_size, QColor(100, 100, 100))
    #
    #         for enemy in self.enemies:
    #             # painter.drawImage(QRect(enemy.x, enemy.y, X_SIZE_ENEMY, Y_SIZE_ENEMY), QImage('enemy.png'))
    #             # painter.fillRect(enemy.x, enemy.y, enemy.x_size, enemy.y_size, QColor(255, 255, 255))
    #             s=0
    #
    #         for i in range(self.player1.HP_P):
    #             # painter.drawImage(QRect(40+i*30, H + 12, X_SIZE_PLAYER_HP, X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))
    #             painter.fillRect(ceil(self.fullW * 0.05) + i * (ceil(self.fullW*0.01) + 2), ceil(self.fullH * 0.82),
    #                              ceil(self.fullW*0.01), ceil(self.fullW*0.03), QColor(200, 100, 100))
    #         # for i in range(self.player2.HP_P):
    #         #     painter.drawImage(QRect(30 + X_SIZE_PLAYER_TXT + X_SIZE_PLAYER_HP*self.player2.HP_P + 33 + i * 30, H + 12, X_SIZE_PLAYER_HP, X_SIZE_PLAYER_HP), QImage('hardcore-heart.png'))
    #
    #     else:
    #         painter.fillRect(0, 0, self.fullW, self.fullH, QColor(123, 123, 123))



# W = 1539-200
# H = 793-200
# X_SIZE_PLAYER_TXT = 50
X_INFO_BAR = 200

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_window = GameWindow()
    game_window.show()
    sys.exit(app.exec())
