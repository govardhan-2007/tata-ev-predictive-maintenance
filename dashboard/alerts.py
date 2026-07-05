import streamlit as st


def render_alerts(data):

    st.subheader("🚨 Active Alerts")

    alerts = []

    if data["Motor Temp"] > 90:
        alerts.append(("🔴", "Motor temperature too high"))

    if data["Brake Temp"] > 120:
        alerts.append(("🟠", "Brake temperature increasing"))

    if data["SOC"] < 25:
        alerts.append(("🟡", "Battery SOC is low"))

    if data["Tyre Pressure"] < 30:
        alerts.append(("🔴", "Low tyre pressure"))

    if data["Vibration"] > 2.5:
        alerts.append(("🟠", "High vibration detected"))

    if not alerts:
        st.success("No active alerts")

    else:

        for icon, text in alerts:

            st.warning(f"{icon} {text}")