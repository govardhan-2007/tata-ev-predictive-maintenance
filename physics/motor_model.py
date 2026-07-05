import math
from physics.vehicle_config import (
    MAX_RPM,
    MAX_TORQUE,
    NOMINAL_VOLTAGE,
    MAX_CURRENT,
    WHEEL_RADIUS,
    GEAR_RATIO,
)

class MotorModel:

    def __init__(self):

        self.max_rpm = MAX_RPM
        self.max_torque = MAX_TORQUE
        self.nominal_voltage = NOMINAL_VOLTAGE

    def update(self, speed_kmh, throttle,battery_voltage):

        # Convert vehicle speed to motor RPM
        wheel_radius = WHEEL_RADIUS      # m
        gear_ratio = GEAR_RATIO

        speed_ms = speed_kmh / 3.6

        wheel_rpm = (
            speed_ms /
            (2 * math.pi * wheel_radius)
        ) * 60

        rpm = wheel_rpm * gear_ratio

        

        rpm = max(0, min(rpm, self.max_rpm))

        # Torque decreases as RPM increases
        if rpm < 4000:

            torque = self.max_torque * throttle

        else:

            torque = (
                self.max_torque
                * (4000 / rpm)
                * throttle
            )

        torque = max(torque, 40)

        # Angular velocity (rad/s)
        omega = (2 * math.pi * rpm) / 60

        # Mechanical Power (W)
        power = torque * omega

        # Motor efficiency
        if rpm < 2000:
            efficiency = 0.88

        elif rpm < 7000:
            efficiency = 0.95

        else:
            efficiency = 0.91

        electrical_power = power / efficiency
        # Heat generated inside the motor
        heat_loss = electrical_power - power

        # Battery current
        voltage = battery_voltage

        current = electrical_power / voltage

        current = max(current, 0)
        # Inverter current limit
        max_current = MAX_CURRENT

        current = min(current, max_current)

        return {

            "RPM": round(rpm, 1),

            "Torque": round(torque, 1),

            "Power": round(power / 1000, 2),      # kW

            "Current": round(current, 2),

            "Voltage": round(voltage, 1),

            "Efficiency": round(efficiency * 100, 1),

            "Heat Loss": round(heat_loss / 1000, 2)

        }