import random
import pandas as pd
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
from config import DATASET_SIZE


def generate_sample():

    # ----------------------------
    # Base Driving Conditions
    # ----------------------------

    speed = round(random.uniform(0, 120), 2)
    rpm = int(800 + speed * 45 + random.randint(-200, 200))

    motor_temp = round(35 + speed * 0.45 + random.uniform(-5, 5), 2)
    brake_temp = round(30 + speed * 0.65 + random.uniform(-8, 8), 2)

    soc = round(random.uniform(20, 100), 2)
    battery_voltage = round(random.uniform(320, 410), 2)

    current = round(random.uniform(10, 220), 2)

    torque = round(speed * 2.4 + random.uniform(-20, 20), 2)

    vibration = round(random.uniform(0.2, 4.5), 2)

    tyre_pressure = round(random.uniform(30, 36), 2)

    steering_angle = round(random.uniform(-35, 35), 2)

    # ----------------------------
    # Fault Classification
    # ----------------------------

    fault = "Healthy"

    if motor_temp > 105:
        fault = "Motor Fault"

    elif brake_temp > 150:
        fault = "Brake Fault"

    elif soc < 25:
        fault = "Battery Fault"

    elif abs(steering_angle) > 30 and speed > 80:
        fault = "Steering Fault"

    return {

        "Speed": speed,
        "RPM": rpm,
        "Motor Temp": motor_temp,
        "Brake Temp": brake_temp,
        "Battery SOC": soc,
        "Battery Voltage": battery_voltage,
        "Current": current,
        "Torque": torque,
        "Vibration": vibration,
        "Tyre Pressure": tyre_pressure,
        "Steering Angle": steering_angle,
        "Fault": fault,

    }


def generate_dataset():

    print("Generating dataset...")

    data = []

    for _ in range(DATASET_SIZE):
        data.append(generate_sample())

    df = pd.DataFrame(data)

    df.to_csv("vehicle_dataset.csv", index=False)

    print(df.head())

    print()

    print("Dataset Shape:", df.shape)

    print()

    print(df["Fault"].value_counts())

    print()

    print("Dataset saved as vehicle_dataset.csv")


if __name__ == "__main__":
    generate_dataset()