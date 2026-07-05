import random
import streamlit as st


class DriverModel:

    def __init__(self):

        self.mode = "CITY"

        self.time = 0

        self.target_speed = 40.0

        self.current_throttle = 0.0

        self.current_brake = 0.0

    def update(self, current_speed=0):

        self.time += 1
        self.mode = st.session_state.get(
            "scenario",
            "City",
        ).upper()

        

        # Change target speed every 80 updates
        if (
            self.time % 80 == 0
            or self.mode != getattr(self, "last_mode", "")
        ):

            if self.mode == "CITY":
                self.target_speed = random.uniform(30, 55)

            elif self.mode == "HIGHWAY":
                self.target_speed = random.uniform(80, 110)

            elif self.mode == "TRAFFIC":
                self.target_speed = random.uniform(0, 25)
            
            elif self.mode == "RAIN":
                self.target_speed = random.uniform(25, 50)

            elif self.mode == "UPHILL":
                self.target_speed = random.uniform(35, 55)

            elif self.mode == "DOWNHILL":
                self.target_speed = random.uniform(45, 70)

            elif self.mode == "SPORT":
                self.target_speed = random.uniform(90, 150)

            elif self.mode == "ECO":
                self.target_speed = random.uniform(35, 65)
        self.last_mode = self.mode

        error = self.target_speed - current_speed

        # -------------------------
        # Throttle Controller
        # -------------------------

        if error > 2:

            self.current_throttle += 0.02

        elif error < -2:

            self.current_throttle -= 0.03

        else:

            self.current_throttle *= 0.98

        self.current_throttle = max(
            0.0,
            min(1.0, self.current_throttle)
        )

        # -------------------------
        # Brake Controller
        # -------------------------

        if current_speed > self.target_speed + 5:

            self.current_brake += 0.03

        else:

            self.current_brake *= 0.85

        self.current_brake = max(
            0.0,
            min(1.0, self.current_brake)
        )

        return {

            "Mode": self.mode,

            "Scenario": self.mode,

            "Target Speed": round(self.target_speed, 1),

            "Throttle": round(self.current_throttle, 3),

            "Brake": round(self.current_brake, 3),

        }