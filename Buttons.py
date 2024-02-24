from PyQt6.QtCore import QPropertyAnimation, QVariantAnimation
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

app = QApplication([])

widget = QWidget()
layout = QVBoxLayout(widget)

label = QLabel("Мерцающий текст", widget)
layout.addWidget(label)

animation = QVariantAnimation(label)
animation.setLoopCount(-1) # Бесконечное мерцание
animation.setDuration(500) # Длительность одного периода мерцания
animation.setStartValue(label.palette().color(label.foregroundRole()))
animation.setEndValue(label.palette().color(label.backgroundRole()))

animation.start()

widget.show()
app.exec()
