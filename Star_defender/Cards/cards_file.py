import random
import sys

from PyQt6.QtCore import QRect, Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QFont, QCursor, QPalette, QColor, QPainter, QPixmap, QBrush
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QVBoxLayout

from Bullets import bullets_file
from Enemies import enemies_file


timer = QTimer()
timer.timeout.connect(timer.stop)

class HoverButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.parent = parent

    def enterEvent(self, event):
        # Изменяем цвет фона родительского виджета при наведении мыши на кнопку
        self.parent.enter_background()
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Восстанавливаем исходный цвет фона родительского виджета при уходе мыши с кнопки
        self.parent.leave_background()
        super().leaveEvent(event)

class Card(QWidget):
    def __init__(self,rect:QRect,style_name:QFont,style_desc:QFont):
        super().__init__()
        self.setGeometry(rect)
        self.setStyleSheet('padding:7px;')
        self.pixmap = QPixmap()
        self.enter_pixmap = QPixmap()
        self.enter_pixmap_path = ''

        self.name = QLabel(self)
        self.name.move(0,0)
        self.name.setFixedWidth(self.width())
        self.name.setStyleSheet('background-color:transparent')
        self.name.setWordWrap(True)
        self.name.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.name.setFont(style_name)
        self.name.show()

        self.description = QLabel(self)
        self.description.setGeometry(QRect(0, int(self.name.height()-1),self.width(), self.height()))
        self.description.setStyleSheet('background-color:transparent')
        self.description.setFixedWidth(self.width())
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.description.setFont(style_desc)
        self.description.show()

        # self.button = QPushButton(self)
        self.button = HoverButton('',self)
        self.button.setGeometry(0,0,self.width(),self.height())
        self.button.setStyleSheet('''
        QPushButton{background-color:rgba(0,0,0,0);border:none}
        ''')
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.show()

    def enter_background(self):
        self.enter_pixmap.load(self.enter_pixmap_path)

    def leave_background(self):
        self.enter_pixmap.load('')

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)
        painter.drawPixmap(self.rect(),self.enter_pixmap)


