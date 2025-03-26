import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QDialog
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

# Класс для главного окна
class LostTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lost&Found Tracker")
        self.setGeometry(200, 100, 800, 500)
        self.setWindowIcon(QIcon("assets/ARLogo.ico"))
        self.initUI()
      
    def initUI(self):
        layout = QVBoxLayout()

        # Логотип
        self.logo = QLabel(self)
        pixmap = QPixmap("assets/ARLost&Found-1.png")  # Загружаем логотип
        pixmap = pixmap.scaled(1000, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрируем логотип
        layout.addWidget(self.logo)

        # Кнопки
        self.search_button = QPushButton("Найти вещь")
        self.add_button = QPushButton("Добавить потерянную вещь")

        layout.addWidget(self.search_button)
        layout.addWidget(self.add_button)

        # Привязываем кнопки к методам
        self.search_button.clicked.connect(self.open_search_window)
        self.add_button.clicked.connect(self.open_add_window)

        self.setLayout(layout)

    def open_search_window(self):
        self.search_window = ItemWindow("Найти вещь")
        self.search_window.show()

    def open_add_window(self):
        self.add_window = ItemWindow("Добавить потерянную вещь")
        self.add_window.show()


# Класс окна поиска или добавления
class ItemWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(300, 150, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Название вещи")

        self.desc_input = QLineEdit(self)
        self.desc_input.setPlaceholderText("Описание")

        self.barcode_input = QLineEdit(self)
        self.barcode_input.setPlaceholderText("Штрих-код ")
        self.barcode_input.setReadOnly(True)  # Только для отображения

        # Кнопки
        self.scan_button = QPushButton("Сканировать ШК")
        self.submit_button = QPushButton("Добавить в базу")

        # Размещение
        layout.addWidget(self.name_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.barcode_input)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.submit_button)

        # Привязываем кнопку сканирования
        self.scan_button.clicked.connect(self.open_scan_window)

        self.setLayout(layout)

    def open_scan_window(self):
        self.scan_window = ScanWindow(self)
        self.scan_window.show()


# Окно сканирования штрих-кода
class ScanWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Сканирование ШК")
        self.setGeometry(350, 200, 300, 100)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.scan_input = QLineEdit(self)
        self.scan_input.setPlaceholderText("Отсканируйте штрих-код")
        layout.addWidget(self.scan_input)

        self.setLayout(layout)

        # Обрабатываем Enter после сканирования
        self.scan_input.returnPressed.connect(self.process_scan)

    def process_scan(self):
        scanned_code = self.scan_input.text()
        if scanned_code:
            self.parent.barcode_input.setText(scanned_code)  # Заполняем поле в главном окне
            self.close()  # Закрываем окно после сканирования


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LostTrackerApp()
    window.show()
    sys.exit(app.exec())