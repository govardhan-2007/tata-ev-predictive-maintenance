import torch
import torch.nn as nn


class CNNLSTM(nn.Module):

    def __init__(
        self,
        input_features=11,
        hidden_size=128,
        num_layers=2,
        num_classes=6,
    ):

        super().__init__()

        # CNN Feature Extractor
        self.cnn = nn.Sequential(

            nn.Conv1d(
                in_channels=input_features,
                out_channels=64,
                kernel_size=3,
                padding=1,
            ),

            nn.BatchNorm1d(64),

            nn.ReLU(),

            nn.MaxPool1d(2),
        )

        # LSTM
        self.lstm = nn.LSTM(

            input_size=64,

            hidden_size=hidden_size,

            num_layers=num_layers,

            batch_first=True,

            dropout=0.3,
        )

        # Classifier
        self.classifier = nn.Sequential(

            nn.Linear(hidden_size, 64),

            nn.ReLU(),

            nn.Dropout(0.4),

            nn.Linear(64, num_classes),
        )

    def forward(self, x):

        # x shape:
        # (batch, sequence, features)

        x = x.permute(0, 2, 1)

        x = self.cnn(x)

        x = x.permute(0, 2, 1)

        output, _ = self.lstm(x)

        output = output[:, -1, :]

        output = self.classifier(output)

        return output