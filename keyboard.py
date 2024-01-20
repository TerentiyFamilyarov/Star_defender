import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import QPropertyAnimation, QPoint


class MovingObject(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.setGeometry(375, 275, 50, 50)
        self.setStyleSheet("background-color: red")

        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(2000)  # 2 секунды
        self.animation.setStartValue(QPoint(, 275))
        self.animation.setEndValue(QPoint(375, 375))
        self.animation.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Moving Object')
        self.setGeometry(100, 100, 800, 600)

        moving_object = MovingObject(self)
        moving_object.show()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
