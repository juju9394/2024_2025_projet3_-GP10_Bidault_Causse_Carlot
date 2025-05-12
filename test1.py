import zipfile
import os
import copy
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from torch.optim.lr_scheduler import ReduceLROnPlateau
from PIL import Image, UnidentifiedImageError
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

basic_transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ======== 3. Fonction Entraînement ========
def train_model():
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Contenu extrait :", os.listdir(extract_path))

    dataset = datasets.ImageFolder(root=data_dir, transform=transform)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    class_names = dataset.classes
    num_classes = len(class_names)
    print(f"Classes détectées : {class_names}")

    model = models.resnet18(pretrained=True)
    for param in model.parameters():
        param.requires_grad = True

    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model = model.to(device)

    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=device))
        print("✅ Modèle pré-entraîné chargé.")

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=2)

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

    model.load_state_dict(best_model_wts)
    return model, class_names

# ======== 4. Fonction Prédiction + Feedback ========
def predict_and_learn(model, class_names, image_path):
    if not os.path.exists(image_path):
        print("❌ L'image spécifiée n'existe pas.")
        return "Image introuvable"

    try:
        image = Image.open(image_path).convert('RGB')
    except UnidentifiedImageError:
        print("❌ Le fichier n'est pas une image valide.")
        return "Fichier non valide"

    image_tensor = basic_transform(image).unsqueeze(0).to(device)

    model.eval()
    outputs = model(image_tensor)
    probabilities = torch.nn.functional.softmax(outputs, dim=1)
    max_prob, predicted = torch.max(probabilities, 1)
    predicted_class = class_names[predicted.item()]

    if max_prob.item() < 0.6:
        print("🤔 Je ne suis pas sûr... Ce n'est peut-être pas un fruit connu.")
        return "Inconnu"

    print(f"Prédiction : {predicted_class} (confiance : {max_prob.item():.2f})")
    user_feedback = input("Est-ce correct ? (o/n) ").strip().lower()

    if user_feedback == 'o':
        print("✓ Prédiction confirmée.")
        return predicted_class
    else:
        print(f"Classes disponibles : {class_names}")
        correct_class = input("Tapez la bonne classe : ").strip().lower()

        if correct_class in class_names:
            correct_index = class_names.index(correct_class)
            criterion = nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

            model.train()
            outputs = model(image_tensor)
            loss = criterion(outputs, torch.tensor([correct_index]).to(device))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            torch.save(model.state_dict(), model_path)
            print(f"🔄 Modèle mis à jour avec la classe '{correct_class}'.")
            print("💾 Modèle sauvegardé après correction.")
        else:
            print("❌ Classe inconnue. Aucune mise à jour effectuée.")

        return correct_class

# ======== 5. Main ========
if __name__ == "__main__":
    freeze_support()
    model, class_names = train_model()

    image_test_path = r'C:\Users\bidault\Downloads\mangue.jpg'
    resultat = predict_and_learn(model, class_names, image_test_path)
    print(f"Résultat final : {resultat}")