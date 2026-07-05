import pandas as pd

from core.digital_twin import DigitalTwin
from config import DATASET_SIZE


class DatasetGenerator:

    def __init__(self):

        self.simulator = DigitalTwin()

    def generate(self):

        records = []

        print("Generating physics-based dataset...")

        for i in range(DATASET_SIZE):

            sample = self.digital_twin.step()

            sample["Time Step"] = i

            records.append(sample)

            if i % 5000 == 0:
                print(f"{i} samples generated...")

        df = pd.DataFrame(records)

        df.to_csv(
            "data/vehicle_dataset.csv",
            index=False
        )

        print()

        print("Dataset Created Successfully!")

        print(df.head())

        print()

        print(df.describe())

        print()

        print(df["Driving Mode"].value_counts())

        return df


if __name__ == "__main__":

    DatasetGenerator().generate()