# Importer le dictionnaire 'ingredients' depuis le fichier ingredients.py
from ingredients import ingredients
import re

# Fonction pour classer les mots et détecter le grammage (uniquement g et l)
def classer_mots_par_categorie(texte, dico):
    resultat = {categorie: [] for categorie in dico}
    
    # Expression régulière pour capturer un grammage en grammes (g) ou litres (l)
    regex_grammage = re.compile(r'(\d+(\.\d+)?)\s*(g|l)', re.IGNORECASE)

    mots_texte = texte.lower().split()
    for i, mot in enumerate(mots_texte):
        # Vérifier si le mot est un ingrédient
        for categorie, mots in dico.items():
            if mot in mots:
                # Si un grammage suit l'ingrédient, l'ajouter à la liste
                grammage = None
                if i + 1 < len(mots_texte):
                    next_mot = mots_texte[i + 1]
                    match = regex_grammage.search(next_mot)
                    if match:
                        grammage = match.group(0)

                # Ajouter l'ingrédient et son grammage s'il y en a
                if grammage:
                    resultat[categorie].append((mot, grammage))
                else:
                    resultat[categorie].append((mot,))

    return resultat

# Exemple de texte
texte = "J'ai acheté 500g de pomme, 2l de jus, et 1l de lait."

# Appeler la fonction avec 'ingredients'
resultats = classer_mots_par_categorie(texte, ingredients)

# Afficher les résultats
for categorie, mots in resultats.items():
    print(f"{categorie.capitalize()}: {mots}")
