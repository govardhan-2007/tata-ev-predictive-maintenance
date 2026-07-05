class BatteryModel:

    def __init__(self):

        self.capacity = 75.0      # kWh

        self.soc = 100.0 # State of Charge

        self.soh = 100.0 # State of Health

        self.voltage = 360.0

    def update(self, current, voltage, dt):

        power = abs(current * voltage) / 1000      # kW

        energy = power * dt / 3600            # kWh

        self.soc -= energy / self.capacity * 100

        self.soc = min(100.0, max(0.0, self.soc))
        
        # Battery ages very slowly
        self.soh -= energy * 0.00001

        self.soh = max(80.0, self.soh)
        # Battery voltage depends on SOC
        battery_voltage = 300 + (self.soc / 100) * 60
        self.voltage = battery_voltage

        return {

            "SOC": round(self.soc, 2),

            "Battery SOH": round(self.soh, 2),

            "Battery Voltage": round(battery_voltage, 1),

        }