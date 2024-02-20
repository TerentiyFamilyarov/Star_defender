import sys

from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QStackedWidget, QLabel, QPushButton, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stackedWidget = QStackedWidget(self)
        self.setCentralWidget(self.stackedWidget)

        self.setupUI()

    def setupUI(self):
        page1 = QWidget()
        page1.setStyleSheet('background-color: black')
        layout1 = QVBoxLayout(page1)
        label1 = QLabel("Это страница 1")
        button1 = QPushButton("Нажми меня")
        layout1.setGeometry(QRect(0,0,500,500))

        # Изменение положения и размеров кнопки
        button1.setGeometry(100, 100, 200, 50)

        layout1.addWidget(label1)
        layout1.addWidget(button1)

        page2 = QWidget()
        layout2 = QVBoxLayout(page2)
        label2 = QLabel("Это страница 2")
        layout2.addWidget(label2)

        self.stackedWidget.addWidget(page1)
        self.stackedWidget.addWidget(page2)

        button1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
