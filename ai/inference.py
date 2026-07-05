from unittest import loader

import joblib
import pandas as pd
import streamlit as st

from ai.model_loader import ModelLoader

from ai.feature_engineering import FeatureEngineer


class InferenceEngine:

    def __init__(self):

        loader = ModelLoader()

        selected_model = st.session_state.get(
            "selected_model",
            "Random Forest"
        )

        self.model = loader.load(selected_model)
        self.engineer = FeatureEngineer()
        self.feature_importance = dict(
        zip(
            self.model.feature_names_in_,
            self.model.feature_importances_
        )
)


    def predict(self, data):

        df = pd.DataFrame([data])

        df = self.engineer.create_features(df)

        drop_columns = [
            "Fault",
            "Driving Mode",
            "Time Step",
        ]

        df = df.drop(columns=drop_columns, errors="ignore")

        prediction = self.model.predict(df)[0]

        probabilities = self.model.predict_proba(df)[0]

        confidence = float(max(probabilities) * 100)

        probability_dict = {}

        for cls, prob in zip(self.model.classes_, probabilities):
            probability_dict[cls] = round(float(prob * 100), 2)

        return {
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "probabilities": probability_dict,
        }
    def explain_prediction(self, top_n=5):

        importance = sorted(
            self.feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return importance[:top_n]