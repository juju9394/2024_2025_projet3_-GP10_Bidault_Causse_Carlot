import sys
import json
import zipfile
import os
import copy
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from PIL import Image, UnidentifiedImageError
from torch.multiprocessing import freeze_support

chemin_image = sys.argv[1]

# ======== CONFIGURATION PRÉCISE ========
torch.backends.cudnn.benchmark = True
zip_path = r'C:\Users\bidau\Downloads\test.zip'
extract_path = r'C:\Users\bidau\Downloads\fruits_dataset'
data_dir = extract_path
batch_size = 16 # Consider reducing to 8 or 4 if memory allows and for potentially better generalization
image_size = 224 # Can increase to 256 or 300 if more detail is needed and resources allow
max_epochs = 50 # Increased epochs for better convergence
learning_rate = 0.0001
model_path = "resnet50_fruits_best.pth"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
confidence_threshold = 0.75

# ======== TRANSFORMATIONS STABLES (with more augmentation) ========
transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.RandomHorizontalFlip(), # Add horizontal flip
    transforms.RandomRotation(15),     # Add slight rotation
    transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1), # Add color jitter
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
# For validation/test, keep basic transform
basic_transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])


# ======== ENTRAÎNEMENT PROFOND ========
def train_model():
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Use 'transform' for training dataset and 'basic_transform' for validation dataset
    train_dataset_full = datasets.ImageFolder(root=data_dir, transform=transform)
    val_dataset_full = datasets.ImageFolder(root=data_dir, transform=basic_transform)

    train_size = int(0.8 * len(train_dataset_full))
    val_size = len(train_dataset_full) - train_size
    train_dataset, _ = random_split(train_dataset_full, [train_size, val_size])
    _, val_dataset = random_split(val_dataset_full, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    class_names = train_dataset_full.classes
    model = models.resnet50(pretrained=True)

    # Fine-tune more layers for better precision
    for param in model.parameters():
        param.requires_grad = False
    for param in model.layer3.parameters(): # Unfreeze layer3
        param.requires_grad = True
    for param in model.layer4.parameters():
        param.requires_grad = True
    model.fc = nn.Linear(model.fc.in_features, len(class_names))
    model = model.to(device)

    if not os.path.exists(model_path):
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=learning_rate)
        # Add a learning rate scheduler
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.1, patience=5, verbose=True)

        best_model_wts = copy.deepcopy(model.state_dict())
        best_val_acc = 0.0
        patience_counter = 0 # For early stopping
        patience = 10 # Number of epochs to wait for improvement

        for epoch in range(max_epochs):
            model.train()
            running_corrects = 0
            total = 0

            for inputs, labels in train_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                _, preds = torch.max(outputs, 1)
                running_corrects += torch.sum(preds == labels)
                total += labels.size(0)

            train_acc = running_corrects.double() / total
            print(f"[{epoch+1}/{max_epochs}] Train Accuracy : {train_acc:.3f}")

            # Évaluation
            model.eval()
            correct = 0
            total = 0
            with torch.no_grad():
                for inputs, labels in val_loader:
                    inputs, labels = inputs.to(device), labels.to(device)
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    correct += torch.sum(preds == labels).item()
                    total += labels.size(0)
            val_acc = correct / total
            print(f"[{epoch+1}/{max_epochs}] Validation Accuracy : {val_acc:.3f}")

            scheduler.step(val_acc) # Step the learning rate scheduler

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_model_wts = copy.deepcopy(model.state_dict())
                patience_counter = 0 # Reset patience counter
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    print(f"Early stopping at epoch {epoch+1} as validation accuracy did not improve for {patience} epochs.")
                    break # Stop training

        model.load_state_dict(best_model_wts)
        torch.save(model.state_dict(), model_path)
    else:
        model.load_state_dict(torch.load(model_path, map_location=device))

    return model, class_names

# ======== PRÉDICTION FIABLE ========
def predict(model, class_names, image_path):
    if not os.path.exists(image_path):
        return "Image introuvable"
    try:
        image = Image.open(image_path).convert('RGB')
    except UnidentifiedImageError:
        return "Fichier non valide"

    image_tensor = basic_transform(image).unsqueeze(0).to(device)
    model.eval()
    with torch.no_grad():
        outputs = model(image_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        max_prob, pred = torch.max(probs, 1)

    predicted_class = class_names[pred.item()]
    confidence = max_prob.item()

    if confidence < confidence_threshold:
        return f"Inconnu (confiance {confidence:.2f})"
    return f"{predicted_class} ({confidence*100:.1f}%)"

# ======== MAIN ========
if __name__ == "__main__":
    freeze_support()
    model, class_names = train_model()
    resultat = predict(model, class_names, chemin_image)

    with open("resultat_prediction.json", "w") as f:
        json.dump({"prediction": resultat}, f)



#C:\Users\bidau\Downloads\ananas.jpg