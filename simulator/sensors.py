from physics.simulator import PhysicsSimulator
from config import SENSOR_INTERVAL
import time


class VirtualSensors:

    def __init__(self):

        self.simulator = PhysicsSimulator()

    def read(self):

        data = self.simulator.update()

        time.sleep(SENSOR_INTERVAL)

        return data