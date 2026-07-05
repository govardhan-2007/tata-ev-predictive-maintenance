import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
)

from ai.preprocess import DataPreprocessor
from ai.feature_engineering import FeatureEngineer


class ModelTrainer:

    def __init__(self):

        self.processor = DataPreprocessor(
            "data/vehicle_dataset.csv"
        )

        self.engineer = FeatureEngineer()

    def train(self):

        # Load dataset
        df = self.processor.load()

        # Clean dataset
        df = self.processor.clean(df)

        # Feature engineering
        df = self.engineer.create_features(df)

        # Features
        X = df.drop(
            columns=[
                "Fault",
                "Driving Mode",
                "Time Step",
            ],
            errors="ignore",
        )

        # Target
        y = df["Fault"]

        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y,
        )

        print("Training Random Forest...")

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            random_state=42,
            n_jobs=-1,
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        print("\nAccuracy:")
        print(accuracy_score(y_test, predictions))

        print("\nClassification Report:")
        print(classification_report(y_test, predictions))

        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, predictions))

        joblib.dump(model, "ai/models/random_forest.pkl")

        print("\nModel saved!")

        return model


if __name__ == "__main__":

    trainer = ModelTrainer()

    trainer.train()