import zipfile
import os

# Décompression
zip_path = 'C:\\Users\\Bidault\\Downloads\\test.zip'

extract_path = 'C:\\Users\\Bidault\\Downloads\\fruits_dataset'


with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Lister le contenu
os.listdir(extract_path)


import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image

# ======== 1. Config ========
data_dir = 'C:\\Users\\Bidault\\Downloads\\fruits_dataset'  # Remplace par ton chemin local
batch_size = 32
image_size = 224
num_epochs = 5
learning_rate = 0.001
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ======== 2. Transforms ========
transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ======== 3. Dataset & DataLoaders ========
dataset = datasets.ImageFolder(root=data_dir, transform=transform)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

class_names = dataset.classes
num_classes = len(class_names)
print(f"Classes: {class_names}")

# ======== 4. Charger ResNet18 ========
model = models.resnet18(pretrained=True)

# Remplacer la dernière couche fully connected
model.fc = nn.Linear(model.fc.in_features, num_classes)
model = model.to(device)

# ======== 5. Loss & Optimizer ========
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# ======== 6. Entraînement ========
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100 * correct / total
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.2f}%')

# ======== 7. Validation ========
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in val_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Validation Accuracy: {100 * correct / total:.2f}%')

# ======== 8. Tester sur une image ========
def predict_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)

    model.eval()
    outputs = model(image)
    _, predicted = torch.max(outputs, 1)
    predicted_class = class_names[predicted.item()]
    return predicted_class

# Exemple d'utilisation :
# 
print(predict_image('C:\\Users\\bidault\\Downloads\\banane.jpg'))


