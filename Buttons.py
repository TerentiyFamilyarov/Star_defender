import sys
import random

from PyQt6.QtCore import QRectF, Qt, QTimer
from PyQt6.QtGui import QPixmap, QPen, QBrush, QColor, QImage
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QApplication, QGraphicsRectItem


class Scene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0,0,600,600)
        # сдесь пишешь всю логику игры
        # rect_with_size_like_bg = self.addRect(QRectF(0,0,self.width(),self.height()),QPen(Qt.PenStyle.NoPen),QBrush(QColor(100,100,100)))
        pixmap = self.addPixmap(QPixmap('Nik Saltykov.jpg'))
        pen = QPen(Qt.PenStyle.DashLine)
        pen.setColor(QColor('green'))
        pen.setWidthF(2)
        self.character = self.addRect(QRectF(100, 100, 40, 40), QPen(pen), QBrush(QColor(100, 100, 100)))
        self.character.move_l = 0
        self.character.move_r = 0
        self.character.move_u = 0
        self.character.move_d = 0
        self.Timer = QTimer()
        self.enemy_arr = []
        self.create_enemy(self, self.enemy_arr)
        self.Timer.timeout.connect(lambda: self.update_game(self.character, enemy_arr=self.enemy_arr))


        self.Timer.start(10)
        # если функция что-то, то так и пишешь, напирмер QBrush('он просит QColor()') значит пишешь QBrush(QColor()) и так далее

    def create_enemy(self, scene, arr):
        enemy = scene.addRect(QRectF(300, 300, 30, 30),QPen(QPen(Qt.PenStyle.NoPen)), QBrush(QColor(200, 40, 40)))
        arr.append(enemy)

    def update_game(self,chara:QGraphicsRectItem, enemy_arr):
        if chara.move_l == 1:
            chara.moveBy(-1,0)
        if chara.move_r == 1:
            chara.moveBy(1,0)
        if chara.move_u == 1:
            chara.moveBy(0,-1)
        if chara.move_d == 1:
            chara.moveBy(0,1)


        # self.create_enemy(self,enemy_arr)
        for enemy in enemy_arr:
            enemy.moveBy(random.randint(-5,5), random.randint(-5,5))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W:
            self.character.move_u = 1
        if event.key() == Qt.Key.Key_A:
            self.character.move_l = 1
        if event.key() == Qt.Key.Key_D:
            self.character.move_r = 1
        if event.key() == Qt.Key.Key_S:
            self.character.move_d = 1

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_W:
            self.character.move_u = 0
        if event.key() == Qt.Key.Key_A:
            self.character.move_l = 0
        if event.key() == Qt.Key.Key_D:
            self.character.move_r = 0
        if event.key() == Qt.Key.Key_S:
            self.character.move_d = 0
class View(QGraphicsView):
    def __init__(self,scene):
        super().__init__()

        self.setScene(scene)
        self.setMinimumSize(700,700)
        # чтобы небыло рекрусии в resize из-за fitinview нужно отключить полосы прокрутки
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # можно сделать Align
        # self.setAlignment(он просит aligment)
        # если чет хочешь сделать но не знаешь что то пишешь "Qt." это помогает почти во всех случаях
        # пишем Qt. ... и там само тебе предложит и ты по смыслу сможешь чте сделать
        # self.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # у view по дефолту есть границы
        self.setStyleSheet('border: 100px; background-image: url("Nik Saltykov.jpg");') # это применяет стили из CSS, если будет ошибка в нем то он отключится
        # self.setStyleSheet('хуйня: 10px;') # последний использованный StyleSheet будет активирован а остальные проигнорированны

        # есть у view разные хуйни типа scale
        # self.scale(0.5,0.5) # что бы сработало нужно убрать resize

    # def resizeEvent(self, event):
    # размеры QRectF влияют на масштабирование, обычно при размере меньше на 5 от размера сцены это масштабирование во всю view
    # по дефолту сцена по центру
    #     self.fitInView(QRectF(0,0,595,595),Qt.AspectRatioMode.KeepAspectRatio)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Scene()
    game_window = View(game)
    game_window.show()
    sys.exit(app.exec())
