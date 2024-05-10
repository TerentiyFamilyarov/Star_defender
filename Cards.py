import random
import sys

from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QVBoxLayout

import Enemies


class Card(QWidget):
    def __init__(self,rect:QRect,style_name:QFont,style_desc:QFont):
        super().__init__()
        self.setGeometry(rect)
        self.setStyleSheet('background-color:rgba(200,255,200,255);border:none')

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


def card_snake_shoot(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Snake shoot')
    card.description.setText('asjhasdaskd lasdhlaksdj alsdhalskj halksdj lksda')
    def procedure():
        scene.bullet_type = 1
        scene.enemy_types.append(Enemies.ping_pong_enemy)
        array_cards.remove(card_snake_shoot)
        card.deleteLater()
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

def card_blessing(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Blessing')
    card.description.setText('askdfjh akjsh wjwhpo[o ;k;d d')
    def procedure():
        card.deleteLater()
        scene.player.hp +=1
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

def card_power(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Power up')
    card.description.setText('asd.mxcn ipwe n 1 ;ldkjf ')
    def procedure():
        card.deleteLater()
        scene.player.damage += 1
    card.button.clicked.connect(lambda: scene.show_card_page_new(False))
    card.button.clicked.connect(procedure)
    card.button.show()
    return card

array_cards = [
    card_snake_shoot,
    card_blessing,
    card_power
]