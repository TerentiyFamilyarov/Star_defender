from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.label = QLabel("Player", self)
        self.label.move(500, 500)
        self.player_margin_left = 0
        self.player_margin_top = 0

    def scaleEvent(self, event):
        # Получить оригинальные размеры окна
        old_size = self.size()

        # Получить позицию игрока относительно размеров окна в процентах
        player_pos = self.label.pos()
        self.player_margin_left = player_pos.x() / old_size.width()
        self.player_margin_top = player_pos.y() / old_size.height()

        # Изменить размер окна
        super().resizeEvent(event)

        # Получить новые размеры окна
        new_size = self.size()

        # Вычислить новую позицию игрока в соответствии с новыми размерами окна
        new_player_pos = QPoint(new_size.width() * self.player_margin_left, new_size.height() * self.player_margin_top)

        # Установить новую позицию игрока
        self.label.move(new_player_pos)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
