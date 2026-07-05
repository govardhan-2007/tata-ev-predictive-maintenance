import os
import pandas as pd


class DataCollector:

    def __init__(self):

        self.file = "data/live_training_data.csv"

    def save(self, sample):

        df = pd.DataFrame([sample])

        if os.path.exists(self.file):

            df.to_csv(
                self.file,
                mode="a",
                header=False,
                index=False
            )

        else:

            df.to_csv(
                self.file,
                index=False
            )