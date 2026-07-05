import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# -----------------------
# Load Dataset
# -----------------------

df = pd.read_csv("data/vehicle_dataset.csv")

# -----------------------
# Features
# -----------------------

X = df.drop(columns=["Fault"])

# Encode Driving Mode if present
if "Driving Mode" in X.columns:
    X["Driving Mode"] = LabelEncoder().fit_transform(X["Driving Mode"])

y = df["Fault"]

# -----------------------
# Encode Labels
# -----------------------

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

joblib.dump(label_encoder, "ai/models/cnn_label_encoder.pkl")

# -----------------------
# Normalize
# -----------------------

scaler = StandardScaler()
X = scaler.fit_transform(X)

joblib.dump(scaler, "ai/models/cnn_scaler.pkl")

# -----------------------
# Create Sequences
# -----------------------

sequence_length = 50

X_seq = []
y_seq = []

for i in range(sequence_length, len(X)):
    X_seq.append(X[i-sequence_length:i])
    y_seq.append(y[i])

X_seq = np.array(X_seq)
y_seq = np.array(y_seq)

y_seq = to_categorical(y_seq)

print(X_seq.shape)
print(y_seq.shape)

# -----------------------
# CNN-LSTM
# -----------------------

model = Sequential()

model.add(
    Conv1D(
        filters=32,
        kernel_size=3,
        activation="relu",
        input_shape=(sequence_length, X_seq.shape[2]),
    )
)

model.add(MaxPooling1D(pool_size=2))

model.add(LSTM(64))

model.add(Dropout(0.3))

model.add(Dense(64, activation="relu"))

model.add(Dense(y_seq.shape[1], activation="softmax"))

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

model.summary()

history = model.fit(
    X_seq,
    y_seq,
    epochs=10,
    batch_size=64,
    validation_split=0.2,
)

model.save("ai/models/cnn_lstm.keras")

print("CNN-LSTM saved successfully!")