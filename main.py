import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QLineEdit, QDialog, QTableWidget, QTableWidgetItem
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

# Класс для управления базой данных
class DatabaseManager:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lost_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    description TEXT,
                    barcode TEXT
                )
            """)
            conn.commit()

    def add_item(self, name, description, barcode):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO lost_items (name, description, barcode) VALUES (?, ?, ?)", 
                           (name, description, barcode))
            conn.commit()

# Класс для главного окна
class LostTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lost&Tracker")
        self.setGeometry(200, 100, 800, 500)
        self.setWindowIcon(QIcon("ARLogo.ico"))
        self.db = DatabaseManager()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Логотип
        self.logo = QLabel(self)
        pixmap = QPixmap("assets/ARLost&Found-1.png")
        pixmap = pixmap.scaled(1000, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)

        # Кнопки
        self.search_button = QPushButton("Найти вещь")
        self.add_button = QPushButton("Добавить потерянную вещь")
        self.list_button = QPushButton("Список потерянных вещей")

        layout.addWidget(self.search_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.list_button)

        # Привязываем кнопки к методам
        self.search_button.clicked.connect(self.open_search_window)
        self.add_button.clicked.connect(self.open_add_window)
        self.list_button.clicked.connect(self.open_list_window)

        self.setLayout(layout)

    def open_search_window(self):
        self.search_window = FindItemWindow(self.db)
        self.search_window.show()

    def open_add_window(self):
        self.add_window = AddItemWindow(self.db)
        self.add_window.show()

    def open_list_window(self):
        self.list_window = ItemListWindow(self.db)
        self.list_window.show()

# Окно добавления вещи
class AddItemWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Добавить потерянную вещь")
        self.setGeometry(300, 150, 400, 300)
        self.setWindowIcon(QIcon("assets/ARLogo.ico"))
        self.db = db
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Название вещи")

        self.desc_input = QLineEdit(self)
        self.desc_input.setPlaceholderText("Описание")

        self.barcode_input = QLineEdit(self)
        self.barcode_input.setPlaceholderText("Штрих-код (или сканируйте)")
        self.barcode_input.setReadOnly(True)

        self.scan_button = QPushButton("Сканировать ШК")
        self.submit_button = QPushButton("Добавить в базу")

        layout.addWidget(self.name_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.barcode_input)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.submit_button)

        self.scan_button.clicked.connect(self.open_scan_window)
        self.submit_button.clicked.connect(self.save_to_db)

        self.setLayout(layout)

    def open_scan_window(self):
        self.scan_window = ScanWindow(self)
        self.scan_window.show()

    def save_to_db(self):
        name = self.name_input.text().strip()
        description = self.desc_input.text().strip()
        barcode = self.barcode_input.text().strip()

        if name and description and barcode:
            self.db.add_item(name, description, barcode)
            self.close()

# Окно поиска вещи
class FindItemWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Найти вещь")
        self.setGeometry(300, 150, 400, 300)
        self.setWindowIcon(QIcon("assets/ARLogo.ico"))
        self.db = db
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Введите название, описание или ШК")

        self.search_button = QPushButton("Найти в базе")

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

# Окно сканирования штрих-кода
class ScanWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Сканирование ШК")
        self.setGeometry(350, 200, 300, 100)
        self.setWindowIcon(QIcon("assets/ARLogo.ico"))

        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.scan_input = QLineEdit(self)
        self.scan_input.setPlaceholderText("Отсканируйте штрих-код")
        layout.addWidget(self.scan_input)

        self.setLayout(layout)

        self.scan_input.returnPressed.connect(self.process_scan)

    def process_scan(self):
        scanned_code = self.scan_input.text()
        if scanned_code:
            self.parent.barcode_input.setText(scanned_code)
            self.close()

# Окно списка вещей
class ItemListWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Список потерянных вещей")
        self.setGeometry(300, 150, 500, 400)
        self.setWindowIcon(QIcon("assets/ARLogo.ico"))
        self.db = db
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Название", "Описание", "Штрих-код"])

        layout.addWidget(self.table)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/ARLogo.ico"))
    window = LostTrackerApp()
    window.setWindowIcon(QIcon("assets/ARLogo.ico"))
    window.show()
    sys.exit(app.exec())
