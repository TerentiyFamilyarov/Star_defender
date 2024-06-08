import random
import sys

from PyQt6.QtCore import QRect, Qt, QTimer
from PyQt6.QtGui import QFont, QCursor, QPalette, QColor
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QVBoxLayout

import Bullets
import Enemies


timer = QTimer()
timer.timeout.connect(timer.stop)

class Card(QWidget):
    def __init__(self,rect:QRect,style_name:QFont,style_desc:QFont):
        super().__init__()
        self.setGeometry(rect)
        self.setStyleSheet('background-color:rgba(100,100,100,255);border:0')
        background = QLabel(self)
        background.setGeometry(0,0,self.width(),self.height())
        background.setStyleSheet('background-color:rgba(100,100,100,255);border:0')

        self.name = QLabel(self)
        self.name.move(0,0)
        self.name.setFixedWidth(self.width())
        self.name.setStyleSheet('background-color:transparent')
        self.name.setWordWrap(True)
        self.name.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.name.setFont(style_name)
        self.name.show()

        self.description = QLabel(self)
        self.description.setGeometry(QRect(0,int(self.name.height())-1,self.width(),self.height()))
        self.description.setStyleSheet('background-color:transparent')
        self.description.setFixedWidth(self.width())
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description.setFont(style_desc)
        self.description.show()

        self.button = QPushButton(self)
        self.button.setGeometry(0,0,self.width(),self.height())
        self.button.setStyleSheet('''
        QPushButton{background-color:rgba(0,0,0,0);border:none}
        QPushButton:hover{background-color:rgba(100,100,100,70)}
        QPushButton:pressed{background-color:rgba(100,100,100,70)}
        ''')
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.show()



