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

# Ouvrir une image
image = Image.open('file:///H:/Documents/Nsi/ticket_de_caisse.jpg')

# Appliquer des modifications à l'image (conversion en noir et blanc par exemple)
bw_image = image.convert('L')

# Sauvegarder l'image modifiée
bw_image.save('image_bw.jpg')
