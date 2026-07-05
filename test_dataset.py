from torch.utils.data import DataLoader

from deep_learning.dataset import VehicleDataset


dataset = VehicleDataset(
    "deep_learning/data/X_sequences.npy",
    "deep_learning/data/y_labels.npy",
)

print("Dataset Size:", len(dataset))

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
)

X, y = next(iter(loader))

print()

print("Input Shape :", X.shape)

print("Labels Shape:", y.shape)