# from PIL import Image
# import tesseract

# # Si tesseract n'est pas dans le PATH, vous devez spécifier son chemin
# # Exemple : pour Windows, le chemin peut être quelque chose comme "C:/Program Files/Tesseract-OCR/tesseract.exe"
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Mettez le chemin correct ici

# def extraire_texte(image_path):
#     # Ouvrir l'image
#     image = Image.open(image_path)
    
#     # Utiliser pytesseract pour extraire le texte
#     texte = pytesseract.image_to_string(image)
    
#     return texte

# # Exemple d'utilisation
# image_path = 'ticket de caisse.jpg'  # Remplacez par le chemin de votre image
# texte_extrait = extraire_texte(image_path)

# print ("Texte extrait de l'image :{texte_extrait}")

import easyocr

reader = easyocr.Reader(['fr'])

# Lire une image
result = reader.readtext('image_avec_aliments.jpg')

# Liste des aliments que tu veux détecter
aliments = ["pain", "tomate", "pomme", "riz", "fromage", ...]

# Filtrer les résultats pour ne garder que les mots d'aliments
for (bbox, text, prob) in result:
    if any(aliment.lower() in text.lower() for aliment in aliments):
        print("Aliment trouvé:", text)
