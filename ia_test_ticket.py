import sys
import cv2
import tesseract
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import re

# Liste des ingrédients recherchés
ingredients_connus = ['lait', 'oeuf', 'farine', 'sucre', 'sel', 'beurre', 'huile',
                      'riz', 'poulet', 'thon', 'yaourt', 'fromage', 'crème', 'miel',
                      'jambon', 'chocolat', 'tomate', 'pain']

class TicketScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Détecteur d'ingrédients - Ticket de caisse")
        self.resize(500, 600)

        self.label = QLabel("Charge une photo de ton ticket de caisse")
        self.image_label = QLabel()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        self.button = QPushButton("Charger une image")
        self.button.clicked.connect(self.load_image)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.button)
        layout.addWidget(self.text_area)

        self.setLayout(layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir l'image", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            image = cv2.imread(file_name)
            self.show_image(image)
            text = pytesseract.image_to_string(image)
            produits = self.clean_text(text)
            ingredients_trouves = self.extract_ingredients(produits)
            self.text_area.setText("\n".join(ingredients_trouves))

    def show_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = image_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(image_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image).scaled(400, 400, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def clean_text(self, text):
        lignes = text.split('\n')
        produits = [ligne.strip() for ligne in lignes if re.search(r'[a-zA-Z]', ligne)]
        return produits

    def extract_ingredients(self, produits):
        ingredients_trouves = set()
        for produit in produits:
            for ingr in ingredients_connus:
                if ingr.lower() in produit.lower():
                    ingredients_trouves.add(ingr)
        return list(ingredients_trouves)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicketScanner()
    window.show()
    sys.exit(app.exec_())
