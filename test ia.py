# from PIL import Image
# import tesseract




# print ("Texte extrait de l'image :{texte_extrait}")

# import easyocr

# reader = easyocr.Reader(['fr'])

# # Lire une image
# result = reader.readtext('image_avec_aliments.jpg')

# # Liste des aliments que tu veux détecter
# aliments = ["pain", "tomate", "pomme", "riz", "fromage", ...]

# # Filtrer les résultats pour ne garder que les mots d'aliments
# for (bbox, text, prob) in result:
#     if any(aliment.lower() in text.lower() for aliment in aliments):
#         print("Aliment trouvé:", text)
from PIL import Image
import numpy as np

# Charger l'image
image = Image.open('ticket_de_caisse.jpg')

# Redimensionner l'image (par exemple à 128x128 pixels)
image = image.resize((128, 128))

# Convertir l'image en niveaux de gris
bw_image = image.convert('L')

# Normalisation des pixels (valeurs entre 0 et 1)
bw_image = np.array(bw_image) / 255.0

# Sauvegarder ou passer à l'étape suivante
