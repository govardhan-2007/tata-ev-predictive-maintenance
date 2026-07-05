class TripManager:

    def __init__(self):

        self.reset()

    def reset(self):

        self.running = False

        self.trip_time = 0.0      # seconds

        self.distance = 0.0       # km

        self.energy_used = 0.0    # kWh

    def start(self):

        self.running = True

    def pause(self):

        self.running = False

    def update(
        self,
        speed,
        power,
        dt,
    ):

        if not self.running:
            return

        self.trip_time += dt

        self.distance += (
            speed * dt / 3600
        )

        self.energy_used += (
            power * dt / 3600
        )

    def summary(self):

        return {

            "Trip Time": round(
                self.trip_time,
                1,
            ),

            "Distance": round(
                self.distance,
                2,
            ),

            "Energy": round(
                self.energy_used,
                2,
            ),

        }