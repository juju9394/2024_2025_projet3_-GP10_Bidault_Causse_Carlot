import pytesseract
from PIL import Image
import re
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from Data_ingredients import*
# 1. Extraire le texte de l'image avec Tesseract OCR
def extraire_texte_image(image_path):
    img = Image.open(image_path)
    texte = pytesseract.image_to_string(img)
    return texte

# 2. Nettoyage du texte extrait
def nettoyage_texte(texte):
    texte = re.sub(r'[^a-zA-Zéàèôùïêâîô]+', ' ', texte)
    texte = re.sub(r'\s+', ' ', texte)
    return texte.lower()

# 3. Préparation du modèle de classification des aliments
def entrainer_modele(data):
    # Séparer les données en caractéristiques et étiquettes
    X = data['aliment']
    y = data['categorie']

    # Séparation des données en jeu d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Création d'un pipeline avec TF-IDF et SVM
    model = make_pipeline(TfidfVectorizer(), SVC())

    # Entraîner le modèle
    model.fit(X_train, y_train)

    return model

# 4. Classification des mots extraits du ticket de caisse
def classifier_mots(mots, model):
    categories = model.predict(mots)
    return categories

# 5. Mise à jour de la base de données
def mettre_a_jour_base_de_donnees(mots, categories):
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('base_de_donnees.db')
    cursor = conn.cursor()

    # Créer la table si elle n'existe pas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aliments (
        nom TEXT,
        categorie TEXT
    )
    ''')

    # Insérer les mots et leurs catégories
    for mot, categorie in zip(mots, categories):
        cursor.execute("INSERT INTO aliments (nom, categorie) VALUES (?, ?)", (mot, categorie))

    # Commit et fermeture de la connexion
    conn.commit()
    conn.close()

# 6. Fonction principale pour traiter l'image
def traiter_ticket(image_path, data):
    # Extraire et nettoyer le texte de l'image
    texte = extraire_texte_image(image_path)
    texte_nettoye = nettoyage_texte(texte)
    
    # Extraire les mots du texte
    mots_du_ticket = texte_nettoye.split()

    # Entraîner le modèle avec les données chargées
    model = entrainer_modele(data)

    # Classifier les mots extraits
    categories = classifier_mots(mots_du_ticket, model)

    # Mettre à jour la base de données avec les mots et catégories
    mettre_a_jour_base_de_donnees(mots_du_ticket, categories)

    # Afficher les résultats
    for mot, categorie in zip(mots_du_ticket, categories):
        print(f"{mot} -> {categorie}")

# 7. Importer les données d'aliments et catégories à partir d'un fichier
def importer_donnees(fichier_path):
    # Exemple d'importation depuis un fichier CSV
    # Le fichier doit avoir deux colonnes : 'aliment' et 'categorie'
    data = pd.read_csv(fichier_path)
    return data

# Exemple d'utilisation
if __name__ == "__main__":
    image_path = 'ticket_de_caisse.jpg'  # Remplace par le chemin de ton image
    fichier_donnees = 'nvbase.csv'  # Remplace par le chemin de ton fichier CSV contenant les aliments et catégories

    # Importer les données
    data = importer_donnees(fichier_donnees)

    # Traiter l'image avec les données importées
    traiter_ticket(image_path, data)
