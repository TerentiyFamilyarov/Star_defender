import sys
import random
from math import cos, sin, pi, sqrt

from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QFont, QPen, QBrush, QColor
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QWidget, QPushButton, QLabel, QStackedWidget, \
    QSlider, QGraphicsRectItem, QGraphicsProxyWidget
from numpy import arcsin


class Scene(QGraphicsScene):
    def __init__(self, view):
        super().__init__()
        self.first_slider_value = 100
        self.setSceneRect(0, 0, 800, 600)  # 16:9 - 960:540
        self.addRect(QRectF(0,0,self.width(),self.height()),QPen(Qt.PenStyle.NoPen),QBrush(QColor('green')))
        self.view = view
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_scene)
        # self.stack_widget = QStackedWidget()
        # stak_widget = self.addWidget(self.stack_widget)
        # stak_widget.setZValue(3) # [eqyZ t,fyyfz
        # self.stack_widget.setGeometry(0, 0, 800, 600)

        # self.main_menu = self.create_main_menu(self, self.view)
        # self.stack_widget.addWidget(self.main_menu)  # Index 0
        # self.settings_menu = self.create_settings_menu(self, self.view)
        # self.stack_widget.addWidget(self.settings_menu)  # Index 1

        # self.stack_widget.setCurrentWidget(self.main_menu)

        self.player = QGraphicsRectItem()
        self.player.setPen(QPen(Qt.PenStyle.NoPen))
        self.player.setBrush(QBrush(QColor('black')))
        self.addItem(self.player)
        self.player.setZValue(1)
        self.player.move_l = 0
        self.player.move_r = 0
        self.player.move_u = 0
        self.player.move_d = 0
        self.player.speed_l = 0
        self.player.speed_r = 0
        self.player.speed_u = 0
        self.player.speed_d = 0
        self.player.step = 5
        self.player.size_x = 30
        self.player.size_y = 30
        self.player.setRect(0, 0, self.player.size_x, self.player.size_y)
        self.player.hp = 5
        self.player.hit_delay = 0
        self.player.damage = 1
        self.player.speed_shoot = 0
        def move(player):
            if player.move_l == 1:
                player.speed_l = -player.step
            else:
                player.speed_l = 0
            if player.move_r == 1:
                player.speed_r = player.step
            else:
                player.speed_r = 0
            if player.move_u == 1:
                player.speed_u = -player.step
            else:
                player.speed_u = 0
            if player.move_d == 1:
                player.speed_d = player.step
            else:
                player.speed_d = 0

            player.moveBy(player.speed_l+player.speed_r, player.speed_u+player.speed_d)
        self.player.move = move

        self.enemy_timer = QTimer()
        self.enemy_timer.timeout.connect(self.enemy_timer.stop)

    class Enemies(QGraphicsRectItem):
        array_enemies = []
        timer = QTimer()
        timer.timeout.connect(timer.stop)
        def __init__(self):
            super().__init__()
            self.setPen(QPen(Qt.PenStyle.NoPen))
            self.timer = QTimer()
            self.move_l = 0
            self.move_r = 0
            self.move_u = 0
            self.move_d = 0
            # self.shoot = 0
            self.speed_x = 0
            self.speed_y = 0
            self.angle = 0
            self.step = 0
            self.size_x = 0
            self.size_y = 0
            self.window_x = 0
            self.window_y = 0
            self.hp = 0
            self.hit_delay = 0
            self.damage = 0
            self.speed_shoot = 0
            self.move = None


        def default_enemy(self,scene):
            enemy = self
            enemy.size_x, enemy.size_y = 40,40
            enemy.step = 0.3
            enemy.damage = 0
            enemy.hp = 1
            enemy.setBrush(QBrush(QColor('red')))
            enemy.setRect(0, 0, enemy.size_x, enemy.size_y)
            # x1 = random.randint(int(scene.width() * 1.2), int(scene.boundingField().width() - enemy.size_x - 1))
            # x2 = random.randint(-int(scene.boundingField().width() + 1), int(scene.width()) - int(scene.width() * 1.2))
            y = random.randint(0, int(scene.height() - enemy.size_y))
            x1 = random.randint(0,int(scene.width()))
            x2 = 0
            enemy.setPos(random.choice((x1, x2)), y)
            # enemy.direction = random.choice((-1, 1))

            def move():
                player_x = scene.player.x() + scene.player.size_x//2
                player_y = scene.player.y() + scene.player.size_y//2
                enemy_x = enemy.x() + enemy.size_x//2
                enemy_y = enemy.y() + enemy.size_y//2
                vertical = abs(player_y - enemy_y)
                horizontal = abs(enemy_x - player_x)
                third = sqrt((vertical ** 2) + (horizontal ** 2))
                if enemy_x > player_x:
                    if enemy_y < player_y:
                        angle = 90 - (arcsin(horizontal / third) * (180 / pi))
                        enemy.angle = angle + 180
                    if enemy_y > player_y:
                        angle = (arcsin(horizontal / third) * (180 / pi))
                        enemy.angle = angle + 90
                if enemy_x < player_x:
                    if enemy_y < player_y:
                        angle = (arcsin(horizontal / third) * (180 / pi))
                        enemy.angle = angle + 270
                    if enemy_y > player_y:
                        angle = 90 - (arcsin(horizontal / third) * (180 / pi))
                        enemy.angle = angle + 0

                print(horizontal/third,'    ', arcsin(horizontal/third),'   ', 90 - (arcsin(horizontal/third)*(180/pi)))


                enemy.speed_x = cos(enemy.angle * (pi / 180)) * enemy.step
                enemy.speed_y = -sin(enemy.angle * (pi / 180)) * enemy.step
                enemy.moveBy(enemy.speed_x, enemy.speed_y)
            enemy.move = move
            scene.addItem(enemy)
            self.array_enemies.append(enemy)
            return enemy


    def stop_game(self,b:bool):
        if b is True and self.timer.isActive() is True:
            self.timer.stop()
        if b is False and self.timer.isActive() is False:
            self.timer.start(10)

    def check_collision(self,player,array_enemies,array_bullets=None):
        player_rect = QRectF(player.x(),player.y(),player.size_x,player.size_y)
        player_x = player.x() + player.size_x / 2
        player_y = player.y() + player.size_y / 2

        for enemy in array_enemies:
            enemy_rect = QRectF(enemy.x(),enemy.y(),enemy.size_x,enemy.size_y)
            enemy_x = enemy.x() + enemy.size_x / 2
            enemy_y = enemy.y() + enemy.size_y / 2
            if player_rect.intersects(enemy_rect):
                penetrat_line_plaeyr = max((player_x+player.size_x/2),) # хочу сделать чтобы были точки допустим 8 на равном рассотянии и их сравнение, берем маскимальное
                movent_x = (enemy.speed_x/2) + abs((player_x+player.size_x/2)-(enemy_x+enemy.size_x/2))
                movent_y = (enemy.speed_y/2) + abs((player_y+player.size_x/2)-(enemy_y+enemy.size_y/2))

                player.moveBy(movent_x,0)
                enemy.moveBy(-enemy.speed_x,-enemy.speed_y)




    def update_scene(self):
        self.player.move(self.player)
        if self.enemy_timer.isActive() is False:
            enemy = self.Enemies().default_enemy(self)
            self.enemy_timer.start(3000)

        for enemy in self.Enemies.array_enemies:
            enemy.move()


        self.check_collision(self.player,self.Enemies.array_enemies)

        self.update()

    def keyPressEvent(self, event):
        if event.text() in ['W','w']:
            self.player.move_u = 1
        if event.text() in ['A','a']:
            self.player.move_l = 1
        if event.text() in ['D','d']:
            self.player.move_r = 1
        if event.text() in ['S','s']:
            self.player.move_d = 1

    def keyReleaseEvent(self, event):
        if event.text() in ['W','w']:
            self.player.move_u = 0
        if event.text() in ['A','a']:
            self.player.move_l = 0
        if event.text() in ['D','d']:
            self.player.move_r = 0
        if event.text() in ['S','s']:
            self.player.move_d = 0


    # def create_main_menu(self, scene, view):
    #     widget = QWidget()
    #     widget.setGeometry(0, 0, 800, 600)
    #     widget.setStyleSheet('background-color: rgb(70, 70, 70)')
    #
    #     main_text = QLabel('Magic Survival', widget)
    #     main_text.setGeometry(200, 100, 200, 30)
    #     main_text.setFont(QFont('Serif', 24))
    #     main_text.setStyleSheet('color: rgb(200, 200, 200)')
    #
    #     start_button = QPushButton('start', widget)
    #     start_button.setGeometry(300, 400, 200, 100)
    #     start_button.clicked.connect(lambda: self.stack_widget.setCurrentWidget(self.settings_menu))
    #
    #     exit_button = QPushButton('exit', widget)
    #     exit_button.setGeometry(300, 500, 200, 100)
    #     exit_button.clicked.connect(lambda: view.close())
    #     scene.addWidget(widget)
    #     return widget
    #
    # def create_settings_menu(self, scene, view):
    #     widget = QWidget()
    #     widget.setGeometry(0, 0, 800, 600)
    #     widget.setStyleSheet('background-color: rgb(70, 70, 70)')
    #
    #     main_text = QLabel('settings', widget)
    #     main_text.setGeometry(200, 100, 200, 30)
    #     main_text.setFont(QFont('serif', 20))
    #     main_text.setStyleSheet('color: rgb(200, 200, 200)')
    #
    #     slider_text = QLabel('Value: 100', widget)
    #     slider_text.setGeometry(250, 150, 200, 30)
    #     slider_text.setFont(QFont('serif', 20))
    #     slider_text.setStyleSheet('color: rgb(150, 230, 150)')
    #
    #     def update():
    #         slider_text.setText(f'value: {slider.value()}')
    #         self.first_slider_value = slider.value()
    #         print(self.first_slider_value)
    #
    #     slider = QSlider(Qt.Orientation.Horizontal, widget)
    #     slider.setGeometry(400, 240, 290, 30)
    #     slider.setRange(10, 300)
    #     # slider.setMinimum(10)
    #     # slider.setMaximum(300)
    #     slider.setValue(100)
    #     slider.setSingleStep(10)
    #     slider.setPageStep(20)
    #     print(slider.value())
    #     self.first_slider_value = slider.value()  # добавилось выше
    #     slider.setTickPosition(QSlider.TickPosition.TicksBelow)
    #     slider.setTickInterval(10)
    #     # slider.valueChanged.connect(lambda: slider_text.setText(f'Value: {slider.value()}'))
    #     slider.valueChanged.connect(update)
    #
    #     main_menu_button = QPushButton('qwerty', widget)
    #     main_menu_button.setGeometry(300, 500, 200, 100)
    #     main_menu_button.clicked.connect(lambda: self.stack_widget.setCurrentWidget(self.main_menu))
    #
    #     start_game_button = QPushButton('start game', widget)
    #     start_game_button.setGeometry(100, 400, 200, 100)
    #     def start_game():
    #         self.stack_widget.hide()
    #     start_game_button.clicked.connect(start_game)
    #     scene.addWidget(widget)
    #     return widget


