import pandas as pd


class FeatureEngineer:

    def create_features(self, df):

        df = df.copy()

        # ----------------------------
        # Speed
        # ----------------------------

        df["Acceleration"] = df["Speed"].diff().fillna(0)

        # ----------------------------
        # RPM
        # ----------------------------

        df["RPM Change"] = df["RPM"].diff().fillna(0)

        # ----------------------------
        # Motor Temperature
        # ----------------------------

        df["Motor Temp Change"] = (
            df["Motor Temp"].diff().fillna(0)
        )

        # ----------------------------
        # Battery
        # ----------------------------

        df["SOC Change"] = (
            df["SOC"].diff().fillna(0)
        )

        # ----------------------------
        # Rolling Features
        # ----------------------------

        df["Current Avg"] = (
            df["Current"]
            .rolling(5)
            .mean()
            .fillna(df["Current"])
        )

        df["RPM Avg"] = (
            df["RPM"]
            .rolling(5)
            .mean()
            .fillna(df["RPM"])
        )

        df["Temp Avg"] = (
            df["Motor Temp"]
            .rolling(5)
            .mean()
            .fillna(df["Motor Temp"])
        )

        df["Vibration Avg"] = (
            df["Vibration"]
            .rolling(5)
            .mean()
            .fillna(df["Vibration"])
        )

        return df