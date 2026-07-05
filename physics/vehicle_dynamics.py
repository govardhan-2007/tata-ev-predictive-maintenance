import math
import random


class VehicleDynamics:

    def __init__(self):

        # Base vehicle mass (without passengers)
        self.vehicle_mass = 1800

        # Driver
        self.driver_mass = 75

        # Passengers
        self.passenger_mass = 0

        # Cargo
        self.cargo_mass = 0

        # Total mass
        self.mass = (
            self.vehicle_mass
            + self.driver_mass
            + self.passenger_mass
            + self.cargo_mass
        )

        self.speed = 0.0           # m/s

        self.acceleration = 0.0

        self.position = 0.0

        self.drag_coeff = 0.29

        self.frontal_area = 2.2

        self.air_density = 1.225

        self.rolling_resistance = 0.015

        self.gravity = 9.81
    
    def update_vehicle_mass(self):

        # Change passenger count occasionally
        if self.position % 1000 < 2:

            passenger_count = math.floor(
                random.uniform(0, 4)
            )

            self.passenger_mass = passenger_count * 70

            self.cargo_mass = random.uniform(0, 80)

        self.mass = (
            self.vehicle_mass
            + self.driver_mass
            + self.passenger_mass
            + self.cargo_mass
        )

        

        

    def update(self, throttle, brake, dt):

        traction_force = throttle * 4500

        brake_force = brake * 6000

        drag_force = (
            0.5
            * self.air_density
            * self.drag_coeff
            * self.frontal_area
            * self.speed ** 2
        )

        rolling_force = (
            self.mass
            * self.gravity
            * self.rolling_resistance
        )

        net_force = (
            traction_force
            - brake_force
            - drag_force
            - rolling_force
        )

        self.acceleration = net_force / self.mass

        self.speed += self.acceleration * dt

        if self.speed < 0:
            self.speed = 0

        self.position += self.speed * dt

        return {

            "speed": self.speed * 3.6,

            "acceleration": self.acceleration,

            "position": self.position,

        }