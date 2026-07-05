from physics.simulator import PhysicsSimulator


class DigitalTwin:

    def __init__(self):
        self.simulator = PhysicsSimulator()
        self.current_state = {}

    def step(self):
        """
        Advance the simulation by one timestep.
        """
        self.current_state = self.simulator.update()
        return self.current_state

    def get_state(self):
        """
        Return the latest vehicle state.
        """
        return self.current_state

    def reset(self):
        """
        Restart the simulation.
        """
        self.simulator = PhysicsSimulator()
        self.current_state = {}