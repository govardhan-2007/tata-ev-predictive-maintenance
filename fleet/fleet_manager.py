from simulator.sensors import VirtualSensors


class FleetManager:

    def __init__(self, num_vehicles=5):

        self.vehicles = {}

        for i in range(num_vehicles):

            vehicle_id = f"EV-{i+1:03d}"

            self.vehicles[vehicle_id] = VirtualSensors()

    def update(self):

        fleet_data = {}

        for vehicle_id, sensor in self.vehicles.items():

            fleet_data[vehicle_id] = sensor.read()

        return fleet_data