import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit,
                             QLabel, QFormLayout, QMessageBox, QInputDialog,
                             QComboBox, QStackedLayout, QHBoxLayout)
from PyQt5.QtCore import Qt

class UserData:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.ingredients = []

    def save_to_file(self):
        data = {
            "username": self.username,
            "password": self.password,
            "ingredients": self.ingredients
        }
        with open(f"{self.username}_data.json", "w") as f:
            json.dump(data, f)

    def load_from_file(self):
        try:
            with open(f"{self.username}_data.json", "r") as f:
                data = json.load(f)
                if data.get("username") == self.username:
                    self.password = data.get("password", "")
                    self.ingredients = data.get("ingredients", [])
        except FileNotFoundError:
            pass

user_data = UserData()

class BaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #f0f0f0;
                font-family: Segoe UI, sans-serif;
                font-size: 16px;
            }
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                 stop:0 #4facfe, stop:1 #00f2fe);
                color: white;
                border: none;
                padding: 12px 26px;
                font-size: 15px;
                border-radius: 8px;
                min-width: 220px;
                max-width: 220px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                 stop:0 #00c6ff, stop:1 #0072ff);
            }
            QPushButton:pressed {
                background-color: #005fa3;
            }
            QLineEdit {
                background-color: #2e2e3a;
                color: white;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 10px;
                font-size: 15px;
                min-width: 200px;
                max-width: 200px;
            }
            QLabel {
                font-size: 17px;
                padding: 6px;
            }
        """)

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface Moderne")
        self.setGeometry(400, 400, 800, 650)

        self.stack_layout = QStackedLayout()

        self.home_widget = self.create_home_page()
        self.account_widget = AccountCreationPage(self)
        self.login_widget = LoginPage(self)

        self.stack_layout.addWidget(self.home_widget)
        self.stack_layout.addWidget(self.account_widget)
        self.stack_layout.addWidget(self.login_widget)

        self.setLayout(self.stack_layout)
        self.stack_layout.setCurrentIndex(0)

    def create_home_page(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        button1 = QPushButton("Créer un compte")
        button1.clicked.connect(lambda: self.stack_layout.setCurrentIndex(1))

        button2 = QPushButton("Connexion")
        button2.clicked.connect(lambda: self.stack_layout.setCurrentIndex(2))

        layout.addWidget(button1)
        layout.addWidget(button2)

        container = QWidget()
        container.setLayout(layout)
        return container

class AccountCreationPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        submit_button = QPushButton("Créer le compte")
        submit_button.clicked.connect(self.create_account)

        layout.addWidget(QLabel("Identifiant:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Mot de passe:"))
        layout.addWidget(self.password_input)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def create_account(self):
        user_data.username = self.username_input.text()
        user_data.password = self.password_input.text()
        user_data.save_to_file()
        self.main_window.stack_layout.setCurrentIndex(0)

class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Se connecter")
        login_button.clicked.connect(self.login)

        layout.addWidget(QLabel("Identifiant:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Mot de passe:"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):
        input_username = self.username_input.text()
        input_password = self.password_input.text()

        user_data.username = input_username
        user_data.load_from_file()

        if input_password == user_data.password:
            QMessageBox.information(self, "Succès", "Connexion réussie !")
        else:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setText("Identifiant ou mot de passe incorrect!")
            error_message.setWindowTitle("Erreur de connexion")
            error_message.exec_()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

