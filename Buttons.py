import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QPushButton, QWidget

from test_zone import MovingPlayer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        timer = QTimer(self)
        timer.timeout.connect(self.updategame)
        timer.start(16)

        self.setGeometry(0,0,600,600)


        mode = [
            MovingPlayer(0,0,10,3,50,50,self.width(),self.height()),
            MovingPlayer(500, 0, 1, 3, 100, 50, self.width(), self.height())
        ]
        modeO=1
        if modeO == 0:
            self.player1 = mode[0]
        if modeO == 1 :
            self.player1 = mode[1]

        button1 = QPushButton('1mode',self)

        button1.clicked.connect(lambda: modeO+1)
        button1.setGeometry(0,0,50,50)
        button1.show()




        # self.showMaximized()

    def updategame(self):
        self.player1.move()
        self.update()

    def keyPressEvent(self, event):
        self.player1.keyPressEvent(event)
    def keyReleaseEvent(self, event):
        self.player1.keyReleaseEvent(event)
    def paintEvent(self, event):
        painter = QPainter(self)
        self.player1.paint(painter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
