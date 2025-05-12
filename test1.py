import zipfile
import os
import copy
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from torch.optim.lr_scheduler import ReduceLROnPlateau
from PIL import Image
from torch.multiprocessing import freeze_support

# ======== 1. Config ========
torch.backends.cudnn.benchmark = True

zip_path = r'C:\Users\bidault\Downloads\test.zip'
extract_path = r'C:\Users\bidault\Downloads\fruits_dataset'
data_dir = extract_path
batch_size = 32
image_size = 128
max_epochs = 8
learning_rate = 0.001
model_path = "resnet18_fruits_best.pth"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ======== 2. Transforms ========
transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ======== 3. Fonction Entraînement ========
def train_model():
    # Décompression ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Contenu extrait :", os.listdir(extract_path))

    # Dataset & Dataloaders
    dataset = datasets.ImageFolder(root=data_dir, transform=transform)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    # ✅ Correction Windows : num_workers=0 ou avec if __main__
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    class_names = dataset.classes
    num_classes = len(class_names)
    print(f"Classes détectées : {class_names}")

    # Modèle ResNet18
    model = models.resnet18(pretrained=True)
    for param in model.parameters():
        param.requires_grad = True

    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model = model.to(device)

    # Loss, Optimizer, Scheduler
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=2)

    # Entraînement avec early stopping
    best_acc = 0.0
    best_model_wts = copy.deepcopy(model.state_dict())
    patience_counter = 0
    patience_limit = 3

    print("Entraînement démarré...")
    for epoch in range(max_epochs):
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

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()

        val_acc = 100 * val_correct / val_total
        scheduler.step(val_acc)

        print(f"Epoch [{epoch+1}/{max_epochs}] | Train Acc: {epoch_acc:.2f}% | Val Acc: {val_acc:.2f}%")

        # Early stopping
        if val_acc > best_acc:
            best_acc = val_acc
            best_model_wts = copy.deepcopy(model.state_dict())
            torch.save(best_model_wts, model_path)
            print("✓ Nouveau meilleur modèle sauvegardé.")
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience_limit:
                print("🛑 Arrêt anticipé (early stopping).")
                break

    # Charger meilleur modèle
    model.load_state_dict(best_model_wts)
    return model, class_names

# ======== 4. Fonction Prédiction ========
def predict_image(model, class_names, image_path):
    if not os.path.exists(image_path):
        print(f"Image introuvable : {image_path}")
        return None

    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)

    model.eval()
    outputs = model(image)
    _, predicted = torch.max(outputs, 1)
    predicted_class = class_names[predicted.item()]
    return predicted_class

# ======== 5. Main ========
if __name__ == "__main__":
    freeze_support()  # Correction Windows multiprocessing
    model, class_names = train_model()

    # Exemple prédiction
    resultat = predict_image(model, class_names, r'C:\Users\bidault\Downloads\poire.jpg')
    print(f"Prédiction : {resultat}")
