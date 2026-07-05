import torch

from deep_learning.cnn_lstm import CNNLSTM


device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

model = CNNLSTM().to(device)

x = torch.randn(
    32,
    50,
    11,
).to(device)

y = model(x)

print("Device:", device)

print("Output Shape:", y.shape)