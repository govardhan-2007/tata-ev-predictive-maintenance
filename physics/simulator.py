from physics.vehicle_dynamics import VehicleDynamics
from physics.motor_model import MotorModel
from physics.battery_model import BatteryModel
from physics.thermal_model import ThermalModel
from physics.driver_model import DriverModel
from physics.fault_model import FaultModel
from physics.degradation_model import DegradationModel
import random


class PhysicsSimulator:

    def __init__(self):

        self.vehicle = VehicleDynamics()
        self.motor = MotorModel()
        self.battery = BatteryModel()
        self.thermal = ThermalModel()
        self.driver = DriverModel()
        self.fault = FaultModel()
        self.degradation = DegradationModel()

        self.time_step = 0.1

        self.throttle = 0.0
        self.brake = 0.0

    
    

    def update(self):

        driver = self.driver.update(
            self.vehicle.speed
        )

        self.throttle = driver["Throttle"]
        self.brake = driver["Brake"]

        vehicle = self.vehicle.update(
            self.throttle,
            self.brake,
            self.time_step,
        )

        motor = self.motor.update(
            vehicle["speed"],
            self.throttle,
            self.battery.voltage,
        )

        battery = self.battery.update(
            motor["Current"],
            motor["Voltage"],
            self.time_step,
        )

        thermal = self.thermal.update(
            motor["Heat Loss"],
            vehicle["speed"],
            self.time_step,
        )
        brake_temp = 30 + self.brake * 120

        vibration = (
            0.5
            + motor["RPM"] / 12000
            + random.uniform(-0.1, 0.1)
        )

        tyre_pressure = 34 + random.uniform(-0.5, 0.5)

        steering = random.uniform(-15, 15)
        health = self.degradation.update(
            current=motor["Current"],
            motor_temp=thermal["Motor Temp"],
            brake_temp=brake_temp,
            vibration=vibration,
            speed=vehicle["speed"],
            dt=self.time_step,
        )

        

        

        data = {

            "Speed": round(vehicle["speed"], 2),

            "RPM": motor["RPM"],

            "Torque": motor["Torque"],

            "Battery Voltage": battery["Battery Voltage"],

            "SOC": battery["SOC"],

            "Current": motor["Current"],

            "Motor Temp": thermal["Motor Temp"],

            "Brake Temp": round(brake_temp, 2),

            "Vibration": round(vibration, 2),

            "Tyre Pressure": round(tyre_pressure, 2),

            "Steering Angle": round(steering, 2),

            "Driving Mode": driver["Mode"],

        }
        data = self.fault.apply(data)
        data.update(health)
        return data