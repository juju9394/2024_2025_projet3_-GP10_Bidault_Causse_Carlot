import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit,
                             QLabel, QMessageBox, QInputDialog, QStackedLayout, QScrollArea,
                             QHBoxLayout)
from PyQt5.QtCore import Qt
from data_recette import recettes
import subprocess
import os 

class UserData:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.ingredients = []

    def save_to_file(self):
        
        if not os.path.exists("user_data"):
            os.makedirs("user_data")
        data = {
            "username": self.username,
            "password": self.password,
            "ingredients": self.ingredients
        }
        with open(f"user_data/{self.username}_data.json", "w") as f:
            json.dump(data, f)

    def load_from_file(self):
        try:
            with open(f"user_data/{self.username}_data.json", "r") as f:
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
            font-family: 'Segoe UI', sans-serif;
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
        }
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #11998e, stop:1 #38ef7d);
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
            color: #e0e0e0;
        }
        QMessageBox {
            background-color: #243b55;
            color: #f5f5f5;
            font-size: 16px;
        }
        QMessageBox QPushButton {
            background-color: #185a9d;
            color: white;
            border-radius: 5px;
            padding: 8px 15px;
            font-size: 14px;
            min-width: 80px;
            max-width: 150px;
        }
        QMessageBox QPushButton:hover {
            background-color: #43cea2;
        }
        QInputDialog {
            background-color: #243b55;
            color: #f5f5f5;
            font-size: 16px;
        }
        QInputDialog QLineEdit {
            background-color: #2a2f4f;
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px;
        }
        QInputDialog QPushButton {
            background-color: #185a9d;
            color: white;
            border-radius: 5px;
            padding: 8px 15px;
            font-size: 14px;
            min-width: 80px;
            max-width: 150px;
        }
        QInputDialog QPushButton:hover {
            background-color: #43cea2;
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
        self.username_input.setPlaceholderText("Entrez votre identifiant")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Entrez votre mot de passe")

        submit_button = QPushButton("Créer le compte")
        submit_button.clicked.connect(self.create_account)

        layout.addWidget(QLabel("Créer un compte"))
        layout.addWidget(QLabel("Identifiant:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Mot de passe:"))
        layout.addWidget(self.password_input)
        layout.addWidget(submit_button)

        back_button = QPushButton("Retour")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                color: white;
                min-width: 120px;
                max-width: 120px;
            }
            QPushButton:hover {
                background-color: #ff1c1c;
            }
        """)
        back_button.clicked.connect(lambda: self.main_window.stack_layout.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)


        self.setLayout(layout)

    def create_account(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        
        temp_user_data = UserData()
        temp_user_data.username = username
        temp_user_data.load_from_file()
        if temp_user_data.password: 
            QMessageBox.warning(self, "Erreur", "Cet identifiant existe déjà. Veuillez en choisir un autre.")
            return

        user_data.username = username
        user_data.password = password
        user_data.save_to_file()
        QMessageBox.information(self, "Succès", "Compte créé avec succès !")
        self.main_window.stack_layout.setCurrentIndex(0)


class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Entrez votre identifiant")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Entrez votre mot de passe")

        login_button = QPushButton("Se connecter")
        login_button.clicked.connect(self.login)

        layout.addWidget(QLabel("Connexion"))
        layout.addWidget(QLabel("Identifiant:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Mot de passe:"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        back_button = QPushButton("Retour")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                color: white;
                min-width: 120px;
                max-width: 120px;
            }
            QPushButton:hover {
                background-color: #ff1c1c;
            }
        """)
        back_button.clicked.connect(lambda: self.main_window.stack_layout.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def login(self):
        input_username = self.username_input.text().strip()
        input_password = self.password_input.text().strip()

        if not input_username or not input_password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        user_data.username = input_username
        user_data.load_from_file()

        if user_data.username == input_username and user_data.password == input_password:
            QMessageBox.information(self, "Succès", f"Bienvenue, {user_data.username} !")
            self.main_window.go_to_menu()
        else:
            QMessageBox.critical(self, "Erreur de connexion", "Identifiant ou mot de passe incorrect!")


class MenuPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(25)

        
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignCenter)
        self.buttons_layout.setSpacing(20)

        self.button1 = QPushButton("Ajouter des ingrédients manuellement")
        self.button1.clicked.connect(self.add_ingredient)

        self.button2 = QPushButton("Mon Frigo")
        self.button2.clicked.connect(self.main_window.go_to_frigo)

        self.button3 = QPushButton("Joindre une photo (Détection AI)")
        self.button3.clicked.connect(self.joindre_photo)

        self.recipe_button = QPushButton("Proposer une recette")
        self.recipe_button.clicked.connect(self.proposer_recette)

        self.buttons_layout.addWidget(self.button1)
        self.buttons_layout.addWidget(self.button2)
        self.buttons_layout.addWidget(self.button3)
        self.buttons_layout.addWidget(self.recipe_button)

        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(self.buttons_layout)
        self.main_layout.addWidget(self.buttons_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.hide()

        self.recette_container = QWidget()
        self.recette_layout = QVBoxLayout()
        self.recette_layout.setAlignment(Qt.AlignTop)
        self.recette_container.setLayout(self.recette_layout)
        self.scroll_area.setWidget(self.recette_container)

        self.main_layout.addWidget(self.scroll_area)

        self.back_button_recettes = QPushButton("Retour au menu")
        self.back_button_recettes.clicked.connect(self.retour_menu)
        self.back_button_recettes.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                color: white;
                min-width: 120px;
                max-width: 150px;
            }
            QPushButton:hover {
                background-color: #ff1c1c;
            }
        """)
        self.recette_layout.addWidget(self.back_button_recettes, alignment=Qt.AlignCenter)
        self.back_button_recettes.hide()

        self.setLayout(self.main_layout)

    def joindre_photo(self):
        chemin, ok = QInputDialog.getText(self, "Joindre une photo", "Entrez le chemin d'accès à la photo :")
        if ok and chemin:
            if not os.path.exists(chemin):
                QMessageBox.warning(self, "Erreur", "Le fichier image spécifié n'existe pas.")
                return

            try:
                
                script_path = r"C:\Users\bidau\Documents\GitHub\2024_2025_projet3_-GP10_Bidault_Causse_Carlot\test1.py"
                
                script_path = os.path.abspath(script_path)

                
                if not os.path.exists(script_path):
                    QMessageBox.critical(self, "Erreur", f"Le script AI '{script_path}' est introuvable. Veuillez vérifier le chemin.")
                    return

                
                process = subprocess.Popen([sys.executable, script_path, chemin])
                process.wait() 

                
                result_file_path = "resultat_prediction.json"
                if not os.path.exists(result_file_path):
                    QMessageBox.critical(self, "Erreur", "Le fichier de résultat de l'IA est introuvable. Le script AI a peut-être échoué.")
                    return

                with open(result_file_path, "r") as f:
                    result_data = json.load(f)
                    prediction_raw = result_data.get("prediction", "Inconnu (confiance 0.00)")

                
                
                if "Inconnu" in prediction_raw:
                    QMessageBox.information(self, "Résultat de la Détection",
                                            f"L'IA n'a pas pu identifier le fruit avec une confiance suffisante.\n{prediction_raw}")
                    
                    add_manually_reply = QMessageBox.question(self, "Action requise",
                                                              "Voulez-vous ajouter cet ingrédient manuellement ?",
                                                              QMessageBox.Yes | QMessageBox.No)
                    if add_manually_reply == QMessageBox.Yes:
                        self.add_ingredient()
                else:
                   
                    parts = prediction_raw.split(' (')
                    fruit_name = parts[0]
                    confidence_str = parts[1][:-2] 
                    confidence = float(confidence_str) / 100

                    reply = QMessageBox.question(self, "Résultat de la Détection",
                                                 f"Fruit détecté : {fruit_name} (Confiance : {confidence*100:.1f}%)\n"
                                                 f"Souhaitez-vous l'ajouter au frigo ?",
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        
                        user_data.ingredients.append({"name": fruit_name, "quantity": 1.0, "unit": "unités"})
                        user_data.save_to_file()
                        QMessageBox.information(self, "Ajouté", f"{fruit_name} ajouté au frigo avec succès.")
                    else:
                        QMessageBox.information(self, "Annulé", "Ajout annulé.")

            except Exception as e:
                QMessageBox.critical(self, "Erreur lors du traitement de l'image", f"Une erreur est survenue : {e}")

    def add_ingredient(self):
        ingredient, ok = QInputDialog.getText(self, "Ajouter un ingrédient", "Nom de l'ingrédient:")
        if ok and ingredient.strip():
            quantity, ok1 = QInputDialog.getDouble(self, "Quantité", f"Quantité de {ingredient.strip()}:", decimals=2)
            if ok1 and quantity > 0:
                units = ["g", "unités", "ml", "kg", "litres"] 
                unit, ok2 = QInputDialog.getItem(self, "Unité", "Unité:", units, 0, False)
                if ok2:
                    user_data.ingredients.append({"name": ingredient.strip(), "quantity": quantity, "unit": unit})
                    user_data.save_to_file()
                    QMessageBox.information(self, "Succès", f"{ingredient.strip()} ajouté au frigo.")
            else:
                QMessageBox.warning(self, "Erreur", "La quantité doit être supérieure à 0.")
        elif ok and not ingredient.strip():
            QMessageBox.warning(self, "Erreur", "Le nom de l'ingrédient ne peut pas être vide.")


    def proposer_recette(self):
        self.buttons_widget.hide()
        self.scroll_area.show()

        
        while self.recette_layout.count() > 1: 
            item = self.recette_layout.takeAt(0) 
            if item.widget() and item.widget() != self.back_button_recettes: 
                item.widget().deleteLater()

        self.back_button_recettes.show()

        
        if not recettes:
            no_recipe_label = QLabel("Aucune recette disponible pour le moment.")
            no_recipe_label.setAlignment(Qt.AlignCenter)
            self.recette_layout.addWidget(no_recipe_label)
        else:
            for recette in recettes:
                recette_text = f"🍽️ {recette['nom']} \n⏲️ {recette['temps_cuisson']} \n👥 {recette['personnes']} personnes"

                recette_card = QPushButton(recette_text)
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
                self.recette_layout.addWidget(recette_card, alignment=Qt.AlignCenter)

        
        self.recette_layout.addWidget(self.back_button_recettes, alignment=Qt.AlignCenter)


    def retour_menu(self):
        self.scroll_area.hide()
        self.buttons_widget.show()
        self.back_button_recettes.hide()

        
        while self.recette_layout.count() > 0: 
            item = self.recette_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        
        self.recette_layout.addWidget(self.back_button_recettes, alignment=Qt.AlignCenter)


    def show_recette_detail(self, recette):
        detail_window = QWidget()
        detail_window.setWindowTitle(f"Recette : {recette['nom']}")
        layout = QVBoxLayout()
        layout.setSpacing(10)

       
        title_label = QLabel(f"<h2 style='color:#43cea2;'>{recette['nom']}</h2>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        
        info_layout = QHBoxLayout()
        info_layout.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(QLabel(f"<b>⏲️ Temps de cuisson :</b> {recette['temps_cuisson']}"))
        info_layout.addWidget(QLabel(f"<b>👥 Pour :</b> {recette['personnes']} personnes"))
        layout.addLayout(info_layout)

        layout.addWidget(QLabel("<br><b>🛒 Ingrédients :</b>"))
        for ingredient, info in recette["ingredients"].items():
            ingredient_label = QLabel(f"- {ingredient.replace('_', ' ').capitalize()} : {info['quantite']} {info['unite']}")
            layout.addWidget(ingredient_label)

        layout.addWidget(QLabel("<br><b>🧑‍🍳 Étapes :</b>"))
        for i, etape in enumerate(recette["etapes"], start=1):
            etape_label = QLabel(f"{i}. {etape}")
            etape_label.setWordWrap(True) 
            layout.addWidget(etape_label)

        def valider_recette():
            manquants = []
            for ing, info in recette["ingredients"].items():
                ing_normalise = ing.lower().replace("_", " ").strip()
                found = False
                for stock in user_data.ingredients:
                    if stock["name"].lower().strip() == ing_normalise and stock["unit"].lower().strip() == info["unite"].lower().strip():
                        if stock["quantity"] >= info["quantite"]:
                            found = True
                            break
                if not found:
                    manquants.append(ing_normalise)

            if manquants:
                QMessageBox.warning(detail_window, "Ingrédients manquants", f"Ingrédients insuffisants :\n- {', '.join([m.capitalize() for m in manquants])}\n\nVoulez-vous quand même valider la recette ? (Cela ne mettra pas à jour votre frigo)")
                
                reply_missing = QMessageBox.question(detail_window, "Confirmation", "Voulez-vous quand même valider la recette ? (Les ingrédients ne seront pas déduits du frigo)",
                                                    QMessageBox.Yes | QMessageBox.No)
                if reply_missing == QMessageBox.Yes:
                    QMessageBox.information(detail_window, "Recette Validée", "Recette validée (ingrédients non déduits). Profitez bien !")
                    detail_window.close()
                return

            
            for ing, info in recette["ingredients"].items():
                ing_normalise = ing.lower().replace("_", " ").strip()
                for stock in user_data.ingredients:
                    if stock["name"].lower().strip() == ing_normalise and stock["unit"].lower().strip() == info["unite"].lower().strip():
                        stock["quantity"] -= info["quantite"]
                        break 

            
            user_data.ingredients = [ing for ing in user_data.ingredients if ing["quantity"] > 0]

            user_data.save_to_file()
            QMessageBox.information(detail_window, "Succès", "Recette validée et ingrédients mis à jour !")
            self.main_window.frigo_widget.update_ingredients()
            detail_window.close()


        valider_button = QPushButton("Valider la recette")
        valider_button.clicked.connect(valider_recette)
        layout.addWidget(valider_button)

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(detail_window.close)
        layout.addWidget(close_button)

        detail_window.setLayout(layout)
        detail_window.setGeometry(500, 300, 500, 700) 
        detail_window.show()
        self.detail_window = detail_window 


class FrigoPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.ingredient_list_widget = QWidget()
        self.ingredient_list_layout = QVBoxLayout()
        self.ingredient_list_layout.setAlignment(Qt.AlignTop)
        self.ingredient_list_widget.setLayout(self.ingredient_list_layout)
        self.scroll_area.setWidget(self.ingredient_list_widget)

        self.main_layout.addWidget(self.scroll_area)

        
        self.button_layout = QHBoxLayout()
        self.remove_button = QPushButton("Retirer un ingrédient")
        self.remove_button.clicked.connect(self.remove_ingredient)
        self.button_layout.addWidget(self.remove_button)

        self.back_button = QPushButton("Retour au menu")
        self.back_button.clicked.connect(self.main_window.go_to_menu)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                color: white;
                min-width: 120px;
                max-width: 150px;
            }
            QPushButton:hover {
                background-color: #ff1c1c;
            }
        """)
        self.button_layout.addWidget(self.back_button)

        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)


    def update_ingredients(self):
      
        for i in reversed(range(self.ingredient_list_layout.count())):
            widget = self.ingredient_list_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.ingredient_list_layout.addWidget(QLabel("<b>Ingrédients dans mon frigo :</b>"))
        sorted_ingredients = sorted(user_data.ingredients, key=lambda x: x['name'].lower())

        if not sorted_ingredients:
            self.ingredient_list_layout.addWidget(QLabel("Votre frigo est vide. Ajoutez des ingrédients !"))
        else:
            for ingredient in sorted_ingredients:
                label = QLabel(f"• {ingredient['name'].capitalize()} ({ingredient['quantity']} {ingredient['unit']})")
                self.ingredient_list_layout.addWidget(label)


    def remove_ingredient(self):
        if not user_data.ingredients:
            QMessageBox.information(self, "Info", "Aucun ingrédient à retirer.")
            return

        sorted_ingredients = sorted(user_data.ingredients, key=lambda x: x['name'].lower())
        items = [f"{i['name'].capitalize()} ({i['quantity']} {i['unit']})" for i in sorted_ingredients]
        item, ok = QInputDialog.getItem(self, "Retirer un ingrédient", "Sélectionnez un ingrédient à retirer:", items, 0, False)
        if ok and item:
            index = items.index(item)
            ingredient_to_remove = sorted_ingredients[index]

           
            if ingredient_to_remove['unit'] != 'unités' and ingredient_to_remove['quantity'] > 1:
                quantity_to_remove, ok_q = QInputDialog.getDouble(self, "Quantité à retirer",
                                                                 f"Quantité de {ingredient_to_remove['name']} à retirer (max {ingredient_to_remove['quantity']}):",
                                                                 decimals=2,
                                                                 value=ingredient_to_remove['quantity'],
                                                                 min=0.01,
                                                                 max=ingredient_to_remove['quantity'])
                if ok_q and quantity_to_remove > 0:
                    ingredient_to_remove['quantity'] -= quantity_to_remove
                    if ingredient_to_remove['quantity'] <= 0:
                        user_data.ingredients.remove(ingredient_to_remove)
                        QMessageBox.information(self, "Retiré", f"Tout le/la {ingredient_to_remove['name']} a été retiré(e).")
                    else:
                        QMessageBox.information(self, "Mis à jour", f"{quantity_to_remove} {ingredient_to_remove['unit']} de {ingredient_to_remove['name']} retiré(e).")
                elif ok_q and quantity_to_remove <= 0:
                    QMessageBox.warning(self, "Erreur", "La quantité à retirer doit être supérieure à 0.")
                    return
                else:
                    return
            else: 
                user_data.ingredients.remove(ingredient_to_remove)
                QMessageBox.information(self, "Retiré", f"{ingredient_to_remove['name']} a été retiré(e) de votre frigo.")

            user_data.save_to_file()
            self.update_ingredients() 


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

 