# import torch
# import torch.nn as nn
# import torch.optim as optim
# import torchvision
# import torchvision.transforms as transforms
# from torchvision import models
# from torch.utils.data import DataLoader
# from torchvision.datasets import ImageFolder
# from tqdm import tqdm
# import matplotlib.pyplot as plt
# from PIL import Image
# import os

# # Vérifie si un GPU est disponible pour l'entraînement
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Utilisation de : {device}")

# # Préparation des transformations d'images (redimensionnement, normalisation)
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
# ])

# # Chargement des données (tu dois avoir un dossier avec des sous-dossiers pour chaque classe d'aliments)
# train_data = ImageFolder(root='./data/train', transform=transform)  # Ton répertoire de train
# val_data = ImageFolder(root='./data/val', transform=transform)      # Ton répertoire de validation

# # DataLoader pour itérer sur les données par lot
# train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
# val_loader = DataLoader(val_data, batch_size=32, shuffle=False)

# # Chargement du modèle pré-entraîné (ResNet50 ici)
# model = models.resnet50(pretrained=True)

# # Geler les poids des premières couches pour ne pas les réentraîner
# for param in model.parameters():
#     param.requires_grad = False

# # Remplacer la dernière couche par une nouvelle, adaptée à notre nombre de classes
# model.fc = nn.Linear(model.fc.in_features, len(train_data.classes))

# # Déplacer le modèle vers le GPU ou CPU
# model = model.to(device)

# # Fonction de perte et optimiseur
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)

# # Entraînement du modèle
# num_epochs = 10
# for epoch in range(num_epochs):
#     model.train()  # Mettre le modèle en mode entraînement
#     running_loss = 0.0

#     # Parcours des données d'entraînement
#     for inputs, labels in tqdm(train_loader):
#         inputs, labels = inputs.to(device), labels.to(device)

#         optimizer.zero_grad()  # Remise à zéro des gradients

#         # Passage avant et calcul de la perte
#         outputs = model(inputs)
#         loss = criterion(outputs, labels)
#         loss.backward()  # Calcul des gradients
#         optimizer.step()  # Mise à jour des poids

#         running_loss += loss.item()

#     print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}")

#     # Validation à chaque époque
#     model.eval()  # Mode évaluation
#     correct = 0
#     total = 0
#     with torch.no_grad():
#         for inputs, labels in val_loader:
#             inputs, labels = inputs.to(device), labels.to(device)
#             outputs = model(inputs)
#             _, predicted = torch.max(outputs.data, 1)
#             total += labels.size(0)
#             correct += (predicted == labels).sum().item()

#     print(f"Accuracy after epoch {epoch + 1}: {100 * correct / total:.2f}%")

# # Sauvegarde du modèle
# torch.save(model.state_dict(), 'food_recognition_model.pth')

# # Fonction de prédiction sur une image
# def predict_image(image_path):
#     model.eval()  # Mode évaluation
#     image = Image.open(image_path).convert('RGB')
#     image = transform(image).unsqueeze(0).to(device)  # Transforme l'image
#     with torch.no_grad():
#         outputs = model(image)
#     _, predicted = torch.max(outputs, 1)
#     predicted_class = train_data.classes[predicted.item()]
#     print(f"Prédiction : {predicted_class}")

#     # Affiche l'image et la prédiction
#     plt.imshow(Image.open(image_path))
#     plt.title(f"Prédiction: {predicted_class}")
#     plt.show()

# # Exemple de prédiction
# predict_image('./data/test/pizza.jpg')  # Remplace par ton image



import numpy as np
import pandas as pd
from pathlib import Path
import os.path
import matplotlib.pyplot as plt
import tensorflow as tf
import warnings
warnings.filterwarnings("ignore")

# Create a list with the filepaths for training and testing
train_dir = Path('../input/fruit-and-vegetable-image-recognition/train')
train_filepaths = list(train_dir.glob(r'**/*.jpg'))

test_dir = Path('../input/fruit-and-vegetable-image-recognition/test')
test_filepaths = list(test_dir.glob(r'**/*.jpg'))

val_dir = Path('../input/fruit-and-vegetable-image-recognition/validation')
val_filepaths = list(test_dir.glob(r'**/*.jpg'))

def proc_img(filepath):
    """ Create a DataFrame with the filepath and the labels of the pictures
    """

    labels = [str(filepath[i]).split("/")[-2] \
              for i in range(len(filepath))]

    filepath = pd.Series(filepath, name='Filepath').astype(str)
    labels = pd.Series(labels, name='Label')

    # Concatenate filepaths and labels
    df = pd.concat([filepath, labels], axis=1)

    # Shuffle the DataFrame and reset index
    df = df.sample(frac=1).reset_index(drop = True)
    
    return df

train_df = proc_img(train_filepaths)
test_df = proc_img(test_filepaths)
val_df = proc_img(val_filepaths)

print('-- Training set --\n')
print(f'Number of pictures: {train_df.shape[0]}\n')
print(f'Number of different labels: {len(train_df.Label.unique())}\n')
print(f'Labels: {train_df.Label.unique()}')


# Create a DataFrame with one Label of each category
df_unique = train_df.copy().drop_duplicates(subset=["Label"]).reset_index()

# Display some pictures of the dataset
fig, axes = plt.subplots(nrows=6, ncols=6, figsize=(8, 7),
                        subplot_kw={'xticks': [], 'yticks': []})

for i, ax in enumerate(axes.flat):
    ax.imshow(plt.imread(df_unique.Filepath[i]))
    ax.set_title(df_unique.Label[i], fontsize = 12)
plt.tight_layout(pad=0.5)
plt.show()

train_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
)

test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
)

train_images = train_generator.flow_from_dataframe(
    dataframe=train_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=32,
    shuffle=True,
    seed=0,
    rotation_range=30,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode="nearest"
)

val_images = train_generator.flow_from_dataframe(
    dataframe=val_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=32,
    shuffle=True,
    seed=0,
    rotation_range=30,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode="nearest"
)

test_images = test_generator.flow_from_dataframe(
    dataframe=test_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=32,
    shuffle=False


    inputs = pretrained_model.input


x = tf.keras.layers.Dense(128, activation='relu')(pretrained_model.output)
x = tf.keras.layers.Dense(128, activation='relu')(x)

outputs = tf.keras.layers.Dense(36, activation='softmax')(x)

model = tf.keras.Model(inputs=inputs, outputs=outputs)

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_images,
    validation_data=val_images,
    batch_size = 32,
    epochs=5,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=2,
            restore_best_weights=True
              )
    ]
)
)
