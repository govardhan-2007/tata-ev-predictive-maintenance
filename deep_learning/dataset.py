import numpy as np
import torch
from torch.utils.data import Dataset


class VehicleDataset(Dataset):

    def __init__(self, x_path, y_path):

        self.X = np.load(x_path).astype(np.float32)

        self.y = np.load(y_path)

        # Normalize each feature
        mean = self.X.mean(axis=(0, 1), keepdims=True)
        std = self.X.std(axis=(0, 1), keepdims=True)

        self.X = (self.X - mean) / (std + 1e-8)

        self.X = torch.tensor(self.X, dtype=torch.float32)
        self.y = torch.tensor(self.y, dtype=torch.long)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]