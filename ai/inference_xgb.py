import pandas as pd
import joblib

from ai.model_loader import ModelLoader
from ai.feature_engineering import FeatureEngineer


class XGBInference:

    def __init__(self):

        loader = ModelLoader()

        self.model = loader.load("XGBoost")

        self.engineer = FeatureEngineer()

        self.encoder = joblib.load(
            "deep_learning/data/label_encoder.pkl"
        )

    def predict(self, data):

        df = pd.DataFrame([data])

        df = self.engineer.create_features(df)

        df = df.drop(
            columns=[
                "Fault",
                "Driving Mode",
                "Time Step",
            ],
            errors="ignore",
        )

        prediction = int(self.model.predict(df)[0])

        prediction = self.encoder.inverse_transform(
            [prediction]
        )[0]

        probabilities = self.model.predict_proba(df)[0]

        confidence = float(max(probabilities) * 100)

        probability_dict = {}

        for cls, prob in zip(
            self.encoder.classes_,
            probabilities,
        ):

            probability_dict[cls] = round(
                float(prob * 100),
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