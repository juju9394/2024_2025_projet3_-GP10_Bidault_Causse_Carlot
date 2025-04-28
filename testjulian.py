# testjulian.py

import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit,
                             QLabel, QMessageBox, QInputDialog, QStackedLayout)
from PyQt5.QtCore import Qt
from data_recette import recettes


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
        layout.setSpacing(20)

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
        layout.setSpacing(20)

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
        layout.setSpacing(20)

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

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(25)

        self.button1 = QPushButton("Ajouter des ingrédients")
        self.button1.clicked.connect(self.add_ingredient)

        self.button2 = QPushButton("Mon Frigo")
        self.button2.clicked.connect(self.main_window.go_to_frigo)

        self.recipe_button = QPushButton("Proposer une recette")
        self.recipe_button.clicked.connect(self.proposer_recette)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.recipe_button)

        self.recette_container = QWidget()
        self.recette_layout = QVBoxLayout()
        self.recette_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.recette_container.setLayout(self.recette_layout)

        self.layout.addWidget(self.recette_container)

        self.back_button = QPushButton("Retour")
        self.back_button.clicked.connect(self.retour_menu)
        self.back_button.hide()
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def add_ingredient(self):
        ingredient, ok = QInputDialog.getText(self, "Ajouter un ingrédient", "Nom de l'ingrédient:")
        if ok and ingredient:
            quantity, ok1 = QInputDialog.getDouble(self, "Quantité", "Quantité:", decimals=2)
            if ok1 and quantity > 0:
                units = ["g", "kg", "unités", "litres", "ml", "cuillères à soupe", "cuillères à café"]
                unit, ok2 = QInputDialog.getItem(self, "Unité", "Unité:", units, 0, False)
                if ok2:
                    user_data.ingredients.append({"name": ingredient, "quantity": quantity, "unit": unit})
                    user_data.save_to_file()
            else:
                QMessageBox.warning(self, "Erreur", "La quantité doit être supérieure à 0.")        

    def proposer_recette(self):
        self.button1.hide()
        self.button2.hide()
        self.recipe_button.hide()

        for i in reversed(range(self.recette_layout.count())):
            widget = self.recette_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for recette in recettes:
            recette_card = QPushButton(f"🍽️ {recette['nom']} \n⏲️ {recette['temps_cuisson']}")
            recette_card.setStyleSheet("""
                QPushButton {
                    background-color: #2a2f4f;
                    border-radius: 15px;
                    padding: 20px;
                    margin: 10px;
                    text-align: left;
                    font-size: 16px;
                    color: #ffffff;
                    min-width: 400px;
                    max-width: 500px;
                }
                QPushButton:hover {
                    background-color: #3e497a;
                }
            """)
            recette_card.clicked.connect(lambda _, r=recette: self.show_recette_detail(r))
            self.recette_layout.addWidget(recette_card)

        self.back_button.show()

    def retour_menu(self):
        self.button1.show()
        self.button2.show()
        self.recipe_button.show()
        self.back_button.hide()

        for i in reversed(range(self.recette_layout.count())):
            widget = self.recette_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def show_recette_detail(self, recette):
        detail_window = QWidget()
        detail_window.setWindowTitle(f"Recette : {recette['nom']}")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>🛒 Ingrédients :</b>"))
        for ingredient, info in recette["ingredients"].items():
            texte = f"- {ingredient.replace('_', ' ').capitalize()} : {info['quantite']} {info['unite']}"
            layout.addWidget(QLabel(texte))

        layout.addWidget(QLabel("\n"))
        layout.addWidget(QLabel("<b>🧑‍🍳 Étapes :</b>"))
        for i, etape in enumerate(recette["etapes"], start=1):
            layout.addWidget(QLabel(f"{i}. {etape}"))

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(detail_window.close)
        layout.addWidget(close_button)

        detail_window.setLayout(layout)
        detail_window.setGeometry(500, 300, 400, 600)
        detail_window.show()
        self.detail_window = detail_window


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
        sorted_ingredients = sorted(user_data.ingredients, key=lambda x: x['name'].lower())

        for ingredient in sorted_ingredients:
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

        sorted_ingredients = sorted(user_data.ingredients, key=lambda x: x['name'].lower())
        items = [f"{i['name']} ({i['quantity']} {i['unit']})" for i in sorted_ingredients]
        item, ok = QInputDialog.getItem(self, "Retirer un ingrédient", "Sélectionnez un ingrédient:", items, 0, False)
        if ok and item:
            index = items.index(item)
            ingredient_to_remove = sorted_ingredients[index]
            user_data.ingredients.remove(ingredient_to_remove)
            user_data.save_to_file()
            self.update_ingredients()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