class View(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        # self.setMaximumSize(1600, 900)
        self.setGeometry(0, 0, 1120, 600)
        stack_widget = QStackedWidget()
        stack_widget.setGeometry(0,0,800,600)
        stack_widget.setStyleSheet('background-color: rgba(255,0,0,100)')
        # stack_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.scene = Scene(self)
        self.setScene(self.scene)
        main_menu = self.create_main_menu(self,stack_widget)
        stack_widget.addWidget(main_menu)
        settings_menu = self.create_settings_menu(self,stack_widget)
        stack_widget.addWidget(settings_menu)
        proxy_wid = self.scene.addWidget(stack_widget)
        proxy_wid.setZValue(1)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        self.fitInView(QRectF(0, 0, 800, 600), Qt.AspectRatioMode.KeepAspectRatio)

    def create_main_menu(self, view,stack_widget):
        widget = QWidget()
        widget.setGeometry(0, 0, 800, 600)
        widget.setStyleSheet('background-color: rgb(70, 70, 70)')

        main_text = QLabel('Magic Survival', widget)
        main_text.setGeometry(200, 100, 200, 30)
        main_text.setFont(QFont('Serif', 24))
        main_text.setStyleSheet('color: rgb(200, 200, 200)')

        start_button = QPushButton('start', widget)
        start_button.setGeometry(300, 400, 200, 100)
        start_button.clicked.connect(lambda: stack_widget.setCurrentIndex(1))

        exit_button = QPushButton('exit', widget)
        exit_button.setGeometry(300, 500, 200, 100)
        exit_button.clicked.connect(lambda: view.close())
        return widget

    def create_settings_menu(self, view,stack_widget):
        widget = QWidget()
        widget.setGeometry(0, 0, 800, 600)
        widget.setStyleSheet('background-color: rgb(70, 70, 70)')

        main_text = QLabel('settings', widget)
        main_text.setGeometry(200, 100, 200, 30)
        main_text.setFont(QFont('serif', 20))
        main_text.setStyleSheet('color: rgb(200, 200, 200)')

        slider_text = QLabel('Value: 100', widget)
        slider_text.setGeometry(250, 150, 200, 30)
        slider_text.setFont(QFont('serif', 20))
        slider_text.setStyleSheet('color: rgb(150, 230, 150)')

        def update():
            slider_text.setText(f'value: {slider.value()}')
            self.first_slider_value = slider.value()
            print(self.first_slider_value)

        slider = QSlider(Qt.Orientation.Horizontal, widget)
        slider.setGeometry(400, 240, 290, 30)
        slider.setRange(10, 300)
        # slider.setMinimum(10)
        # slider.setMaximum(300)
        slider.setValue(100)
        slider.setSingleStep(10)
        slider.setPageStep(20)
        print(slider.value())
        self.first_slider_value = slider.value()  # добавилось выше
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(10)
        # slider.valueChanged.connect(lambda: slider_text.setText(f'Value: {slider.value()}'))
        slider.valueChanged.connect(update)

        main_menu_button = QPushButton('qwerty', widget)
        main_menu_button.setGeometry(300, 500, 200, 100)
        main_menu_button.clicked.connect(lambda: stack_widget.setCurrentIndex(0))

        start_game_button = QPushButton('start game', widget)
        start_game_button.setGeometry(100, 400, 200, 100)
        def start_game():
            stack_widget.hide()
            view.scene.stop_game(False)
        start_game_button.clicked.connect(start_game)
        return widget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #
    menu = View()
    menu.show()
    sys.exit(app.exec())