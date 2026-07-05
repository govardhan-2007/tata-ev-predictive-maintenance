class DegradationModel:

    def __init__(self):

        self.motor_health = 100.0
        self.battery_health = 100.0
        self.brake_health = 100.0
        self.bearing_health = 100.0
        self.tyre_health = 100.0

    def update(
        self,
        current,
        motor_temp,
        brake_temp,
        vibration,
        speed,
        dt,
    ):

        # -------------------------
        # Motor
        # -------------------------

        motor_wear = (
            (current / 450) ** 2
            + max(0, motor_temp - 80) / 100
        ) * 0.0005 * dt

        self.motor_health -= motor_wear

        # -------------------------
        # Battery
        # -------------------------

        battery_wear = (
            current / 450
        ) * 0.0001 * dt

        self.battery_health -= battery_wear

        # -------------------------
        # Brake
        # -------------------------

        brake_wear = (
            max(0, brake_temp - 80) / 120
        ) * 0.0003 * dt

        self.brake_health -= brake_wear

        # -------------------------
        # Bearing
        # -------------------------

        bearing_wear = (
            vibration ** 2
        ) * 0.00015 * dt

        self.bearing_health -= bearing_wear

        # -------------------------
        # Tyres
        # -------------------------

        tyre_wear = (
            speed / 180
        ) * 0.0002 * dt

        self.tyre_health -= tyre_wear

        # Clamp values

        self.motor_health = max(0, self.motor_health)
        self.battery_health = max(0, self.battery_health)
        self.brake_health = max(0, self.brake_health)
        self.bearing_health = max(0, self.bearing_health)
        self.tyre_health = max(0, self.tyre_health)

        return {

            "Motor Health": round(self.motor_health,2),

            "Battery Health": round(self.battery_health,2),

            "Brake Health": round(self.brake_health,2),

            "Bearing Health": round(self.bearing_health,2),

            "Tyre Health": round(self.tyre_health,2),

        }