import random
import sqlite3
import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget
)

# Создаем или подключаемся к базе данных
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"
)
conn.commit()


# Главное окно входа
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setGeometry(100, 100, 300, 150)
        self.layout = QVBoxLayout()

        self.label_username = QLabel("Имя пользователя:")
        self.layout.addWidget(self.label_username)

        self.input_username = QLineEdit()
        self.layout.addWidget(self.input_username)

        self.label_password = QLabel("Пароль:")
        self.layout.addWidget(self.label_password)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.input_password)

        self.button_login = QPushButton("Войти")
        self.button_login.clicked.connect(self.login)
        self.layout.addWidget(self.button_login)

        self.button_register = QPushButton("Регистрация (z + x + c)")
        self.button_register.clicked.connect(self.open_register_window)
        self.layout.addWidget(self.button_register)

        self.setLayout(self.layout)

    def login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        # Проверка учетных данных в базе данных
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            QMessageBox.information(self, "Успех", "Вход выполнен успешно!")
            self.open_main_program()
        else:
            QMessageBox.warning(self, "Ошибка", "Неправильное имя пользователя или пароль.")

    def open_register_window(self):
        self.close()
        self.register_window = RegisterWindow()
        self.register_window.show()

    def open_main_program(self):
        self.close()
        self.main_program = MyWidget()
        self.main_program.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Z:
            self.z_pressed = True
        elif event.key() == Qt.Key.Key_X and getattr(self, "z_pressed", False):
            self.x_pressed = True
        elif event.key() == Qt.Key.Key_C and getattr(self, "x_pressed", False):
            self.open_register_window()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Z:
            self.z_pressed = False
        elif event.key() == Qt.Key.Key_X:
            self.x_pressed = False


# Окно регистрации нового пользователя
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(100, 100, 300, 150)
        self.layout = QVBoxLayout()

        self.label_username = QLabel("Имя пользователя:")
        self.layout.addWidget(self.label_username)

        self.input_username = QLineEdit()
        self.layout.addWidget(self.input_username)

        self.label_password = QLabel("Пароль:")
        self.layout.addWidget(self.label_password)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.input_password)

        self.button_register = QPushButton("Зарегистрироваться")
        self.button_register.clicked.connect(self.register_user)
        self.layout.addWidget(self.button_register)

        self.setLayout(self.layout)

    def register_user(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Добавляем нового пользователя в базу данных
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
            self.close()
            self.login_window = LoginWindow()
            self.login_window.show()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Имя пользователя уже занято.")


# Окно для создания нового пароля
class CreatePasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание пароля")
        self.setGeometry(100, 100, 300, 250)
        self.layout = QVBoxLayout()

        self.label_service = QLabel("Сервис:")
        self.layout.addWidget(self.label_service)

        self.input_service = QLineEdit()
        self.layout.addWidget(self.input_service)

        self.label_password = QLabel("Пароль:")
        self.layout.addWidget(self.label_password)

        self.input_password = QLineEdit()
        self.layout.addWidget(self.input_password)

        # Добавляем кнопку "Случайный пароль"
        self.button_generate_password = QPushButton("Случайный пароль")
        self.button_generate_password.clicked.connect(self.generate_random_password)
        self.layout.addWidget(self.button_generate_password)

        self.label_type = QLabel("Тип сервиса:")
        self.layout.addWidget(self.label_type)

        self.input_type = QLineEdit()
        self.layout.addWidget(self.input_type)

        self.label_login = QLabel("Логин:")
        self.layout.addWidget(self.label_login)

        self.input_login = QLineEdit()
        self.layout.addWidget(self.input_login)

        self.button_save = QPushButton("Сохранить")
        self.button_save.clicked.connect(self.save_password)
        self.layout.addWidget(self.button_save)

        self.setLayout(self.layout)

    def generate_random_password(self):
        # Генерирует случайный пароль из 10 символов и вставляет его в поле ввода.
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        random_password = ''.join(random.choices(characters, k=10))
        self.input_password.setText(random_password)

    def save_password(self):
        service = self.input_service.text()
        password = self.input_password.text()
        service_type = self.input_type.text()
        login = self.input_login.text()

        if not service or not password or not service_type or not login:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            conn = sqlite3.connect("films_db.sqlite")
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS films "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "service TEXT, password TEXT, type TEXT, login TEXT)"
            )
            conn.commit()

            cursor.execute(
                "INSERT INTO films (service, password, type, login) VALUES (?, ?, ?, ?)",
                (service, password, service_type, login)
            )
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Пароль сохранен!")
            self.close()
            self.open_search_window()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные: {e}")

    def open_search_window(self):
        self.search_window = MyWidget()
        self.search_window.show()


