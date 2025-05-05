#Data aliments


import re



aliments = {
    "fruits": [
        "pomme", "banane", "orange", "fraise", "raisin", "kiwi", "poire", "abricot", 
        "prune", "mangue", "ananas", "melon", "pêche", "nectarine", "citrons", "framboise", 
        "myrtille", "figue", "papaye", "litchi", "clementine", "grenade", "rhubarbe"
    ],
    "legumes": [
        "carotte", "pomme de terre", "tomate", "oignon", "ail", "courgette", "poivron", 
        "concombre", "aubergine", "haricot vert", "brocoli", "chou-fleur", "épinard", 
        "salade", "laitue", "radis", "betterave", "céleri", "artichaut", "poireau", "chou", 
        "navet", "petit pois", "fenouil", "asperge", "patate douce", "topinambour"
    ],
    "feculents": [
        "pomme de terre", "riz", "pâtes", "semoule", "polenta", "quinoa", "lentilles", 
        "haricots secs", "pois chiches", "blé", "épeautre", "orge", "farine", "sarrasin", 
        "amarante", "patate douce", "maïs", "pois cassés"
    ],
    "viandes": [
        "bœuf", "poulet", "dinde", "porc", "agneau", "canard", "lapin", "veau", 
        "sanglier", "jambon", "saucisse", "bacon", "pâté", "charcuterie", "magret de canard",
        "côte de porc", "escalope de poulet", "filet de bœuf", "côtelettes d'agneau"
    ],
    "poissons_et_fruits_de_mer": [
        "saumon", "truite", "thon", "morue", "sardine", "maquereau", "merlu", "raie", 
        "anguille", "sole", "bar", "langouste", "crevette", "huître", "moule", "palourde", 
        "coquille Saint-Jacques", "crabe", "calamar", "pieuvre"
    ],
    "produits_laitiers": [
        "lait", "fromage", "yaourt", "crème", "beurre", "fromage blanc", "fromage de chèvre", 
        "camembert", "brie", "emmental", "gruyère", "mozzarella", "feta", "chèvre frais", 
        "beurre doux", "beurre salé", "crème fraîche"
    ],
    "boissons": [
        "eau", "jus de fruits", "vin", "bière", "thé", "café", "cacao", 
        
    ],
    "sucreries_et_confiseries": [
        "chocolat", "bonbons", "biscuit", "glace", 
        "caramel", "miel", "sucre", "compote de pommes", "confiture", "madeleine"
    ],
    "épices_et_condiments": [
        "sel", "poivre", "paprika", "curcuma", "curry", "thym", "romarin", "basilic", 
        "ciboulette", "persil", "menthe", "safran", "gingembre", "coriandre", "moutarde", 
        "vinaigre", "huile d'olive", "huile de tournesol", "sauce soja", "ketchup", "mayonnaise"
    ]
}
# Fonction pour extraire les mots présents dans le dictionnaire des aliments
def extraire_aliments_texte(texte, dictionnaire):
    # Convertir le texte en minuscule pour que la comparaison soit insensible à la casse
    texte = texte.lower()
    
    # Nettoyage du texte : retirer la ponctuation et découper en mots
    mots_texte = re.findall(r'\b\w+\b', texte)

    # Créer un set de tous les mots dans le dictionnaire
    aliments_set = set()
    for categorie, aliments in dictionnaire.items():
        aliments_set.update([aliment.lower() for aliment in aliments])

    # Trouver les mots du texte qui sont dans le dictionnaire
    mots_trouves = [mot for mot in mots_texte if mot in aliments_set]
    
    return mots_trouves

# Exemple de texte à analyser
texte = "J'ai acheté des pommes, des tomates, du riz, du poulet et du chocolat pour faire un bon dîner."

# Extraction des mots présents dans le texte
mots_aliments = extraire_aliments_texte(texte, aliments)

print("Mots trouvés dans le texte :")
print(mots_aliments)