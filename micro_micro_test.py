import sys
from math import ceil
import random

from PyQt6.QtCore import QPoint, QSize, QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QBrush
from PyQt6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsView, QGraphicsScene


class StartGame(QGraphicsScene):
    def __init__(self, menu, game_begin=False):
        super().__init__()
        self.game_begin = game_begin
        self.menu = menu
        self.view = QGraphicsView()
        self.view.setScene(self)
        # self.view.setBackgroundBrush(QColor(100,100,100))
        self.view.setMinimumSize(1120,600)
        self.view.show()
        # self.setSceneRect(0, 0, self.width(), self.height())
        self.setSceneRect(0,0,1120,600)
        self.addRect(self.boundingRect(),QColor('black'),QBrush(QColor('black')))


        self.previous_size = QSize()

        self.count_restart_sec = 3

        self.mode = 0

        self.sec = -1
        self.min = 0

        self.create_player2()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScene)
        self.timer.start(10)
        self.enemy_timer = QTimer(self)
        self.bullet_timer1 = QTimer(self)


        # players = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.players = [
            ('Default',      3,  1,      10,   25,        370,         45,     45,     QColor(0, 0, 255)),
            ('IFeelPain',    1,  0.5,    16,   40,        290,         35,     35,     QColor(200, 150, 0)),
            ('UPower',       5,  2,      7,    15,        420,         65,     65,     QColor(100, 255, 255))
        ]
        # players = [ (name, hp, damage, step, soap_koef, speed_shoot, size_x, size_y, color) ]
        self.enemies = [
            ('Default',      3,  1,      1,    0,         0,           65,     65,     QColor(255, 0, 0)),
            ('Tiny',         1,  1,      3,    0,         0,           35,     35,     QColor(255, 111, 0)),
            ('Fat',          5,  1,      0.5,  0,         0,           85,     85,     QColor(255, 111, 111)),
        ]



        self.view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        # self.view.scale(0.4, 0.4)

    def boundingRect(self):
        # return QRectF(-100, -100, (self.scene.width() + 200), (self.scene.height() + 200))
        return QRectF(0,0,self.width(),self.height())

    def create_player2(self):
        self.player2 = self.addRect(QRectF(0, 0, 45, 45), QColor('green'), QBrush(QColor('green')))
        self.player2.move_direction_L = 0
        self.player2.move_direction_R = 0
        self.player2.move_direction_U = 0
        self.player2.move_direction_D = 0
        self.player2.shoot = 0
        self.player2.speed_l = 0
        self.player2.speed_r = 0
        self.player2.speed_u = 0
        self.player2.speed_d = 0
        self.player2.step = 10
        self.player2.soap_koef = 25
        self.player2.size_x = 45
        self.player2.size_y = 45
        self.player2.window_x = self.width()
        self.player2.window_y = self.height()
        self.timer_player = QTimer(self)

    def new_move(self,obj,timer, move=1, soap_move=1, window_borders=1):
        if soap_move == 1:
            if timer.isActive() is False:
                if obj.speed_l < obj.step * 0.2 and obj.move_direction_L == 1:
                    obj.speed_l = obj.step * 0.2
                elif obj.speed_l < obj.step and obj.move_direction_L == 1:
                    obj.speed_l += 0.5
                elif obj.move_direction_L == 0 and obj.speed_l > 0:
                    obj.speed_l -= 0.5
                elif obj.speed_l < 0:
                    obj.speed_l = 0

                if obj.speed_r < obj.step * 0.2 and obj.move_direction_R == 1:
                    obj.speed_r = obj.step * 0.2
                elif obj.speed_r < obj.step and obj.move_direction_R == 1:
                    obj.speed_r += 0.5
                elif obj.move_direction_R == 0 and obj.speed_r > 0:
                    obj.speed_r -= 0.5
                elif obj.speed_r < 0:
                    obj.speed_r = 0

                if obj.speed_u < obj.step * 0.2 and obj.move_direction_U == 1:
                    obj.speed_u = obj.step * 0.2
                elif obj.speed_u < obj.step and obj.move_direction_U == 1:
                    obj.speed_u += 0.5
                elif obj.move_direction_U == 0 and obj.speed_u > 0:
                    obj.speed_u -= 0.5
                elif obj.speed_u < 0:
                    obj.speed_u = 0

                if obj.speed_d < obj.step * 0.2 and obj.move_direction_D == 1:
                    obj.speed_d = obj.step * 0.2
                elif obj.speed_d < obj.step and obj.move_direction_D == 1:
                    obj.speed_d += 0.5
                elif obj.move_direction_D == 0 and obj.speed_d > 0:
                    obj.speed_d -= 0.5
                elif obj.speed_d < 0:
                    obj.speed_d = 0


                timer.timeout.connect(timer.stop)
                timer.start(int(obj.soap_koef))
        else:
            if obj.move_direction_L == 1:
                obj.speed_l = obj.step
            elif obj.move_direction_L == 0:
                    obj.speed_l = 0

            if obj.move_direction_R == 1:
                obj.speed_r = obj.step
            elif obj.move_direction_R == 0:
                    obj.speed_r = 0

            if obj.move_direction_U == 1:
                obj.speed_u = obj.step
            elif obj.move_direction_U == 0:
                obj.speed_u = 0

            if obj.move_direction_D == 1:
                obj.speed_d = obj.step
            elif obj.move_direction_D == 0:
                    obj.speed_d = 0

        if window_borders == 1:
            if obj.x() + obj.speed_l < 0:
                obj.setX(0)
                obj.speed_l = 0
            else:
                obj.moveBy(-obj.speed_l,0)

            if obj.x() + obj.speed_r + obj.size_x > obj.window_x:
                obj.setX(obj.window_x - obj.size_x)
                obj.speed_r = 0
            else:
                obj.moveBy(obj.speed_r,0)

            if obj.y() + obj.speed_u < 0:
                obj.setY(0)
                obj.speed_u = 0
            else:
                obj.moveBy(0, -obj.speed_u)

            if obj.y() + obj.speed_d + obj.size_y > obj.window_y:
                obj.setY(obj.window_y - obj.size_y)
                obj.speed_d = 0
            else:
                obj.moveBy(0, obj.speed_d)


        else:
            obj.moveBy(-obj.speed_l + obj.speed_r,-obj.speed_u + obj.speed_d)


    # def create_obj(self,cd,timer,array_objs,pos,hp,damage,step,speed_shoot,x_size,y_size,color):
    #     if timer.isActive() is False:
    #         obj = MovingObject(pos[0], pos[1], hp, damage, step,  speed_shoot,
    #                                     x_size, y_size, self.width(), self.height())
    #         obj.set_default()
    #         obj.draw_color = color
    #         obj.setBrush(QColor(color))
    #         array_objs.append(obj)
    #         timer.start(cd)
    #         timer.timeout.connect(timer.stop)
    #         return obj

    # def check_collision(self):
    #     # if self.player1.HP_O <= 0:
    #         # self.menu.stackWidget.setCurrentWidget(self.menu.game_over_page)
    #     # Проверяем столкновение пуль с врагами
    #     for enemy in self.array_enemies:
    #         if self.player1.boundingRect().intersects(enemy.boundingRect()):
    #             if self.player1.x() + self.player1.x_size // 2 < enemy.x():
    #                 self.player1.l_speed = self.player1.step_x * 1
    #                 self.player1.r_speed = 0
    #             elif self.player1.x() + self.player1.x_size // 2 > enemy.x() + enemy.x_size:
    #                 self.player1.r_speed = self.player1.step_x * 1
    #                 self.player1.l_speed = 0
    #             elif self.player1.y() + self.player1.y_size // 2 < enemy.y():  # Отталкивание игрока от врага
    #                 self.player1.u_speed = self.player1.step_y * 1
    #                 self.player1.d_speed = 0
    #             elif self.player1.y() + self.player1.y_size // 2 > enemy.y() + enemy.y_size:
    #                 self.player1.d_speed = self.player1.step_y * 1
    #                 self.player1.u_speed = 0
    #
    #         if enemy.x() <= -enemy.x_size:
    #             self.player1.HP_O -= enemy.damage  # Уменьшение здоровья игрока
    #             self.array_enemies.remove(enemy)
    #             self.removeItem(enemy)
    #             continue
    #         if self.boundingRect().contains(enemy.boundingRect()) is False:
    #             self.array_enemies.remove(enemy)
    #             self.removeItem(enemy)
    #         for bullet in self.array_bullets:
    #             if self.boundingRect().contains(bullet.boundingRect()) is False:
    #                 self.array_bullets.remove(bullet)
    #                 self.removeItem(bullet)
    #                 continue
    #             if enemy.x() <= self.width() - (enemy.x_size // 2):
    #                 if enemy.boundingRect().intersects(bullet.boundingRect()):
    #                     self.array_bullets.remove(bullet)
    #                     self.removeItem(bullet)
    #                     enemy.HP_O -= (self.bullet.damage * self.player1.damage)
    #                     if enemy.HP_O <= 0:
    #                         self.array_enemies.remove(enemy)
    #                         self.removeItem(enemy)

    def updateScene(self):
        # self.restart_timer_txt.setText(f'{self.count_restart_sec}')
        # if self.restart_timer.isActive() is False:
        #     if self.count_restart_sec > 1:
        #         self.restart_timer.start(1000)
        #         self.count_restart_sec -= 1

        # if self.menu.stackWidget.currentWidget() == self and self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
            # if self.sec == 3 or self.sec % 10 == 0 and self.sec > 0:
            #     self.menu.stackWidget.setCurrentWidget(self.menu.choose_card_page)  # Костыль, переделай
            #     self.menu.choose_card_page.randomize_cards(self)
            #
            #     self.sec += 1

            # if len(self.menu.stars) < 100:
            #     randomint = random.randint(0, 101)
            #     if randomint <= 4:
            #         self.menu.create_star(1)
            # for star in self.menu.stars:
            #     star.move_direction_L = 1
            #     # if star.max_step_x < star.primary_step*1.5:
            #     #     star.step_x += 1
            #     star.new_move(1, 0, 0)
            #     if star.x() <= -star.x_size:
            #         self.menu.reborn_star(star)

            # if self.player1.shoot == 1:
            #     x_size = 20
            #     y_size = 5
            #     if self.bullet_timer1.isActive() is False:
            #         bullet = self.create_obj(int(self.player1.speed_shoot),self.bullet_timer1,self.array_bullets,
            #                         (ceil(self.player1.x() + (self.player1.x_size*self.player1.direction) +
            #                               (x_size*(self.player1.direction-1))),
            #                               (ceil(self.player1.y() + self.player1.y_size // 2) - self.bullet.y_size // 2)),
            #                         1, 1, 13, 0, x_size, y_size, QColor(0, 255, 0))
            #         if self.player1.direction == 1:
            #             bullet.move_direction_R = 1
            #             bullet.move_direction_L = 0  # Почему то не изчезают пули --> они не пропадают тк врагов нет
            #         else:
            #             bullet.move_direction_L = 1
            #             bullet.move_direction_R = 0
            #         self.addItem(bullet)
            #
            # enemy = self.create_obj(2000, self.enemy_timer, self.array_enemies,
            #                 (self.width(), random.randint(0, int(self.height()*0.8)-self.enemies[0][7])),
            #                 self.enemies[0][1], self.enemies[0][2], self.enemies[0][3], self.enemies[0][5],
            #                 self.enemies[0][6], self.enemies[0][7], self.enemies[0][8])
            # self.addItem(enemy)
            # self.player1.new_move(1,1,1)
        self.new_move(self.player2,self.timer_player,1,1,1)
            # for bullet in self.array_bullets:
            #     bullet.new_move(1, 0, 0)
            # for enemy in self.array_enemies:
            #     enemy.move_direction_L = 1
            #     enemy.new_move(1, 0, 0)
            # self.check_collision()
        # else:
            # self.player1.new_move(0)
        # if self.isActiveWindow() is False and self.menu.stackWidget.currentWidget() == self:
        #     self.menu.stackWidget.setCurrentWidget(self.menu.pause_page)
        self.update()



    def keyPressEvent(self, event):
        # if self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
            if event.text() in ['Ц', 'ц', 'W', 'w']:
                self.player2.move_direction_U = 1

            if event.text() in ['Ф', 'ф', 'A', 'a']:
                    self.player2.move_direction_L = 1



            if event.text() in ['Ы', 'ы', 'S', 's']:
                self.player2.move_direction_D = 1


            elif event.text() in ['В', 'в', 'D', 'd']:
                    self.player2.move_direction_R = 1

            # if event.text() in ['C', 'c', 'С', 'с']:
            #     self.player1.shoot = 1
            # print(self.boundingRect().x(),'x ',self.boundingRect().y(),'y ',self.boundingRect().width(),'w ',self.boundingRect().height(),'h')

            # print('Scene ',self.width(), 'w ',self.height(), 'h')
            # print(self.player1.x(),'x ',self.player1.y(),'y ',self.player1.x_size,'w ',self.player1.y_size,'h')
            # scene_coords = QPoint(int(self.player1.x()),int(self.player1.y()))
            # view_coords = self.view.mapFromScene(self.player1.x(),self.player1.y())
            # global_coords = self.view.mapToGlobal(QPoint(0,0))
            # parent_coords = self.view.mapToParent(QPoint(0,0))
            # view_coords = self.view.mapToScene(scene_coords)
            # print('scene p ->',scene_coords)
            # print('view p ->',view_coords)
            # print('global p ->',global_coords)
            # print('parent p ->',parent_coords)
            # if event.key() == Qt.Key.Key_Escape:  # кнопку надо ограничить в свое нажатии, можно прям в меню ее нажать
            #     self.menu.stackWidget.setCurrentWidget(self.menu.pause_page)

    def keyReleaseEvent(self, event):
        if event.text() in ['Ц', 'ц', 'W', 'w']:
            self.player2.move_direction_U = 0

        elif event.text() in ['Ф', 'ф', 'A', 'a']:
            self.player2.move_direction_L = 0

        elif event.text() in ['Ы', 'ы', 'S', 's']:
            self.player2.move_direction_D = 0

        elif event.text() in ['В', 'в', 'D', 'd']:
            self.player2.move_direction_R = 0

        # if event.text() in ['C', 'c', 'С', 'с']:
        #     self.player1.shoot = 0



    # def paint(self, painter):
    #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    #     painter.fillRect(0, 0, self.width(), self.height(),
    #                      QColor(0,0,0))  # Очищаем окно, закрашивая его зеленым
    #     # for star in self.menu.stars:
    #     #     star.paint(painter)
    #
    #     painter.fillRect(0, ceil(self.height() * 0.8), self.width(), self.height(), QColor(100, 100, 100))
    #
    #     for i in range(int(self.player1.HP_O)):
    #         painter.fillRect(ceil(self.width() * 0.05) + i * (ceil(self.width() * 0.01) + 2),
    #                          ceil(self.height() * 0.82),
    #                          ceil(self.width() * 0.01), ceil(self.width() * 0.03), QColor(200, 100, 100))
    #     # self.player1.paint(painter)
    #     # for bullet in self.array_bullets:
    #     #     bullet.paint(painter)
    #     for enemy in self.array_enemies:
    #         enemy.paint(painter)
    #
    #     # if self.count_restart_sec <= 1 and self.restart_timer.isActive() is False:
    #     #     self.restart_timer_txt.hide()
    #     # else:
    #     #     self.restart_timer_txt.show()
    #     #     painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 0, 200))
    #
    # def paint_static(self):
    #     info_bar = QGraphicsRectItem(0,ceil(self.height() * 0.8),self.width(),self.height())
    #     info_bar.setBrush(QColor(100, 100, 100))
    #     self.addItem(info_bar)

# с помощью лебел можно сделать переход по словам, также модификации у обьектов должен быть как у карточек



if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_window = StartGame(None,True)
    # game_window.show()
    sys.exit(app.exec())