import random


class FaultInjector:

    def __init__(self):

        self.active_fault = None

    def inject_random_fault(self):

        faults = [

            None,

            "Motor Overheating",

            "Brake Wear",

            "Battery Degradation",

            "Tyre Pressure Loss",

            "Steering Vibration"

        ]

        self.active_fault = random.choice(faults)

        return self.active_fault