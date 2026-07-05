import joblib
import numpy as np
import torch
import torch.nn.functional as F

from deep_learning.cnn_lstm import CNNLSTM


class CNNInference:

    def __init__(self):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available()
            else "cpu"
        )

        self.model = CNNLSTM().to(self.device)

        self.model.load_state_dict(
            torch.load(
                "deep_learning/models/vehicle_cnn_lstm.pth",
                map_location=self.device,
            )
        )

        self.model.eval()

        self.encoder = joblib.load(
            "deep_learning/data/label_encoder.pkl"
        )

    def predict(self, sequence):

        """
        sequence shape:
        (50,11)
        """

        x = np.array(
            sequence,
            dtype=np.float32
        )

        # Normalize exactly like training
        mean = x.mean(axis=0, keepdims=True)
        std = x.std(axis=0, keepdims=True)

        x = (x - mean) / (std + 1e-8)

        x = torch.tensor(
            x,
            dtype=torch.float32
        ).unsqueeze(0).to(self.device)

        with torch.no_grad():

            outputs = self.model(x)

            probs = F.softmax(
                outputs,
                dim=1
            )

        confidence = float(
            probs.max().item() * 100
        )

        prediction = int(
            probs.argmax().item()
        )

        prediction = self.encoder.inverse_transform(
            [prediction]
        )[0]

        probability_dict = {}

        for i, cls in enumerate(self.encoder.classes_):

            probability_dict[cls] = round(
                float(probs[0][i].item() * 100),
                2,
            )

        return {

            "prediction": prediction,

            "confidence": round(
                confidence,
                2,
            ),

            "probabilities": probability_dict,

        }