def card_blessing(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Blessing')
    card.description.setText(
        '''Starship health points increases by 2. Also starship size +10%. Maximum starship size equals 100. But starship speed -80%.
        Enemy health points, speed and damage +15%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0,int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        scene.player.hp += 2
        scene.player.size_x = int(scene.player.size_x*1.1)
        scene.player.size_y = int(scene.player.size_y*1.1)
        if scene.player.size_x > 100:
            scene.player.size_x = 100
            scene.player.size_y = 100
        scene.player.update_size(scene.player.size_x,scene.player.size_y)
        scene.player.step *= 0.2
        enemies_file.difficult_koef *= 1.15
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_power(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Power up')
    card.description.setText(
        '''Starship damage +10%. Starship speed +20%. But starship size -10%. Minimum starship size equals 15.
        Enemy health points, speed and damage increases by 10%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        scene.player.damage *= 1.1
        scene.player.step *= 1.2
        scene.player.size_x = int(scene.player.size_x*0.9)
        scene.player.size_y = int(scene.player.size_y*0.9)
        if scene.player.size_x < 15:
            scene.player.size_x = 15
            scene.player.size_y = 15
        scene.player.update_size(scene.player.size_x,scene.player.size_y)
        enemies_file.difficult_koef *= 1.1
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.player.update_size(scene.player.size_x,scene.player.size_y)
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)

    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_washing(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Washing ship')
    card.description.setText(
        '''Starship speed +20%. Starship breaking speed +20%. But starship damage -1%.
        Enemy health points, speed and damage increases by 8%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        scene.player.step *= 1.2
        scene.player.soap_koef *= 0.8
        scene.player.damage *= 0.99
        enemies_file.difficult_koef *= 1.08
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_add_bullet(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Add bullet')
    card.description.setText(
        '''Starship bullets count increases by 1. But starship damage -10%.
        Enemy health points, speed and damage increases by 6%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        bullets_file.bullet_count += 1
        bullets_file.first_arg_method = bullets_file.bullet_count
        scene.player.damage *= 0.9
        enemies_file.difficult_koef *= 1.06
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card


def card_big_bullet(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Big bullet')
    card.description.setText(
        '''Bullet size +20%. Maximum bullet size: normal size + 4900%. Bullet damage +20%. But bullet speed -10%. Shoot cooldown +30%
        Enemy health points, speed and damage increases by 9%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        bullets_file.scale_x_koef *= 1.2
        if int(bullets_file.scale_x_koef) > 50:
            bullets_file.scale_x_koef = 50
        bullets_file.scale_y_koef *= 1.2
        if int(bullets_file.scale_y_koef) > 50:
            bullets_file.scale_y_koef = 50
        bullets_file.damage_koef *= 1.2
        bullets_file.speed_koef *= 0.7
        bullets_file.speed_shoot_koef *= 1.3
        bullets_file.update_bullets_list()
        enemies_file.difficult_koef *= 1.09
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_chaos_bullet_set(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Chaos set')
    card.description.setText(
        '''Sets chaos bullet type:
        bullet count equals 5, bullet direction spread equals 2*60 degrees, bullet width, height, speed, damage, shoot cooldown coefficients equals 1. Starship health points decreates by 2, but minimum health equals 1.
        Enemy health points, speed and damage increases by 20%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        bullets_file.bullet_count = 5
        bullets_file.first_arg_method = bullets_file.bullet_count
        bullets_file.bullet_degree = 60
        bullets_file.second_arg_mothod = bullets_file.bullet_degree
        bullets_file.scale_x_koef = 1
        bullets_file.scale_y_koef = 1
        bullets_file.speed_koef = 1
        bullets_file.damage_koef = 1
        bullets_file.speed_shoot_koef = 1
        bullets_file.update_bullets_list()
        scene.player.hp -= 2
        if scene.player.hp < 1:
            scene.player.hp = 1
        enemies_file.difficult_koef *= 1.2
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.player.current_bullet_type = bullets_file.chaos_bullet
        scene.keys_txt.setPlainText('W,A,S,D - movement; C - shooting; F11 - toggle full screen')
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)

    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_navigation_bullet_set(scene,rect:QRect,style_name:QFont,style_desc:QFont):
    card = Card(rect,style_name,style_desc)
    card.name.setText('Navigation set')
    card.description.setText(
        '''Sets navigation bullet type:
        you can manipulate starship bullets on up, down keys.
        Bullet count equals 5, bullet direction spread equals 2*30 degrees, bullet width, height, speed, damage, shoot cooldown coefficients equals 1. Starship speed -20%.
        Enemy health points, speed and damage increases by 25%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        bullets_file.bullet_count = 1
        bullets_file.bullet_degree = 30
        bullets_file.scale_x_koef = 1
        bullets_file.scale_y_koef = 1
        bullets_file.speed_koef = 1
        bullets_file.damage_koef = 1
        bullets_file.speed_shoot_koef = 1
        bullets_file.update_bullets_list()
        scene.player.step *= 0.8
        enemies_file.difficult_koef *= 1.25
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.player.current_bullet_type = bullets_file.navigation_bullet
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
    card.description.setText(
        '''Bullet count decreases by 100, but minimum bullet count equals 1. Bullet size: width+50%, height+100%. Maximum bullet size: normal size + 4900%. Bullet damage +100%. But shoot cooldown +1000%. Starship speed -30%.
        Enemy health points, speed and damage increases by 13%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        bullets_file.bullet_count -= 100
        bullets_file.scale_x_koef *= 1.5
        if int(bullets_file.scale_x_koef) > 50:
            bullets_file.scale_x_koef = 50
        bullets_file.scale_y_koef *= 2
        if int(bullets_file.scale_y_koef) > 50:
            bullets_file.scale_y_koef = 50
        bullets_file.speed_koef *= 0.8
        bullets_file.damage_koef *= 2
        bullets_file.speed_shoot_koef *= 11
        bullets_file.update_bullets_list()
        scene.player.step *= 0.7
        enemies_file.difficult_koef *= 1.13
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card


def card_army_bullet(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('More bullets')
    card.description.setText(
        '''Bullet count increases by 2. Starship speed +10%. But bullet damage -10% and bullet size -10%. Minimum bullet size: normal size -50%.
        Enemy health points, speed and damage increases by 10%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        bullets_file.bullet_count += 2
        bullets_file.scale_x_koef *= 0.9
        if round(bullets_file.scale_x_koef,1) < 0.5:
            bullets_file.scale_x_koef = 0.5
        bullets_file.scale_y_koef *= 0.9
        if round(bullets_file.scale_y_koef,1) < 0.5:
            bullets_file.scale_y_koef = 0.5
        bullets_file.damage_koef *= 0.9
        bullets_file.update_bullets_list()
        scene.player.step *= 1.1
        enemies_file.difficult_koef *= 1.1
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card


def card_concentrate_bullet(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('Concentrate')
    card.description.setText(
        '''Bullet direction spread decreases by 2*10 degrees. bullet size -10%. Minimum bullet size: normal size - 50%. Bullet damage -20%. Bullet speed +20%. 
        Enemy health points, speed and damage increases by 10%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        bullets_file.bullet_degree -= 10
        bullets_file.scale_x_koef *= 0.9
        if round(bullets_file.scale_x_koef,1) < 0.5:
            bullets_file.scale_x_koef = 0.5
        bullets_file.scale_y_koef *= 0.9
        if round(bullets_file.scale_y_koef,1) < 0.5:
            bullets_file.scale_y_koef = 0.5
        bullets_file.speed_koef *= 1.2
        bullets_file.damage_koef *= 0.8
        # bullets_file.speed_shoot_koef *= 0.8
        bullets_file.update_bullets_list()
        enemies_file.difficult_koef *= 1.1
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card


def card_spray_bullet(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('Spread')
    card.description.setText(
        '''Bullet direction spread increases by 2*10 degrees. bullet size +10%. Maximum bullet size: normal size + 4900%. Bullet damage -20%. Bullet speed -30%
        Enemy health points, speed and damage increases by 10%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        bullets_file.bullet_degree += 10
        bullets_file.scale_x_koef *= 1.1
        if int(bullets_file.scale_x_koef) > 50:
            bullets_file.scale_x_koef = 50
        bullets_file.scale_y_koef *= 1.1
        if int(bullets_file.scale_y_koef) > 50:
            bullets_file.scale_y_koef = 50
        bullets_file.speed_koef *= 0.7
        bullets_file.update_bullets_list()
        enemies_file.difficult_koef *= 1.1
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
        scene.stack_proxy_widget.setVisible(False)
        scene.stop_game(False)
    card.button.clicked.connect(on_click)
    card.button.show()
    return card

def card_random_effect(scene, rect:QRect, style_name:QFont, style_desc:QFont):
    card = Card(rect, style_name, style_desc)
    card.name.setText('Random')
    card.description.setText(
        '''Starship health points decreases by 1, but minimum health points equal 1.
        Random effects may be:
        first effect: bullet size x, bullet size y, starship breaking speed, bullet speed, shoot cooldown. first effect decreases/increases by from -50% to +100%.
        second effect: bullet count, bullet spread(degrees), starship health points, starship size, starship speed. second effect decreases/increases by from -5 to 5. But minimum starship health points equals 1, minimum satrship size equals 15.    
        Enemy health points, speed and damage increases by 15%. Enemy ship types can be added.''')
    card.description.adjustSize()
    card.description.move(0, int((card.height() // 2) - (card.description.height() // 2)))
    def on_click():
        positive_effect1 = random.choice(
            (bullets_file.scale_x_koef,scene.player.soap_koef,
             bullets_file.scale_y_koef,bullets_file.speed_koef,bullets_file.speed_shoot_koef))
        positive_effect1 *= random.uniform(0.5,2)
        positive_effect2 = random.choice(
            (bullets_file.bullet_count,bullets_file.bullet_degree,scene.player.hp,scene.player.size_x,
             scene.player.step))
        positive_effect2 += random.randint(-5,5)
        scene.player.hp -= 1
        if scene.player.hp <= 0:
            scene.player.hp = 1
        if scene.player.size_x < 15:
            scene.player.size_x = 15
        scene.player.size_y = scene.player.size_x
        scene.player.update_size(scene.player.size_x,scene.player.size_y)
        if round(bullets_file.scale_x_koef,1) < 0.5:
            bullets_file.scale_x_koef = 0.5
        if round(bullets_file.scale_y_koef,1) < 0.5:
            bullets_file.scale_y_koef = 0.5
        if int(bullets_file.scale_x_koef) > 50:
            bullets_file.scale_x_koef = 50
        if int(bullets_file.scale_y_koef) > 50:
            bullets_file.scale_y_koef = 50
        bullets_file.update_bullets_list()
        enemies_file.difficult_koef *= 1.15
        enemies_file.update_enemies_list()
        if len(scene.available_enemy_types) < len(enemies_file.list_of_types):
            scene.available_enemy_types.append(enemies_file.list_of_types[len(scene.available_enemy_types)])
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