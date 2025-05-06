import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torchvision import models
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from tqdm import tqdm
import matplotlib.pyplot as plt
from PIL import Image
import os

# Vérifie si un GPU est disponible pour l'entraînement
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Utilisation de : {device}")

# Préparation des transformations d'images (redimensionnement, normalisation)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Chargement des données (tu dois avoir un dossier avec des sous-dossiers pour chaque classe d'aliments)
train_data = ImageFolder(root='./data/train', transform=transform)  # Ton répertoire de train
val_data = ImageFolder(root='./data/val', transform=transform)      # Ton répertoire de validation

# DataLoader pour itérer sur les données par lot
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
val_loader = DataLoader(val_data, batch_size=32, shuffle=False)

# Chargement du modèle pré-entraîné (ResNet50 ici)
model = models.resnet50(pretrained=True)

# Geler les poids des premières couches pour ne pas les réentraîner
for param in model.parameters():
    param.requires_grad = False

# Remplacer la dernière couche par une nouvelle, adaptée à notre nombre de classes
model.fc = nn.Linear(model.fc.in_features, len(train_data.classes))

# Déplacer le modèle vers le GPU ou CPU
model = model.to(device)

# Fonction de perte et optimiseur
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Entraînement du modèle
num_epochs = 10
for epoch in range(num_epochs):
    model.train()  # Mettre le modèle en mode entraînement
    running_loss = 0.0

    # Parcours des données d'entraînement
    for inputs, labels in tqdm(train_loader):
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()  # Remise à zéro des gradients

        # Passage avant et calcul de la perte
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()  # Calcul des gradients
        optimizer.step()  # Mise à jour des poids

        running_loss += loss.item()

    print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}")

    # Validation à chaque époque
    model.eval()  # Mode évaluation
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f"Accuracy after epoch {epoch + 1}: {100 * correct / total:.2f}%")

# Sauvegarde du modèle
torch.save(model.state_dict(), 'food_recognition_model.pth')

# Fonction de prédiction sur une image
def predict_image(image_path):
    model.eval()  # Mode évaluation
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)  # Transforme l'image
    with torch.no_grad():
        outputs = model(image)
    _, predicted = torch.max(outputs, 1)
    predicted_class = train_data.classes[predicted.item()]
    print(f"Prédiction : {predicted_class}")

    # Affiche l'image et la prédiction
    plt.imshow(Image.open(image_path))
    plt.title(f"Prédiction: {predicted_class}")
    plt.show()

# Exemple de prédiction
predict_image('./data/test/pizza.jpg')  # Remplace par ton image
