import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from xgboost import XGBClassifier

from ai.feature_engineering import FeatureEngineer


print("Loading dataset...")

df = pd.read_csv("data/vehicle_dataset.csv")

print(df.shape)

engineer = FeatureEngineer()

df = engineer.create_features(df)

drop_columns = [
    "Fault",
    "Driving Mode",
    "Time Step",
]

X = df.drop(columns=drop_columns, errors="ignore")

y = df["Fault"]

# Encode labels
label_mapping = {
    "Healthy": 0,
    "Motor Fault": 1,
    "Battery Fault": 2,
    "Brake Fault": 3,
    "Bearing Fault": 4,
    "Tyre Fault": 5,
}

reverse_mapping = {v: k for k, v in label_mapping.items()}

y = y.map(label_mapping)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

print("Training XGBoost...")

model = XGBClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    objective="multi:softprob",
    num_class=6,
    random_state=42,
    eval_metric="mlogloss",
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, pred))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        pred,
        target_names=list(label_mapping.keys())
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, pred))

joblib.dump(model, "ai/models/xgboost.pkl")

print("\nXGBoost model saved!")