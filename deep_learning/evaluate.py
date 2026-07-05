import os

import matplotlib.pyplot as plt
import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Subset

from deep_learning.cnn_lstm import CNNLSTM
from deep_learning.dataset import VehicleDataset

# -----------------------------
# Configuration
# -----------------------------

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

BATCH_SIZE = 128

# -----------------------------
# Load Dataset
# -----------------------------

dataset = VehicleDataset(
    "deep_learning/data/X_sequences.npy",
    "deep_learning/data/y_labels.npy",
)

indices = list(range(len(dataset)))

_, test_idx = train_test_split(
    indices,
    test_size=0.2,
    random_state=42,
    shuffle=True,
)

test_dataset = Subset(dataset, test_idx)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0,
)

# -----------------------------
# Load Model
# -----------------------------

model = CNNLSTM().to(DEVICE)

model.load_state_dict(
    torch.load(
        "deep_learning/models/vehicle_cnn_lstm.pth",
        map_location=DEVICE,
    )
)

model.eval()

predictions = []
labels = []

with torch.no_grad():

    for X, y in test_loader:

        X = X.to(DEVICE)
        y = y.to(DEVICE)

        outputs = model(X)

        predicted = torch.argmax(outputs, dim=1)

        predictions.extend(predicted.cpu().numpy())
        labels.extend(y.cpu().numpy())

# -----------------------------
# Metrics
# -----------------------------

accuracy = accuracy_score(labels, predictions)

print(f"\nAccuracy : {accuracy*100:.2f}%\n")

print(
    classification_report(
        labels,
        predictions,
    )
)

# -----------------------------
# Confusion Matrix
# -----------------------------

cm = confusion_matrix(labels, predictions)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
)

disp.plot()

os.makedirs(
    "deep_learning/results",
    exist_ok=True,
)

plt.savefig(
    "deep_learning/results/confusion_matrix.png",
    dpi=300,
)

plt.show()

print("\n✅ Confusion Matrix Saved")