import torch

from sklearn.model_selection import train_test_split

from torch.utils.data import DataLoader
from torch.utils.data import Subset

from deep_learning.dataset import VehicleDataset
from tqdm import tqdm
from sklearn.metrics import accuracy_score
import os


# -----------------------------
# Configuration
# -----------------------------

BATCH_SIZE = 128

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

print(f"\nUsing Device : {DEVICE}")


# -----------------------------
# Load Dataset
# -----------------------------

dataset = VehicleDataset(
    "deep_learning/data/X_sequences.npy",
    "deep_learning/data/y_labels.npy",
)

print(f"Dataset Size : {len(dataset):,}")


# -----------------------------
# Train / Validation Split
# -----------------------------

indices = list(range(len(dataset)))

train_idx, val_idx = train_test_split(

    indices,

    test_size=0.2,

    random_state=42,

    shuffle=True,

)


train_dataset = Subset(dataset, train_idx)

val_dataset = Subset(dataset, val_idx)


# -----------------------------
# DataLoaders
# -----------------------------

train_loader = DataLoader(

    train_dataset,

    batch_size=BATCH_SIZE,

    shuffle=True,

    num_workers=0,

    pin_memory=True,

)

val_loader = DataLoader(

    val_dataset,

    batch_size=BATCH_SIZE,

    shuffle=False,

    num_workers=0,

    pin_memory=True,

)


print()

print("Training Samples :", len(train_dataset))

print("Validation Samples :", len(val_dataset))

print()

print("Train Batches :", len(train_loader))

print("Validation Batches :", len(val_loader))
from deep_learning.cnn_lstm import CNNLSTM

import torch.nn as nn

from torch.optim import Adam

from torch.optim.lr_scheduler import ReduceLROnPlateau


# -----------------------------
# Model
# -----------------------------

model = CNNLSTM().to(DEVICE)

print("\nModel Loaded Successfully")

# -----------------------------
# Loss Function
# -----------------------------

criterion = nn.CrossEntropyLoss()

# -----------------------------
# Optimizer
# -----------------------------

optimizer = Adam(

    model.parameters(),

    lr=0.0003,

    weight_decay=1e-5,

)

# -----------------------------
# Learning Rate Scheduler
# -----------------------------

scheduler = ReduceLROnPlateau(

    optimizer,

    mode="min",

    factor=0.5,

    patience=3,

)

# -----------------------------
# Mixed Precision
# -----------------------------

#scaler = torch.amp.GradScaler("cuda")

print("Mixed Precision Enabled")

print()

print(model)
# -----------------------------
# Training
# -----------------------------

EPOCHS = 20

best_accuracy = 0

os.makedirs(
    "deep_learning/models",
    exist_ok=True,
)

for epoch in range(EPOCHS):

    print(f"\nEpoch {epoch+1}/{EPOCHS}")

    model.train()

    running_loss = 0

    for X, y in tqdm(train_loader):

        X = X.to(DEVICE, non_blocking=True)

        y = y.to(DEVICE, non_blocking=True)

        optimizer.zero_grad()

        outputs = model(X)

        loss = criterion(outputs, y)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    train_loss = running_loss / len(train_loader)

    # -----------------------------
    # Validation
    # -----------------------------

    model.eval()

    predictions = []

    labels = []

    validation_loss = 0

    with torch.no_grad():

        for X, y in val_loader:

            X = X.to(DEVICE)

            y = y.to(DEVICE)

            with torch.amp.autocast("cuda"):

                outputs = model(X)

                loss = criterion(outputs, y)

            validation_loss += loss.item()

            predicted = torch.argmax(outputs, dim=1)

            predictions.extend(
                predicted.cpu().numpy()
            )

            labels.extend(
                y.cpu().numpy()
            )

    validation_loss /= len(val_loader)

    accuracy = accuracy_score(
        labels,
        predictions,
    )

    scheduler.step(validation_loss)

    print(f"Train Loss : {train_loss:.4f}")

    print(f"Validation Loss : {validation_loss:.4f}")

    print(f"Validation Accuracy : {accuracy*100:.2f}%")

    # -----------------------------
    # Save Best Model
    # -----------------------------

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        torch.save(

            model.state_dict(),

            "deep_learning/models/vehicle_cnn_lstm.pth",

        )

        print("✅ Best Model Saved")