from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt6.QtCore import QRectF


class MovingPlayer(QGraphicsItem):
    def __init__(self, x=0, y=0, step=10, HP_P=3, x_size=50, y_size=50, width_window=1920, height_window=1080):
        super().__init__()
        self.step = step
        self.HP_P = HP_P
        self.x_size = x_size
        self.y_size = y_size
        self.setX(x)
        self.setY(y)

        self.move_direction_L = 0
        self.move_direction_R = 0
        self.move_direction_U = 0
        self.move_direction_D = 0

        self.width_window = width_window
        self.height_window = height_window

    def boundingRect(self):
        return QRectF(0, 0, self.x_size, self.y_size)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(0, 0, 255))
        painter.drawRect(int(self.x()), int(self.y()), self.x_size, self.y_size)

    def move(self):
        if self.x() - self.step < 0:
            self.setX(0)
        elif self.move_direction_L == 1:
            self.setX(self.x() - self.step)

        if self.x() + self.step > self.width_window - self.x_size:
            self.setX(self.width_window - self.x_size)
        elif self.move_direction_R == 1:
            self.setX(self.x() + self.step)

        if self.y() - self.step < 0:
            self.setY(0)
        elif self.move_direction_U == 1:
            self.setY(self.y() - self.step)

        if self.y() + self.step > self.height_window - self.y_size:
            self.setY(self.height_window - self.y_size)
        elif self.move_direction_D == 1:
            self.setY(self.y() + self.step)

if __name__ == '__main__':
    app = QApplication([])

    window = QMainWindow()
    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    player = MovingPlayer()
    scene.addItem(player)

    window.setCentralWidget(view)
    window.show()

    player.move()

    app.exec()
