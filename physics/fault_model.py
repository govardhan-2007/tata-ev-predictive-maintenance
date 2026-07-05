import random
import streamlit as st


class FaultModel:

    def __init__(self):

        self.motor_fault = False
        self.brake_fault = False
        self.battery_fault = False
        self.tyre_fault = False
        self.bearing_fault = False

        self.time = 0
        self.fault_severity = 0.0

    def update(self):

        self.time += 1

        # Every 600 simulation steps (~60 s)
        fault = st.session_state.get(
            "fault",
            "Healthy",
            )

        self.motor_fault = fault == "Motor Fault"

        self.brake_fault = fault == "Brake Fault"

        self.battery_fault = fault == "Battery Fault"

        self.tyre_fault = fault == "Tyre Fault"

        self.bearing_fault = fault == "Bearing Fault"

        # Gradually increase or decrease fault severity
        if fault != "Healthy":
            self.fault_severity = min(
                1.0,
                self.fault_severity + 0.02,
            )
        else:
            self.fault_severity = max(
                0.0,
                self.fault_severity - 0.05,
            )

    def apply(self, data):

        self.update()

        active_fault = "Healthy"

        if self.motor_fault:

            data["Motor Temp"] += (
                40 * self.fault_severity
            )

            data["Current"] *= (
                1 + 0.30 * self.fault_severity
            )

            active_fault = "Motor Fault"

        if self.brake_fault:

            data["Brake Temp"] += (
                70 * self.fault_severity
            )

            active_fault = "Brake Fault"

        if self.battery_fault:

            data["SOC"] -= (
                10 * self.fault_severity
            )

            data["Battery Voltage"] -= (
                30 * self.fault_severity
            )

            active_fault = "Battery Fault"

        if self.tyre_fault:

            data["Tyre Pressure"] -= (
                8 * self.fault_severity
            )

            active_fault = "Tyre Fault"

        if self.bearing_fault:

            data["Vibration"] += (
                5 * self.fault_severity
            )

            active_fault = "Bearing Fault"

        data["Fault"] = active_fault

        return data