import numpy as np
import pandas as pd
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Reshape, LSTM, Dense, Dropout
from keras.layers import Bidirectional
import os
import pytesseract

# Fonction pour charger et prétraiter les images
def preprocess_image(image_path, target_size=(128, 128)):
    # Charger l'image
    image = Image.open(image_path)
    
    # Convertir l'image en noir et blanc (Luminance)
    bw_image = image.convert('L')
    
    # Redimensionner l'image
    bw_image = bw_image.resize(target_size)
    
    # Normalisation des pixels (entre 0 et 1)
    image_array = np.array(bw_image) / 255.0
    return image_array

# Fonction pour créer le modèle CRNN
def create_crnn_model(input_shape=(128, 128, 1), num_classes=100):
    model = Sequential()

    # Couches Convolutives pour extraire des caractéristiques de l'image
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # Reshaping pour rendre compatible avec les LSTM
    model.add(Reshape(target_shape=(-1, 64)))

    # Couches récurrentes pour gérer les séquences (LSTM)
    model.add(Bidirectional(LSTM(128, return_sequences=True)))
    model.add(Dropout(0.25))

    # Couches de sortie pour prédire les caractères (par exemple, 100 classes de caractères possibles)
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Charger et préparer les données
def load_data(image_folder, labels_file):
    # Charger les étiquettes à partir d'un fichier CSV
    labels_df = pd.read_csv(labels_file)
    
    images = []
    labels = []
    
    # Pour chaque image, charger et prétraiter l'image
    for index, row in labels_df.iterrows():
        image_path = os.path.join(image_folder, row['image_name'])
        image = preprocess_image(image_path)
        images.append(image)
        labels.append(row['text'])
    
    # Convertir en tableau numpy
    images = np.array(images)
    
    # Encoder les textes (étiquettes) en entiers
    encoder = LabelEncoder()
    encoder.fit(list(''.join(labels)))  # Encoder tous les caractères
    encoded_labels = [encoder.transform(list(text)) for text in labels]
    
    return images, encoded_labels, encoder

# Fonction d'entraînement du modèle
def train_model(images, encoded_labels, model):
    # Ajuster les données pour correspondre au format d'entrée du modèle (en particulier la forme de X_train)
    X_train = np.expand_dims(images, axis=-1)  # Ajouter un canal (noir et blanc)

    # Ajouter un padding sur les séquences d'étiquettes pour avoir la même longueur (si nécessaire)
    max_label_length = max([len(label) for label in encoded_labels])
    y_train = np.array([np.pad(label, (0, max_label_length - len(label)), mode='constant') for label in encoded_labels])

    # Entraîner le modèle
    model.fit(X_train, y_train, batch_size=32, epochs=10)

# # Fonction principale
# def main():
#     # Répertoire des images et fichier des étiquettes
#     image_folder = 'images/'  # Dossier des images
#     labels_file = 'labels.csv'  # Fichier CSV des étiquettes
    
#     # Charger les données
#     images, encoded_labels, encoder = load_data(image_folder, labels_file)
    
#     # Créer le modèle CRNN
#     model = create_crnn_model(input_shape=(128, 128, 1), num_classes=len(encoder.classes_))
    
#     # Entraîner le modèle
#     train_model(images, encoded_labels, model)
    
#     # Sauvegarder le modèle
#     model.save('ocr_model.h5')

# # Lancer le programme
0


