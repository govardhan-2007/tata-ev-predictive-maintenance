import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


class SequenceGenerator:

    def __init__(self, sequence_length=50):

        self.sequence_length = sequence_length

        self.features = [
            "Speed",
            "RPM",
            "Torque",
            "Battery Voltage",
            "SOC",
            "Current",
            "Motor Temp",
            "Brake Temp",
            "Vibration",
            "Tyre Pressure",
            "Steering Angle",
        ]

    def generate(self, csv_path):

        print("Loading dataset...")

        df = pd.read_csv(csv_path)

        # Ensure chronological order
        df = df.sort_values("Time Step").reset_index(drop=True)

        X = df[self.features].values

        y = df["Fault"].values

        encoder = LabelEncoder()

        y = encoder.fit_transform(y)

        sequences = []
        labels = []

        for i in range(len(df) - self.sequence_length):

            sequences.append(
                X[i:i + self.sequence_length]
            )

            labels.append(
                y[i + self.sequence_length]
            )

        X_seq = np.array(sequences)

        y_seq = np.array(labels)

        print()

        print("Sequence Dataset Created")

        print("Input Shape :", X_seq.shape)

        print("Output Shape:", y_seq.shape)

        # Create folder if it doesn't exist
        os.makedirs("deep_learning/data", exist_ok=True)

        # Save the sequences
        np.save(
            "deep_learning/data/X_sequences.npy",
            X_seq,
        )

        np.save(
            "deep_learning/data/y_labels.npy",
            y_seq,
        )

        # Save the label encoder
        joblib.dump(
        encoder,
            "deep_learning/data/label_encoder.pkl",
        )

        print()
        print("✅ Sequence dataset saved successfully.")

        return X_seq, y_seq, encoder


if __name__ == "__main__":

    generator = SequenceGenerator(sequence_length=50)

    X, y, encoder = generator.generate(
        "data/vehicle_dataset.csv"
    )

    print()

    print("Classes:")

    print(encoder.classes_)