# Основное приложение, которое запускается после успешного входа
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поиск пароля")
        self.setGeometry(100, 100, 600, 250)

        # Основной вертикальный layout
        main_layout = QVBoxLayout(self)

        # Верхний layout с параметрами поиска
        search_layout = QHBoxLayout()
        self.parameterSelection = QComboBox()
        self.parameterSelection.setMinimumSize(200, 0)
        search_layout.addWidget(self.parameterSelection)

        self.queryLine = QLineEdit()
        search_layout.addWidget(self.queryLine)

        self.queryButton = QPushButton("Поиск")
        search_layout.addWidget(self.queryButton)

        main_layout.addLayout(search_layout)

        # Сетка для отображения найденной информации
        grid_layout = QGridLayout()
        labels = ["ID:", "Сервис:", "Пароль:", "Тип сервиса:", "Логин:"]
        self.fields = {}

        for i, text in enumerate(labels):
            label = QLabel(text)
            grid_layout.addWidget(label, i, 0)
            field = QLineEdit()
            self.fields[text] = field
            grid_layout.addWidget(field, i, 1)

        main_layout.addLayout(grid_layout)

        # Метка для ошибок
        self.errorLabel = QLabel("")
        main_layout.addWidget(self.errorLabel)

        # Добавление кнопок управления
        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.newPasswordButton = QPushButton("Новый пароль")
        button_layout.addWidget(self.newPasswordButton)

        self.clearStorageButton = QPushButton("Очистить хранилище")
        button_layout.addWidget(self.clearStorageButton)

        main_layout.addLayout(button_layout)

        # Кнопка для удаления
        self.deletePasswordButton = QPushButton("Удалить этот пароль")
        main_layout.addWidget(self.deletePasswordButton)

        # Настройка поведения кнопок
        self.params = {"Пароль": "password", "Сервис": "service", "логин": "login"}
        self.parameterSelection.addItems(list(self.params.keys()))
        self.con = sqlite3.connect("films_db.sqlite")
        self.queryButton.clicked.connect(self.select)
        self.newPasswordButton.clicked.connect(self.open_create_password_window)
        self.clearStorageButton.clicked.connect(self.clear_storage)
        self.deletePasswordButton.clicked.connect(self.delete_password)

    def select(self):
        try:
            req = (f"SELECT * FROM films WHERE "
                   f"{self.params.get(self.parameterSelection.currentText())} "
                   f"= ?")
            cur = self.con.cursor()
            result = cur.execute(
                req,
                (self.queryLine.text(),)
            ).fetchone()
            if not result:
                if self.queryLine.text().replace(" ", "") == "":
                    self.errorLabel.setText("Неправильный запрос")
                else:
                    self.errorLabel.setText("Ничего не найдено")
                for field in self.fields.values():
                    field.setText("")
                return
            for key, value in zip(self.fields.keys(), result):
                self.fields[key].setText(str(value))
            self.errorLabel.setText("")
        except sqlite3.OperationalError:
            self.errorLabel.setText("Неправильный запрос")

    def delete_password(self):
        record_id = self.fields["ID:"].text()
        if not record_id:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить эту запись?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                cur = self.con.cursor()
                cur.execute("DELETE FROM films WHERE id = ?", (record_id,))
                self.con.commit()
                QMessageBox.information(self, "Успех", "Запись успешно удалена.")
                for field in self.fields.values():
                    field.setText("")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить запись: {e}")
        else:
            QMessageBox.information(self, "Отмена", "Удаление записи отменено.")

    def open_create_password_window(self):
        self.close()
        self.create_password_window = CreatePasswordWindow()
        self.create_password_window.show()

    def clear_storage(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение очистки",
            "Все данные будут безвозвратно утеряны! Хотите продолжить?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                cur = self.con.cursor()
                cur.execute("DELETE FROM films")
                self.con.commit()
                QMessageBox.information(self, "Успех", "Хранилище успешно очищено.")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось очистить хранилище: {e}")
        else:
            QMessageBox.information(self, "Отмена", "Очистка хранилища отменена.")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
