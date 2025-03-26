import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap

class LostTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lost&Tracker")
        self.setGeometry(200, 100, 800, 500)  # Размер окна
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Логотип
        self.logo = QLabel(self)
        pixmap = QPixmap("assets/logo.png")  # Загружаем логотип
        self.logo.setPixmap(pixmap)
        layout.addWidget(self.logo)

        # Кнопки
        self.add_button = QPushButton("Добавить потерянную вещь")
        self.search_button = QPushButton("Найти вещь")
        self.scan_button = QPushButton("Сканировать штрих-код")

        layout.addWidget(self.add_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.scan_button)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LostTrackerApp()
    window.show()
    sys.exit(app.exec())
