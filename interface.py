import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QFormLayout, QMessageBox, QHBoxLayout, QInputDialog, QComboBox
from PyQt5.QtCore import Qt

class UserData:
    """Classe pour stocker les données utilisateur globalement."""
    def __init__(self):
        self.username = ""
        self.password = ""
        self.ingredients = []  # Liste des ingrédients avec leurs quantités

    def save_to_file(self):
        """Enregistrer les informations utilisateur et les ingrédients dans un fichier JSON."""
        data = {
            "username": self.username,
            "password": self.password,
            "ingredients": self.ingredients  # Sauvegarder les ingrédients
        }
        with open(f"{self.username}_data.json", "w") as f:
            json.dump(data, f)

    def load_from_file(self):
        """Charger les informations utilisateur et les ingrédients à partir d'un fichier JSON."""
        try:
            with open(f"{self.username}_data.json", "r") as f:
                data = json.load(f)
                self.username = data.get("username", "")
                self.password = data.get("password", "")
                self.ingredients = data.get("ingredients", [])  # Charger les ingrédients
        except FileNotFoundError:
            pass  # Si le fichier n'existe pas, ne rien faire

user_data = UserData()  # Instance pour stocker les données de l'utilisateur

class BaseWindow(QWidget):
    """Fenêtre de base qui applique le même style à toutes les fenêtres."""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 16px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
            QLineEdit {
                background-color: #555;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
        """)

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interface Moderne")
        self.setGeometry(100, 100, 400, 300)

        # Layout principal pour les boutons
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # Boutons de la page d'accueil
        self.button1 = QPushButton("Créer un compte", self)
        self.button1.setFixedSize(300, 75)
        self.button1.clicked.connect(self.on_click_button1)

        self.button2 = QPushButton("Connexion", self)
        self.button2.setFixedSize(300, 75)
        self.button2.clicked.connect(self.on_click_button2)

        # Ajouter les boutons à l'interface principale
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)

        self.setLayout(self.layout)

    def on_click_button1(self):
        print("Le bouton 'Créer un compte' a été cliqué!")
        self.account_window = AccountCreationWindow()
        self.account_window.show()

    def on_click_button2(self):
        print("Le bouton 'Connexion' a été cliqué!")
        self.login_window = LoginWindow()
        self.login_window.show()

class AccountCreationWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Créer un compte")
        self.setGeometry(100, 100, 400, 250)

        # Création des widgets pour l'interface de création de compte
        self.username_label = QLabel("Identifiant:")
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("Mot de passe:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Pour masquer le mot de passe

        # Création d'un bouton pour valider la création du compte
        self.submit_button = QPushButton("Créer le compte", self)
        self.submit_button.clicked.connect(self.create_account)

        # Layout pour organiser les éléments
        form_layout = QFormLayout()
        form_layout.addRow(self.username_label, self.username_input)
        form_layout.addRow(self.password_label, self.password_input)
        form_layout.addRow(self.submit_button)

        self.setLayout(form_layout)

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Enregistrer les informations dans l'instance UserData
        user_data.username = username
        user_data.password = password

        # Sauvegarder les données utilisateur dans un fichier JSON
        user_data.save_to_file()

        print(f"Compte créé avec l'identifiant: {username} et le mot de passe: {password}")
        self.close()

class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connexion")
        self.setGeometry(100, 100, 400, 250)

        # Création des widgets pour l'interface de connexion
        self.username_label = QLabel("Identifiant:")
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("Mot de passe:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Pour masquer le mot de passe

        # Création d'un bouton pour valider la connexion
        self.login_button = QPushButton("Se connecter", self)
        self.login_button.clicked.connect(self.login)

        # Layout pour organiser les éléments
        form_layout = QFormLayout()
        form_layout.addRow(self.username_label, self.username_input)
        form_layout.addRow(self.password_label, self.password_input)
        form_layout.addRow(self.login_button)

        self.setLayout(form_layout)
        

    def login(self):
        entered_username = self.username_input.text()
        entered_password = self.password_input.text()

        # Charger les données utilisateur depuis le fichier
        user_data.username = entered_username
        user_data.load_from_file()

        # Vérifier si les identifiants sont corrects
        if entered_username == user_data.username and entered_password == user_data.password:
            print("Connexion réussie!")
            # Passer à l'écran de menu après la connexion
            self.menu_window = MenuWindow()
            self.menu_window.show()
            self.close()
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            self.show_error_message()

    def show_error_message(self):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setText("Identifiant ou mot de passe incorrect!")
        error_message.setWindowTitle("Erreur de connexion")
        error_message.exec_()

class MenuWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu d'accueil")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        # Bouton pour ajouter des ingrédients manuellement
        self.ingredients_button = QPushButton("Ajouter des ingrédients manuellement", self)
        self.ingredients_button.setFixedSize(300, 75)
        self.ingredients_button.clicked.connect(self.on_add_ingredients)

        # Bouton pour accéder à "Mon Frigo"
        self.frigo_button = QPushButton("Mon Frigo", self)
        self.frigo_button.setFixedSize(300, 75)
        self.frigo_button.clicked.connect(self.on_click_frigo_button)

        # Ajouter les boutons à l'interface
        self.layout.addWidget(self.ingredients_button)
        self.layout.addWidget(self.frigo_button)

        self.setLayout(self.layout)

    def on_add_ingredients(self):
        print("Ajouter des ingrédients manuellement")
        ingredient, ok = QInputDialog.getText(self, "Ajouter un ingrédient", "Nom de l'ingrédient:")
        if ok and ingredient:
            # Demander la quantité de l'ingrédient
            quantity, unit, unit_ok = self.get_ingredient_quantity()
            if unit_ok:
                user_data.ingredients.append({"name": ingredient, "quantity": quantity, "unit": unit})  # Ajouter l'ingrédient avec la quantité
                user_data.save_to_file()  # Sauvegarder la liste mise à jour
                print(f"Ingrédient ajouté: {ingredient} ({quantity} {unit})")

    def get_ingredient_quantity(self):
        # Demander la quantité
        quantity, ok = QInputDialog.getDouble(self, "Quantité", "Quantité de l'ingrédient:", decimals=2)
        if not ok:
            return None, None, False

        # Demander l'unité
        units = ["g", "kg", "unités"]
        unit, unit_ok = QInputDialog.getItem(self, "Unité", "Choisissez l'unité:", units, 0, False)
        if not unit_ok:
            return None, None, False

        return quantity, unit, True

    def on_click_frigo_button(self):
        print("Le bouton 'Mon Frigo' a été cliqué!")
        self.frigo_window = FrigoWindow()
        self.frigo_window.show()
        # self.close()  # Fermer la fenêtre principale

class FrigoWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mon Frigo")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        # Afficher la liste des ingrédients
        self.ingredients_label = QLabel("Ingrédients dans mon frigo:")
        self.layout.addWidget(self.ingredients_label)
        print (f"user_data.ingredients = {user_data.ingredients}")
        for ingredient in user_data.ingredients: 
            print(f"ingredient = {ingredient}")
            ingredient_label = QLabel(f"{ingredient['name']} ({ingredient['quantity']} {ingredient['unit']})")
            self.layout.addWidget(ingredient_label)

        # Ajouter un bouton pour revenir au menu
        self.back_button = QPushButton("Retour au menu", self)
        self.back_button.setFixedSize(300, 75)
        self.back_button.clicked.connect(self.on_back_button)

        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def on_back_button(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

