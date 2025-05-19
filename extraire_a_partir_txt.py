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


texte = "Bien sûr, voici le **ticket de caisse très long** en une seule ligne, comme demandé :🧾 HYPERMARCHÉ SUPERPLUS pomme - 123 Avenue de la République - 75000 Paris - SIRET : 123 456 789 00000 - Tel : 01 23 45 67 89 - Merci de votre visite ! - Date : 19/05/2025 - Heure : 14:36 - Caisse : 03 — Hôte(sse) : Pauline - Ticket : 00012875 - Articles : 2x Pâtes 500g 2,58 € ; 1x Sauce tomate basilic 300g 1,49 € ; 1x Huile d'olive vierge extra 1L 6,89 € ; 1x Pain de mie complet 500g 1,35 € ; 3x Yaourts nature 4x125g 2,67 € ; 1x Lait demi-écrémé 1L 0,89 € ; 1x Camembert AOP 250g 2,19 € ; 1x Beurre doux 250g 1,89 € ; 2x Steak haché 15% 2x125g 4,98 € ; 1x Pommes golden 1,5kg 3,15 € ; 1x Bananes 1,2kg 2,28 € ; 1x Tomates grappe 1kg 2,79 € ; 1x Carottes bio 1kg 1,99 € ; 1x Jus d'orange 1,5L 2,49 € ; 1x Eau minérale x6 1,5L 3,18 € ; 1x Papier toilette 12 rouleaux 4,99 € ; 1x Liquide vaisselle 750ml 1,65 € ; 1x Lessive liquide 2L 6,49 € ; 1x Éponge x3 1,15 € ; 1x Dentifrice Signal blancheur 2,29 € ; 1x Gel douche Le Petit Marseillais 3,49 € ; 1x Shampooing Garnier Fructis 3,89 € ; 1x Sac cabas réutilisable 0,10 € - Remises appliquées : Promo Yaourts -0,27 € ; Carte fidélité - Huile d'olive -0,69 € ; Bon de réduction papier toilette -1,00 € - TOTAL TTC : 61,67 € - Paiement : Carte bancaire - Montant payé : 61,67 € - Carte fidélité utilisée : OUI - Points cumulés : +61 - Économies réalisées : 1,96 € - Solde fidélité : 174 points - À très bientôt chez SuperPlus ! Conservez votre ticket pour tout échange.Souhaitez-vous que ce soit encore plus long (plus d’articles) ou formaté pour un usage spécifique (fichier, site web, jeu, etc.) ?"


# Appeler la fonction avec 'ingredients'

resultats = classer_mots_par_categorie(texte, ingredients)

# Afficher les résultats
for categorie, mots in resultats.items():
    print(f"{categorie.capitalize()}: {mots}")
