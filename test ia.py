from PIL import Image
import pytesseract

# Si tesseract n'est pas dans le PATH, vous devez spécifier son chemin
# Exemple : pour Windows, le chemin peut être quelque chose comme "C:/Program Files/Tesseract-OCR/tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Mettez le chemin correct ici

def extraire_texte(image_path):
    # Ouvrir l'image
    image = Image.open(image_path)
    
    # Utiliser pytesseract pour extraire le texte
    texte = pytesseract.image_to_string(image)
    
    return texte

# Exemple d'utilisation
image_path = 'chemin/vers/votre/image.png'  # Remplacez par le chemin de votre image
texte_extrait = extraire_texte(image_path)

print("Texte extrait de l'image :")
print(texte_extrait)
