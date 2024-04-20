import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem
from PyQt6.QtCore import Qt, QRectF, QTimer, QObject
from PyQt6.QtCore import QPropertyAnimation, QPoint


class CustomItem(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.rect = QRectF(-20, -20, 40, 40)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.drawRect(self.rect)

class AnimationExample(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.item = QGraphicsRectItem(0,0,100,100)
        self.scene.addItem(self.item)

        self.animation = QPropertyAnimation(QObject(), b"pos")
        self.animation.setDuration(1000)  # 1 секунда
        self.animation.setStartValue(self.item.pos())
        self.animation.setEndValue(self.item.pos() + QPoint(100, 0))  # Сдвиг по оси X на 100 пикселей
        self.animation.setLoopCount(-1)  # бесконечное повторение
        self.animation.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = AnimationExample()
    view.show()
    sys.exit(app.exec())




