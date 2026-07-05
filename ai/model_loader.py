import joblib
from tensorflow.keras.models import load_model


class ModelLoader:

    def __init__(self):

        self.models = {
            "Random Forest": "ai/models/random_forest.pkl",
            "XGBoost": "ai/models/xgboost.pkl",
            "CNN-LSTM": "ai/models/cnn_lstm.keras",
        }

    def load(self, model_name):

        if model_name == "CNN-LSTM":
            return load_model(self.models[model_name])

        return joblib.load(self.models[model_name])

    def get_available_models(self):

        return list(self.models.keys())