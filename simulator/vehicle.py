import random
import math


class Vehicle:

    def __init__(self):

        self.time = 0

        self.speed = 0

        self.rpm = 0

        self.acceleration = 0

        self.soc = 100

        self.soh = 100

        self.motor_temp = 35

        self.brake_temp = 30

        self.battery_voltage = 400

        self.current = 0

        self.power = 0

        self.torque = 0

        self.vibration = 0.2

        self.tyre_pressure = 34

        self.steering_angle = 0

    def update(self):

        self.time += 1

        self.acceleration = random.uniform(-2, 3)

        self.speed += self.acceleration

        self.speed = max(0, min(120, self.speed))

        self.rpm = 500 + self.speed * 45

        self.torque = 120 + self.acceleration * 40

        self.current = abs(self.torque) * 1.6

        self.power = (self.battery_voltage * self.current) / 1000

        self.motor_temp += 0.03 * self.current - 0.08

        self.motor_temp = max(30, min(120, self.motor_temp))

        self.brake_temp += max(0, -self.acceleration) * 2

        self.brake_temp -= 0.3

        self.brake_temp = max(25, min(180, self.brake_temp))

        self.soc -= self.power / 100000

        self.soc = max(0, self.soc)

        self.soh -= 0.00002

        self.vibration = 0.2 + self.speed / 120 + random.uniform(0, 0.5)

        self.tyre_pressure += random.uniform(-0.02, 0.02)

        self.steering_angle = random.randint(-35, 35)

    def get_state(self):

        return {

            "Speed": round(self.speed, 2),

            "RPM": int(self.rpm),

            "Motor Temp": round(self.motor_temp, 2),

            "Brake Temp": round(self.brake_temp, 2),

            "Battery Voltage": round(self.battery_voltage, 2),

            "Current": round(self.current, 2),

            "Power (kW)": round(self.power, 2),

            "Torque": round(self.torque, 2),

            "SOC": round(self.soc, 2),

            "SOH": round(self.soh, 2),

            "Tyre Pressure": round(self.tyre_pressure, 2),

            "Vibration": round(self.vibration, 2),

            "Steering Angle": self.steering_angle

        }