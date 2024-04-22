import sys

from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEffect, QLabel, QGraphicsItem
from PyQt6.QtGui import QPixmap

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создать сцену
    scene = QGraphicsScene()

    # Создать объект с изображением
    # pixmap_item = scene.addPixmap(QPixmap('Nik Saltykov.jpg'))
    # pixmap_item.setPixmap(QPixmap("image.png"))
    # pixmap_item.setTiled(True)
    # Добавить объект в сцену
    # scene.addItem(pixmap_item)

    # Создать виджет просмотра и установить сцену
    view = QGraphicsView()
    view.setScene(scene)
    # view.rotate(45)
    # view.setStyleSheet("background-image: url('Nik Saltykov.jpg');")

    # Отобразить виджет просмотра
    view.show()

    sys.exit(app.exec())
