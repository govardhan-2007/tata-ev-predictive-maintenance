from physics.vehicle_config import AMBIENT_TEMP

class ThermalModel:

    def __init__(self):

        self.motor_temp = AMBIENT_TEMP
    def update(self, heat_loss, speed, dt):

        # Electrical heat generation (kW equivalent)
        heat = heat_loss

        cooling = (
            0.15
            + speed * 0.012
        )

        temperature_change = (
            heat
            - cooling
        ) * dt

        #THERMAL inertia
        self.motor_temp += (
            AMBIENT_TEMP
            - self.motor_temp
        ) * 0.002

        self.motor_temp += temperature_change 

        # Cooling system limits excessive temperatures
        if self.motor_temp > 125:

            self.motor_temp -= (
                self.motor_temp - 125
            ) * 0.05
        if self.motor_temp < AMBIENT_TEMP:
            self.motor_temp = AMBIENT_TEMP+5

        return {

            "Motor Temp": round(self.motor_temp, 2)

        }