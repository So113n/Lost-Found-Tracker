import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QLineEdit, QDialog, QListWidget, QMessageBox
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt


class Database:
    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lost_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                barcode TEXT UNIQUE NOT NULL
            )
        """)
        self.conn.commit()

    def add_item(self, name, description, barcode):
        self.cursor.execute("INSERT INTO lost_items (name, description, barcode) VALUES (?, ?, ?)", (name, description, barcode))
        self.conn.commit()

    def get_items(self):
        self.cursor.execute("SELECT name, description, barcode FROM lost_items")
        return self.cursor.fetchall()

    def search_item(self, query):
        self.cursor.execute("SELECT name, description, barcode FROM lost_items WHERE name LIKE ? OR description LIKE ? OR barcode LIKE ?", (f"%{query}%", f"%{query}%", f"%{query}%"))
        return self.cursor.fetchall()

    def delete_item(self, barcode):
        self.cursor.execute("DELETE FROM lost_items WHERE barcode = ?", (barcode,))
        self.conn.commit()


class LostTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lost&Tracker")
        self.setGeometry(200, 100, 800, 500)
        self.setWindowIcon(QIcon("ARLogo.ico"))
        self.db = Database()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.logo = QLabel(self)
        pixmap = QPixmap("assets/ARLost&Found-1.png")
        pixmap = pixmap.scaled(1000, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)

        self.search_button = QPushButton("Найти вещь")
        self.add_button = QPushButton("Добавить потерянную вещь")
        self.list_button = QPushButton("Список потерянных вещей")

        layout.addWidget(self.search_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.list_button)

        self.search_button.clicked.connect(self.open_search_window)
        self.add_button.clicked.connect(self.open_add_window)
        self.list_button.clicked.connect(self.open_list_window)

        self.setLayout(layout)

    def open_search_window(self):
        self.search_window = SearchWindow(self.db)
        self.search_window.show()

    def open_add_window(self):
        self.add_window = AddItemWindow(self.db)
        self.add_window.show()

    def open_list_window(self):
        self.list_window = ListWindow(self.db)
        self.list_window.show()


class AddItemWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Добавить потерянную вещь")
        self.setGeometry(300, 150, 400, 300)
        self.setWindowIcon(QIcon("assets/favicon.ico"))
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
        self.submit_button = QPushButton("Добавить в базу")

        layout.addWidget(self.name_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.barcode_input)
        layout.addWidget(self.submit_button)

        self.submit_button.clicked.connect(self.save_to_db)
        self.setLayout(layout)

    def save_to_db(self):
        name = self.name_input.text().strip()
        description = self.desc_input.text().strip()
        barcode = self.barcode_input.text().strip()
        if name and description and barcode:
            self.db.add_item(name, description, barcode)
            self.close()


class SearchWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Найти вещь")
        self.setGeometry(300, 150, 400, 200)
        self.db = db
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Введите название, описание или ШК")
        self.search_button = QPushButton("Найти в базе")

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)

        self.search_button.clicked.connect(self.search_item)
        self.setLayout(layout)

    def search_item(self):
        query = self.search_input.text().strip()
        results = self.db.search_item(query)
        if results:
            QMessageBox.information(self, "Результаты поиска", f"Найдено: {results}")
        else:
            QMessageBox.warning(self, "Ошибка", "Ничего не найдено!")


class ListWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Список потерянных вещей")
        self.setGeometry(300, 150, 400, 300)
        self.db = db
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.delete_button = QPushButton("Удалить выбранную вещь")

        layout.addWidget(self.list_widget)
        layout.addWidget(self.delete_button)

        self.load_items()
        self.delete_button.clicked.connect(self.delete_item)

        self.setLayout(layout)

    def load_items(self):
        self.list_widget.clear()
        items = self.db.get_items()
        for item in items:
            self.list_widget.addItem(f"{item[0]} - {item[1]} - {item[2]}")

    def delete_item(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            barcode = selected_item.text().split(" - ")[-1]
            self.db.delete_item(barcode)
            self.load_items()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LostTrackerApp()
    window.show()
    sys.exit(app.exec())
