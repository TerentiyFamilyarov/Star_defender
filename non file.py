# import sys
# from time import sleep
#
# from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QTimer
# from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
#
# class Worker(QThread):
#     data_updated = pyqtSignal(str)  # Сигнал для передачи данных в основной поток
#     finished = pyqtSignal()  # Сигнал для уведомления о завершении работы
#     request_data = pyqtSignal()  # Сигнал для запроса данных из основного потока
#     receive_data = pyqtSlot(object)  # Слот для получения данных из основного потока
#
#     def __init__(self):
#         super().__init__()
#         self._is_running = False
#         self.data = None
#
#     def run(self):
#         self._is_running = True
#         counter = 0
#         while self._is_running:
#             self.request_data.emit()  # Запрашиваем данные из основного потока
#             if self.data is not None:
#                 # Обновление данных (пример)
#                 data = f"Counter: {counter}, Data: {self.data}"
#                 self.data_updated.emit(data)
#             self.msleep(1000)  # Задержка для имитации длительной работы
#             counter += 1
#
#         self.finished.emit()  # Уведомление о завершении работы
#
#     def stop(self):
#         self._is_running = False
#
#     @pyqtSlot(object)
#     def receive_data(self, data):
#         self.data = data
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.layout = QVBoxLayout(self)
#
#         self.label = QLabel("Press 'Start' to run the worker", self)
#         self.layout.addWidget(self.label)
#
#         self.start_button = QPushButton("Start", self)
#         self.start_button.clicked.connect(self.start_worker)
#         self.layout.addWidget(self.start_button)
#
#         self.stop_button = QPushButton("Stop", self)
#         self.stop_button.clicked.connect(self.stop_worker)
#         self.layout.addWidget(self.stop_button)
#
#         self.data_label = QLabel("Data: None", self)
#         self.layout.addWidget(self.data_label)
#
#         self.worker = Worker()
#         self.worker.data_updated.connect(self.update_label)
#         self.worker.finished.connect(self.on_worker_finished)
#         self.worker.request_data.connect(self.send_data_to_worker)
#
#         # self.timer = QTimer()
#         # self.timer.timeout.connect(self.update_game)
#         # self.timer.start(10)
#
#         self.data = [12,4,6,7,(1,5)]  # Пример данных
#
#     # def update_game(self):
#     #     print('work')
#     #     sleep(0.1)
#
#     @pyqtSlot()
#     def start_worker(self):
#         if not self.worker.isRunning():
#             self.worker.start()
#
#     @pyqtSlot()
#     def stop_worker(self):
#         self.worker.stop()
#
#     @pyqtSlot(str)
#     def update_label(self, data):
#         self.label.setText(data)
#
#     @pyqtSlot()
#     def on_worker_finished(self):
#         self.label.setText("Worker finished")
#
#     @pyqtSlot()
#     def send_data_to_worker(self):
#         # self.data += 1  # Обновление данных (пример)
#         self.data_label.setText(f"Data: {self.data}")
#         self.worker.receive_data(self.data)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = MainWindow()
#     mainWindow.show()
#     sys.exit(app.exec())



import sys
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QRectF, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class CollisionWorker(QThread):
    collisions_calculated = pyqtSignal(list)  # Сигнал для передачи результатов коллизий в основной поток
    request_data = pyqtSignal()  # Сигнал для запроса данных из основного потока
    receive_data = pyqtSlot(object)  # Слот для получения данных из основного потока

    def __init__(self):
        super().__init__()
        self._is_running = False
        self.data = None

    def run(self):
        self._is_running = True
        while self._is_running:
            self.request_data.emit()  # Запрашиваем данные из основного потока
            if self.data is not None:
                collisions = self.calculate_collisions(self.data)
                self.collisions_calculated.emit(collisions)
            self.msleep(1600)  # 60 FPS

    def stop(self):
        self._is_running = False

    @pyqtSlot(object)
    def receive_data(self, data):
        self.data = data

    def calculate_collisions(self, data):
        enemies, bullets, scene_rect = data
        collisions = []
        for enemy in enemies:
            enemy_rect = QRectF(enemy['x'], enemy['y'], enemy['size_x'], enemy['size_y'])
            if not scene_rect.intersects(enemy_rect):
                collisions.append(('enemy_out_of_bounds', enemy))
            for bullet in bullets:
                bullet_rect = QRectF(bullet['x'], bullet['y'], bullet['size_x'], bullet['size_y'])
                if enemy_rect.intersects(bullet_rect):
                    collisions.append(('bullet_hit_enemy', bullet, enemy))
        return collisions

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.enemies = [{'x': 10, 'y': 10, 'size_x': 30, 'size_y': 30}]
        self.bullets = [{'x': 15, 'y': 15, 'size_x': 5, 'size_y': 5}]
        self.scene_rect = QRectF(0, 0, 400, 300)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_game)
        self.update_timer.start(16)  # 60 FPS

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Press 'Start' to run the collision worker", self)
        self.layout.addWidget(self.label)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_worker)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_worker)
        self.layout.addWidget(self.stop_button)

        self.worker = CollisionWorker()
        self.worker.collisions_calculated.connect(self.handle_collisions)
        self.worker.request_data.connect(self.send_data_to_worker)

    @pyqtSlot()
    def start_worker(self):
        if not self.worker.isRunning():
            self.worker.start()

    @pyqtSlot()
    def stop_worker(self):
        self.worker.stop()

    @pyqtSlot(list)
    def handle_collisions(self, collisions):
        for collision in collisions:
            if collision[0] == 'enemy_out_of_bounds':
                enemy = collision[1]
                self.label.setText(f"Enemy out of bounds at ({enemy['x']}, {enemy['y']})")
            elif collision[0] == 'bullet_hit_enemy':
                bullet, enemy = collision[1], collision[2]
                self.label.setText(f"Bullet hit enemy at ({bullet['x']}, {bullet['y']})")

    @pyqtSlot()
    def send_data_to_worker(self):
        data = (self.enemies, self.bullets, self.scene_rect)
        self.worker.receive_data(data)

    def update_game(self):
        print('main work')
        # Обновление положения врагов и пуль, вызов других игровых логик и отрисовка
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

