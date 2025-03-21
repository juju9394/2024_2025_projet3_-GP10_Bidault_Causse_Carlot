import sqlite3

# Connexion à la base de données SQLite (elle sera créée si elle n'existe pas)
conn = sqlite3.connect('recettes_cuisine.db')
cursor = conn.cursor()

# Fonction pour créer les tables
def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            id_categorie INTEGER PRIMARY KEY,
            nom_categorie TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Recettes (
            id_recette INTEGER PRIMARY KEY,
            nom_recette TEXT,
            id_categorie INTEGER,
            description TEXT,
            temps_preparation TEXT,
            FOREIGN KEY (id_categorie) REFERENCES Categories(id_categorie)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ingredients (
            id_ingredient INTEGER PRIMARY KEY,
            nom_ingredient TEXT,
            quantite TEXT,
            id_recette INTEGER,
            FOREIGN KEY (id_recette) REFERENCES Recettes(id_recette)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ustensiles (
            id_ustensile INTEGER PRIMARY KEY,
            nom_ustensile TEXT,
            id_recette INTEGER,
            FOREIGN KEY (id_recette) REFERENCES Recettes(id_recette)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Temps_Preparation (
            id_recette INTEGER PRIMARY KEY,
            temps_total TEXT,
            temps_cuisson TEXT,
            temps_preparation TEXT,
            FOREIGN KEY (id_recette) REFERENCES Recettes(id_recette)
        );
    ''')

# Fonction pour insérer des données dans les tables
def insert_data():
    # Insertion des catégories
    cursor.execute("INSERT INTO Categories (nom_categorie) VALUES ('Entrée')")
    cursor.execute("INSERT INTO Categories (nom_categorie) VALUES ('Plat principal')")
    cursor.execute("INSERT INTO Categories (nom_categorie) VALUES ('Dessert')")
    
    # Récupérer les id des catégories
    cursor.execute("SELECT id_categorie FROM Categories WHERE nom_categorie = 'Entrée'")
    id_entrée = cursor.fetchone()[0]
    
    cursor.execute("SELECT id_categorie FROM Categories WHERE nom_categorie = 'Plat principal'")
    id_plat_principal = cursor.fetchone()[0]
    
    cursor.execute("SELECT id_categorie FROM Categories WHERE nom_categorie = 'Dessert'")
    id_dessert = cursor.fetchone()[0]
    
    # Insertion des recettes
    recettes = [
        ('Ratatouille', id_plat_principal, 'Un plat provençal délicieux', '40 min'),
        ('Tarte au citron', id_dessert, 'Dessert sucré et acidulé', '30 min'),
        ('Salade César', id_entrée, 'Salade fraîche avec une sauce crémeuse', '15 min'),
        ('Boeuf bourguignon', id_plat_principal, 'Plat mijoté à base de boeuf et de vin rouge', '3h'),
        ('Panna cotta', id_dessert, 'Dessert crémeux italien', '25 min'),
        ('Soupe à l\'oignon', id_entrée, 'Soupe chaude à base d\'oignons caramélisés', '1h'),
        ('Pizza Margherita', id_plat_principal, 'Pizza classique avec tomate, mozzarella et basilic', '40 min'),
        ('Poulet rôti', id_plat_principal, 'Poulet rôti au four avec herbes et légumes', '1h 30min'),
        ('Spaghetti bolognaise', id_plat_principal, 'Pâtes avec sauce à base de viande hachée et tomate', '1h'),
        ('Quiche lorraine', id_plat_principal, 'Tarte salée avec lardons, œufs et crème', '1h'),
        ('Gratin dauphinois', id_plat_principal, 'Pommes de terre en gratin avec de la crème et du fromage', '1h'),
        ('Chili con carne', id_plat_principal, 'Plat épicé à base de viande hachée, haricots et tomates', '1h 15min'),
        ('Croque-monsieur', id_entrée, 'Sandwich grillé avec du jambon et du fromage', '10 min'),
        ('Pâtes aux crevettes', id_plat_principal, 'Pâtes avec des crevettes sautées et une sauce crémeuse', '30 min'),
        ('Riz au lait', id_dessert, 'Dessert crémeux à base de riz, lait et sucre', '45 min'),
        ('Gâteau au chocolat', id_dessert, 'Gâteau moelleux au chocolat', '1h'),
        ('Couscous', id_plat_principal, 'Plat traditionnel avec de la semoule et des légumes', '2h'),
        ('Frittata', id_plat_principal, 'Omelette italienne avec légumes et fromage', '20 min'),
        ('Moules marinières', id_plat_principal, 'Moules cuites dans du vin blanc et des herbes', '20 min'),
        ('Pavé de saumon', id_plat_principal, 'Saumon cuit au four ou poêlé', '25 min')
    ]
    
    # Insertion des recettes et récupération des id_recette
    recette_ids = {}
    for recette in recettes:
        cursor.execute('''
            INSERT INTO Recettes (nom_recette, id_categorie, description, temps_preparation)
            VALUES (?, ?, ?, ?)
        ''', (recette[0], recette[1], recette[2], recette[3]))
        
        # Récupérer l'id de la recette insérée
        cursor.execute("SELECT id_recette FROM Recettes WHERE nom_recette = ?", (recette[0],))
        recette_ids[recette[0]] = cursor.fetchone()[0]

    # Insertion des ingrédients pour chaque recette
    ingredients = [
        ('Aubergine', '2 pièces', 'Ratatouille'),
        ('Courgette', '2 pièces', 'Ratatouille'),
        ('Citron', '2 pièces', 'Tarte au citron'),
        ('Sucre', '200g', 'Tarte au citron'),
        ('Lait', '500 ml', 'Panna cotta'),
        ('Crème fraîche', '200 ml', 'Panna cotta'),
        ('Oignons', '4', 'Soupe à l\'oignon'),
        ('Boeuf', '800g', 'Boeuf bourguignon'),
        ('Vin rouge', '500 ml', 'Boeuf bourguignon'),
        ('Mozzarella', '200g', 'Pizza Margherita'),
        ('Tomate', '2', 'Pizza Margherita'),
        ('Basilic', 'quelques feuilles', 'Pizza Margherita'),
        ('Poulet', '1 entier', 'Poulet rôti')
    ]
    
    # Insérer les ingrédients avec le bon id_recette
    for ingredient in ingredients:
        recette_id = recette_ids[ingredient[2]]  # Trouver l'id de la recette correspondante
        cursor.execute('''
            INSERT INTO Ingredients (nom_ingredient, quantite, id_recette)
            VALUES (?, ?, ?)
        ''', (ingredient[0], ingredient[1], recette_id))

    # Insertion des ustensiles pour chaque recette
    ustensiles = [
        ('Poêle', 'Ratatouille'),
        ('Four', 'Ratatouille'),
        ('Moule à tarte', 'Tarte au citron'),
        ('Fouet', 'Tarte au citron'),
        ('Casserole', 'Soupe à l\'oignon'),
        ('Cocotte', 'Boeuf bourguignon'),
        ('Moule à panna cotta', 'Panna cotta'),
        ('Rôtissoire', 'Poulet rôti')
    ]

    for ustensile in ustensiles:
        recette_id = recette_ids[ustensile[1]]
        cursor.execute('''
            INSERT INTO Ustensiles (nom_ustensile, id_recette)
            VALUES (?, ?)
        ''', (ustensile[0], recette_id))

    # Insertion des temps de préparation pour chaque recette
    temps_preparation = [
        ('Ratatouille', '40 min', '30 min', '10 min'),
        ('Tarte au citron', '30 min', '20 min', '10 min'),
        ('Soupe à l\'oignon', '1h', '30 min', '30 min')
    ]

    for temps in temps_preparation:
        recette_id = recette_ids[temps[0]]
        cursor.execute('''
            INSERT INTO Temps_Preparation (id_recette, temps_total, temps_cuisson, temps_preparation)
            VALUES (?, ?, ?, ?)
        ''', (recette_id, temps[1], temps[2], temps[3]))

# Fonction pour afficher les recettes avec leurs détails
def display_recipes():
    cursor.execute('''
        SELECT r.nom_recette, c.nom_categorie, r.description, r.temps_preparation, 
               i.nom_ingredient, i.quantite, u.nom_ustensile, t.temps_total, t.temps_cuisson, t.temps_preparation
        FROM Recettes r
        JOIN Categories c ON r.id_categorie = c.id_categorie
        LEFT JOIN Ingredients i ON r.id_recette = i.id_recette
        LEFT JOIN Ustensiles u ON r.id_recette = u.id_recette
        LEFT JOIN Temps_Preparation t ON r.id_recette = t.id_recette
    ''')

    recipes = cursor.fetchall()

    # Si aucune recette n'est trouvée
    if not recipes:
        print("Aucune recette trouvée.")
    
    for recipe in recipes:
        print(f"Nom de la recette: {recipe[0]}")
        print(f"Catégorie: {recipe[1]}")
        print(f"Description: {recipe[2]}")
        print(f"Temps de préparation: {recipe[3]}")
        print(f"Ingrédients: {recipe[4]} - {recipe[5]}")
        print(f"Ustensiles nécessaires: {recipe[6]}")
        print(f"Temps total: {recipe[7]} | Temps de cuisson: {recipe[8]} | Temps de préparation: {recipe[9]}")
        print("-" * 40)

# Exécution des fonctions
create_tables()
insert_data()
display_recipes()

