import pandas as pd


class DataPreprocessor:

    def __init__(self, csv_path):

        self.csv_path = csv_path

    def load(self):

        df = pd.read_csv(self.csv_path)

        print("Dataset Loaded")

        print(df.shape)

        return df

    def clean(self, df):

        # Remove duplicates
        df = df.drop_duplicates()

        # Remove missing values
        df = df.dropna()

        # Remove impossible values
        df = df[df["Speed"] >= 0]
        df = df[df["SOC"] >= 0]
        df = df[df["Battery Voltage"] > 0]

        return df