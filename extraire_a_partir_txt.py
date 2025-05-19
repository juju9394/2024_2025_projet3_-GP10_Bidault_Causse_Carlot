# Importer le dictionnaire 'ingredients' depuis le fichier ingredients.py
from ingredients import ingredient

# Fonction pour classer les mots
def classer_mots_par_categorie(texte, dico):
    resultat = {categorie: [] for categorie in dico}

    # Séparation du texte en mots
    mots_texte = texte.lower().split()

    # Parcours du texte et classification des mots
    for mot in mots_texte:
        for categorie, mots in dico.items():
            if mot in mots:
                resultat[categorie].append(mot)

    return resultat

# Exemple de texte
texte = "J'aime manger une pomme et une banane, parfois avec un peu de riz ou de pâtes."

# Appeler la fonction avec 'ingredients' qui contient les données importées depuis ingredients.py
resultats = classer_mots_par_categorie(texte, ingredient)

# Afficher les résultats
for categorie, mots in resultats.items():
    print(f"{categorie.capitalize()}: {mots}")
