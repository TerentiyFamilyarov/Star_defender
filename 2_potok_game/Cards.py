import random
import sys

from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QVBoxLayout

import Bullets
import Enemies


class Card(QWidget):
    def __init__(self,rect:QRect,style_name:QFont,style_desc:QFont):
        super().__init__()
        self.setGeometry(rect)
        self.setStyleSheet('background-color:rgba(100,100,100,255);border:none')

        self.name = QLabel(self)
        self.name.setGeometry(QRect(0,0,self.width(),int(self.height()*0.3)))
        self.name.setFixedWidth(self.width())
        # self.name.setText(name)
        self.name.setWordWrap(True)
        self.name.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.name.setFont(style_name)
        self.name.show()

        self.description = QLabel(self)
        self.description.setGeometry(QRect(0,int(self.height()*0.4),self.width(),self.height()))
        self.description.setFixedWidth(self.width())
        # self.description.setText(description)
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.description.setFont(style_desc)
        self.description.show()

        self.button = QPushButton(self)
        self.button.setGeometry(0,0,self.width(),self.height())
        self.button.setStyleSheet('''
        QPushButton{background-color:rgba(0,0,0,0);border:none}
        QPushButton:hover{background-color:rgba(255,255,255,100)}
        QPushButton:pressed{background-color:rgba(200,200,200,100)}
        ''')
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.show()



def card_blessing(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Blessing')
    card.description.setText('askdfjh akjsh wjwhpo[o ;k;d d')
    def procedure():
        scene.player.hp += 1
        scene.player.size_x = int(scene.player.size_x*1.1)
        scene.player.size_y = int(scene.player.size_y*1.1)
        scene.player.setRect(0,0,scene.player.size_x,scene.player.size_y)
        scene.player.step *= 0.2
        card.deleteLater()
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

def card_power(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Power up')
    card.description.setText('asd.mxcn ipwe n 1 ;ldkjf ')
    def procedure():
        scene.player.damage *= 1.1
        scene.player.step *= 1.2
        scene.player.size_x = int(scene.player.size_x*0.9)
        scene.player.size_y = int(scene.player.size_y*0.9)
        card.deleteLater()
        scene.player.setRect(0,0,scene.player.size_x,scene.player.size_y)
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

def card_washing(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('wash machine')
    card.description.setText('asd.mxcn ipwe n 1 ;ldkjf ')
    def procedure():
        scene.player.step *= 1.2
        scene.player.soap_koef *= 0.8
        card.deleteLater()
        scene.player.setRect(0,0,scene.player.size_x,scene.player.size_y)
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

def card_add_bullet(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Add bullet')
    card.description.setText('asd.mxcn ipwe c 1 ;ldkjf ')
    def procedure():
        # scene.player.triples_count += 1
        Bullets.bullet_count += 1
        scene.player.damage *= 0.9
        card.deleteLater()
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

def card_big_bullet(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Big bullet')
    card.description.setText('asd.mxcn ipwe bb 1 ;ldkjf ')
    def procedure():
        Bullets.size_koef *= 1.2
        Bullets.damage_koef *= 1.2
        Bullets.speed_koef *= 0.7
        Bullets.speed_shoot_koef *= 1.3
        Bullets.update_bullets_list()
        card.deleteLater()
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

def card_chaos_bullet_set(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Chaos set')
    card.description.setText('asd.mxcn ipwe bb 1 ;ldkjf ')
    def procedure():
        # scene.player.triples_count = 10
        Bullets.bullet_count = 5
        Bullets.first_arg_method = Bullets.bullet_count
        # scene.player.triples_degree = 90
        Bullets.bullet_degree = 60
        Bullets.second_arg_mothod = Bullets.bullet_degree
        Bullets.size_koef = 1
        Bullets.speed_koef = 1
        Bullets.damage_koef = 1
        Bullets.speed_shoot_koef = 1
        Bullets.update_bullets_list()
        scene.player.hp -= 2
        if scene.player.hp < 1:
            scene.player.hp = 1
        card.deleteLater()
        scene.player.current_bullet_type = Bullets.chaos_bullet
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

def card_navigation_bullet_set(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Navi set')
    card.description.setText('asd.mxcn ipwe bb 1 ;ldkjf ')
    def procedure():
        # scene.player.triples_count = 10
        Bullets.bullet_count = 1
        # Bullets.first_arg_method = Bullets.bullet_count
        # scene.player.triples_degree = 90
        Bullets.bullet_degree = 45
        # Bullets.second_arg_mothod = Bullets.bullet_degree
        Bullets.size_koef = 1
        Bullets.speed_koef = 1
        Bullets.damage_koef = 1
        Bullets.speed_shoot_koef = 1
        Bullets.update_bullets_list()
        scene.player.step *= 0.8
        card.deleteLater()
        scene.player.current_bullet_type = Bullets.navigation_bullet
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

def card_ultimate_bullet(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('Ultimate set')
    card.description.setText('asd.mxcn ipwe bb 1 ;ldkjf ')

    def procedure():
        Bullets.bullet_count -= 100
        # Bullets.first_arg_method = Bullets.bullet_count
        Bullets.size_koef *= 2
        Bullets.speed_koef *= 0.8
        Bullets.damage_koef *= 2
        Bullets.speed_shoot_koef *= 1000
        Bullets.update_bullets_list()
        scene.player.step *= 0.7
        card.deleteLater()
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

def card_army_bullet(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('army bullets')
    card.description.setText('asd.mxcn ipwe bb 1 ;ldkjf ')

    def procedure():
        Bullets.bullet_count += 5
        Bullets.bullet_degree += 5
        # Bullets.first_arg_method = Bullets.bullet_count
        Bullets.size_koef *= 0.9
        Bullets.speed_koef *= 1.2
        Bullets.damage_koef *= 0.9
        Bullets.speed_shoot_koef *= 0.9
        Bullets.update_bullets_list()
        scene.player.step *= 1.1
        card.deleteLater()
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

array_cards = [
    card_blessing,
    card_power,
    card_washing,
    card_add_bullet,
    card_big_bullet,
    card_chaos_bullet_set,
    card_navigation_bullet_set,
    card_ultimate_bullet,
    card_army_bullet
]