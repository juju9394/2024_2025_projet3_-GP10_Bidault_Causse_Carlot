# extractor.py
import re
from ingredients import ingredients

def classer_mots_par_categorie(texte):
    resultat = {categorie: [] for categorie in ingredients}
    regex_grammage = re.compile(r'(\d+(?:\.\d+)?)\s*(g|l)\b', re.IGNORECASE)
    mots_texte = texte.lower().split()

    for i, mot in enumerate(mots_texte):
        for categorie, mots in ingredients.items():
            if mot in mots:
                grammage = None
                if i + 1 < len(mots_texte):
                    match = regex_grammage.match(mots_texte[i + 1])
                    if match:
                        grammage = match.group(1)
                        unite = match.group(3).lower()
                        resultat[categorie].append({"name": mot, "quantity": float(grammage), "unit": unite})
                    else:
                        resultat[categorie].append({"name": mot, "quantity": 1, "unit": "unités"})
                else:
                    resultat[categorie].append({"name": mot, "quantity": 1, "unit": "unités"})
    return resultat