def card_blessing(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Blessing')
    card.description.setText('''
    Starship health points increases by 1. Also starship size +10%. Maximum starship size equals 100. But starship speed -80%.
    Enemy health points, speed and damage +20%. Enemy ship types can be added.
    ''')
    def on_click():
        scene.player.hp += 1
        scene.player.size_x = int(scene.player.size_x*1.1)
        scene.player.size_y = int(scene.player.size_y*1.1)
        if scene.player.size_x > 100:
            scene.player.size_x = 100
            scene.player.size_y = 100
        scene.player.update_size(scene.player.size_x,scene.player.size_y)
        scene.player.step *= 0.2
        Enemies.difficult_koef *= 1.2
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_power(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Power up')
    card.description.setText('''
    Starship damage +10%. Starship speed +20%. But starship size -10%. Minimum starship size equals 15.
    Enemy health points, speed and damage increases by 15%. Enemy ship types can be added.
    ''')
    def on_click():
        scene.player.damage *= 1.1
        scene.player.step *= 1.2
        scene.player.size_x = int(scene.player.size_x*0.9)
        scene.player.size_y = int(scene.player.size_y*0.9)
        if scene.player.size_x < 15:
            scene.player.size_x = 15
            scene.player.size_y = 15
        scene.player.update_size(scene.player.size_x,scene.player.size_y)
        Enemies.difficult_koef *= 1.15
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.player.update_size(scene.player.size_x,scene.player.size_y)
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)

    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_washing(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Washing ship')
    card.description.setText('''
    Starship speed +20%. Starship breaking speed +20%. But starship damage -1%.
    Enemy health points, speed and damage increases by 13%. Enemy ship types can be added.
    ''')
    def on_click():
        scene.player.step *= 1.2
        scene.player.soap_koef *= 0.8
        scene.player.damage *= 0.99
        Enemies.difficult_koef *= 1.13
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_add_bullet(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Add bullet')
    card.description.setText('''
    Starship bullets count increases by 1. But starship damage -10%.
    Enemy health points, speed and damage increases by 11%. Enemy ship types can be added.
    ''')
    def on_click():
        Bullets.bullet_count += 1
        Bullets.first_arg_method = Bullets.bullet_count
        scene.player.damage *= 0.9
        Enemies.difficult_koef *= 1.11
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_big_bullet(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Big bullet')
    card.description.setText('''
    Bullet size +20%. Maximum bullet size: normal size + 4900%. Bullet damage +20%. But bullet speed -10%. Shoot cooldown +30%
    Enemy health points, speed and damage increases by 14%. Enemy ship types can be added.
    ''')
    def on_click():
        Bullets.scale_x_koef *= 1.2
        if int(Bullets.scale_x_koef) > 50:
            Bullets.scale_x_koef = 50
        Bullets.scale_y_koef *= 1.2
        if int(Bullets.scale_y_koef) > 50:
            Bullets.scale_y_koef = 50
        Bullets.damage_koef *= 1.2
        Bullets.speed_koef *= 0.7
        Bullets.speed_shoot_koef *= 1.3
        Bullets.update_bullets_list()
        Enemies.difficult_koef *= 1.14
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_chaos_bullet_set(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Chaos set')
    card.description.setText('''
    Sets chaos bullet type:
    bullet count equals 5, bullet direction spread equals 2*60 degrees, bullet width, height, speed, damage, shoot cooldown coefficients equals 1. Starship health points decreates by 2, but minimum health equals 1.
    Enemy health points, speed and damage increases by 25%. Enemy ship types can be added.
    ''')
    def on_click():
        Bullets.bullet_count = 5
        Bullets.first_arg_method = Bullets.bullet_count
        Bullets.bullet_degree = 60
        Bullets.second_arg_mothod = Bullets.bullet_degree
        Bullets.scale_x_koef = 1
        Bullets.scale_y_koef = 1
        Bullets.speed_koef = 1
        Bullets.damage_koef = 1
        Bullets.speed_shoot_koef = 1
        Bullets.update_bullets_list()
        scene.player.hp -= 2
        if scene.player.hp < 1:
            scene.player.hp = 1
        Enemies.difficult_koef *= 1.25
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.player.current_bullet_type = Bullets.chaos_bullet
        scene.keys_txt.setPlainText('W,A,S,D - movement; C - shooting; F11 - toggle full screen')
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)

    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_navigation_bullet_set(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Navigation set')
    card.description.setText('''
    Sets navigation bullet type:
    you can manipulate starship bullets on up, down keys.
    Bullet count equals 5, bullet direction spread equals 2*30 degrees, bullet width, height, speed, damage, shoot cooldown coefficients equals 1. Starship speed -20%.
    Enemy health points, speed and damage increases by 30%. Enemy ship types can be added.
    ''')
    def on_click():
        Bullets.bullet_count = 1
        Bullets.bullet_degree = 30
        Bullets.scale_x_koef = 1
        Bullets.scale_y_koef = 1
        Bullets.speed_koef = 1
        Bullets.damage_koef = 1
        Bullets.speed_shoot_koef = 1
        Bullets.update_bullets_list()
        scene.player.step *= 0.8
        Enemies.difficult_koef *= 1.30
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.player.current_bullet_type = Bullets.navigation_bullet
        scene.keys_txt.setPlainText(
            'W,A,S,D - movement; C - shooting; F11 - toggle full screen; Key_UP,Key_DOWN - navigate bullets')
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)

    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_ultimate_bullet(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('Ultra bullet')
    card.description.setText('''
    Bullet count decreases by 100, but minimum bullet count equals 1. Bullet size: width+50%, height+100%. Maximum bullet size: normal size + 4900%. Bullet damage +100%. But shoot cooldown +1000%. Starship speed -30%.
    Enemy health points, speed and damage increases by 18%. Enemy ship types can be added.
    ''')

    def on_click():
        Bullets.bullet_count -= 100
        Bullets.scale_x_koef *= 1.5
        if int(Bullets.scale_x_koef) > 50:
            Bullets.scale_x_koef = 50
        Bullets.scale_y_koef *= 2
        if int(Bullets.scale_y_koef) > 50:
            Bullets.scale_y_koef = 50
        Bullets.speed_koef *= 0.8
        Bullets.damage_koef *= 2
        Bullets.speed_shoot_koef *= 11
        Bullets.update_bullets_list()
        scene.player.step *= 0.7
        Enemies.difficult_koef *= 1.18
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_army_bullet(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('More bullets')
    card.description.setText('''
    Bullet count increases by 5. Starship speed +10%. But bullet damage -10% and bullet size -10%. Minimum bullet size: normal size -50%.
    Enemy health points, speed and damage increases by 15%. Enemy ship types can be added.
    ''')

    def on_click():
        Bullets.bullet_count += 5
        Bullets.scale_x_koef *= 0.9
        if round(Bullets.scale_x_koef,1) < 0.5:
            Bullets.scale_x_koef = 0.5
        Bullets.scale_y_koef *= 0.9
        if round(Bullets.scale_y_koef,1) < 0.5:
            Bullets.scale_y_koef = 0.5
        Bullets.damage_koef *= 0.9
        Bullets.update_bullets_list()
        scene.player.step *= 1.1
        Enemies.difficult_koef *= 1.15
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card


def card_concentrate_bullet(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('Concentrate')
    card.description.setText('''
    Bullet direction spread decreases by 2*10 degrees. bullet size -10%. Minimum bullet size: normal size - 50%. Bullet damage -20%. Bullet speed +20%. 
    Enemy health points, speed and damage increases by 15%. Enemy ship types can be added.
    ''')
    def on_click():
        Bullets.bullet_degree -= 10
        Bullets.scale_x_koef *= 0.9
        if round(Bullets.scale_x_koef,1) < 0.5:
            Bullets.scale_x_koef = 0.5
        Bullets.scale_y_koef *= 0.9
        if round(Bullets.scale_y_koef,1) < 0.5:
            Bullets.scale_y_koef = 0.5
        Bullets.speed_koef *= 1.2
        Bullets.damage_koef *= 0.8
        # Bullets.speed_shoot_koef *= 0.8
        Bullets.update_bullets_list()
        Enemies.difficult_koef *= 1.15
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_spray_bullet(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('Spread')
    card.description.setText('''
    Bullet direction spread increases by 2*10 degrees. bullet size +10%. Maximum bullet size: normal size + 4900%. Bullet damage -20%. Bullet speed -30%
    Enemy health points, speed and damage increases by 15%. Enemy ship types can be added.
    ''')
    def on_click():
        Bullets.bullet_degree += 10
        Bullets.scale_x_koef *= 1.1
        if int(Bullets.scale_x_koef) > 50:
            Bullets.scale_x_koef = 50
        Bullets.scale_y_koef *= 1.1
        if int(Bullets.scale_y_koef) > 50:
            Bullets.scale_y_koef = 50
        Bullets.speed_koef *= 0.7
        Bullets.update_bullets_list()
        Enemies.difficult_koef *= 1.15
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_random_effect(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('Random')
    card.description.setText('''
    Starship health points decreases by 1, but minimum health points equal 1.
    Random effects may be:
    first effect: bullet size x, bullet size y, starship breaking speed, bullet speed, shoot cooldown. first effect decreases/increases by from -50% to +100%.
    second effect: bullet count, bullet spread(degrees), starship health points, starship size, starship speed. second effect decreases/increases by from -5 to 5. But minimum starship health points equals 1, minimum satrship size equals 15.    
    Enemy health points, speed and damage increases by 20%. Enemy ship types can be added.
    ''')
    def on_click():
        positive_effect1 = random.choice(
            (Bullets.scale_x_koef,scene.player.soap_koef,
             Bullets.scale_y_koef,Bullets.speed_koef,Bullets.speed_shoot_koef))
        positive_effect1 *= random.uniform(0.5,2)
        positive_effect2 = random.choice(
            (Bullets.bullet_count,Bullets.bullet_degree,scene.player.hp,scene.player.size_x,
             scene.player.step))
        positive_effect2 += random.randint(-5,5)
        scene.player.hp -= 1
        if scene.player.hp <= 0:
            scene.player.hp = 1
        if scene.player.size_x < 15:
            scene.player.size_x = 15
        scene.player.size_y = scene.player.size_x
        scene.player.update_size(scene.player.size_x,scene.player.size_y)
        if round(Bullets.scale_x_koef,1) < 0.5:
            Bullets.scale_x_koef = 0.5
        if round(Bullets.scale_y_koef,1) < 0.5:
            Bullets.scale_y_koef = 0.5
        if int(Bullets.scale_x_koef) > 50:
            Bullets.scale_x_koef = 50
        if int(Bullets.scale_y_koef) > 50:
            Bullets.scale_y_koef = 50
        Bullets.update_bullets_list()
        Enemies.difficult_koef *= 1.2
        Enemies.update_enemies_list()
        if len(scene.available_enemy_types) < len(Enemies.list_of_types):
            scene.available_enemy_types.append(Enemies.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
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
    card_army_bullet,
    card_concentrate_bullet,
    card_spray_bullet,
    card_random_effect
]