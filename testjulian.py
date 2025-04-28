
import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit,
                             QLabel, QFormLayout, QMessageBox, QInputDialog,
                             QComboBox, QStackedLayout)
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
                self.username = data.get("username", "")
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
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #141e30, stop:1 #243b55);
            color: #f5f5f5;
            font-family: Segoe UI, sans-serif;
            font-size: 17px;
        }
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #43cea2, stop:1 #185a9d);
            color: white;
            border: none;
            padding: 14px 30px;
            font-size: 16px;
            border-radius: 12px;
            min-width: 250px;
            max-width: 250px;
            transition: all 0.3s ease;
        }
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #11998e, stop:1 #38ef7d);
            transform: scale(1.05);
        }
        QPushButton:pressed {
            background-color: #0b486b;
        }
        QLineEdit {
            background-color: #2a2f4f;
            color: #ffffff;
            border: 2px solid #555;
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            min-width: 240px;
            max-width: 240px;
        }
        QLabel {
            font-size: 18px;
            padding: 8px;
        }
    """)


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RECIPEASY")
        self.setGeometry(400, 400, 800, 650)

        self.stack_layout = QStackedLayout()

        self.home_widget = self.create_home_page()
        self.account_widget = AccountCreationPage(self)
        self.login_widget = LoginPage(self)
        self.menu_widget = MenuPage(self)
        self.frigo_widget = FrigoPage(self)

        self.stack_layout.addWidget(self.home_widget)
        self.stack_layout.addWidget(self.account_widget)
        self.stack_layout.addWidget(self.login_widget)
        self.stack_layout.addWidget(self.menu_widget)
        self.stack_layout.addWidget(self.frigo_widget)

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

    def go_to_menu(self):
        self.stack_layout.setCurrentIndex(3)

    def go_to_frigo(self):
        self.frigo_widget.update_ingredients()
        self.stack_layout.setCurrentIndex(4)


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
        user_data.username = self.username_input.text()
        user_data.load_from_file()

        if self.username_input.text() == user_data.username and self.password_input.text() == user_data.password:
            self.main_window.go_to_menu()
        else:
            QMessageBox.critical(self, "Erreur de connexion", "Identifiant ou mot de passe incorrect!")


class MenuPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        button1 = QPushButton("Ajouter des ingrédients")
        button1.clicked.connect(self.add_ingredient)

        button2 = QPushButton("Mon Frigo")
        button2.clicked.connect(self.main_window.go_to_frigo)

        self.recipe_button = QPushButton("Proposer une recette")
        self.recipe_button.clicked.connect(self.proposer_recette)

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(self.recipe_button)

        self.setLayout(layout)

    def add_ingredient(self):
      ingredient, ok = QInputDialog.getText(self, "Ajouter un ingrédient", "Nom de l'ingrédient:")
      if ok and ingredient:
          quantity, ok1 = QInputDialog.getDouble(self, "Quantité", "Quantité:", decimals=2)
          if ok1:
              if quantity <= 0:
                  QMessageBox.warning(self, "Quantité invalide", "La quantité doit être positive.")
                  return
              units = ["g", "kg", "unités", "litres", "ml", "cuilleres à soupe", "cuilleres à café"]
              unit, ok2 = QInputDialog.getItem(self, "Unité", "Unité:", units, 0, False)
              if ok2:
                  user_data.ingredients.append({"name": ingredient, "quantity": quantity, "unit": unit})
                  user_data.save_to_file()


    def proposer_recette(self):
        QMessageBox.information(self, "Recette", "Voici une recette que l'IA te proposera ici !")


class FrigoPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

    def update_ingredients(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.layout.addWidget(QLabel("Ingrédients dans mon frigo:"))
        for ingredient in user_data.ingredients:
            label = QLabel(f"{ingredient['name']} ({ingredient['quantity']} {ingredient['unit']})")
            self.layout.addWidget(label)

        remove_button = QPushButton("Retirer un ingrédient")
        remove_button.clicked.connect(self.remove_ingredient)
        self.layout.addWidget(remove_button)

        back_button = QPushButton("Retour au menu")
        back_button.clicked.connect(self.main_window.go_to_menu)
        self.layout.addWidget(back_button)

    def remove_ingredient(self):
        if not user_data.ingredients:
            QMessageBox.information(self, "Info", "Aucun ingrédient à retirer.")
            return

        items = [f"{i['name']} ({i['quantity']} {i['unit']})" for i in user_data.ingredients]
        item, ok = QInputDialog.getItem(self, "Retirer un ingrédient", "Sélectionnez un ingrédient:", items, 0, False)
        if ok and item:
            index = items.index(item)
            del user_data.ingredients[index]
            user_data.save_to_file()
            self.update_ingredients()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
