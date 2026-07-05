import streamlit as st


def render_maintenance(data):

    st.subheader("🔧 Maintenance Advisor")

    recommendations = []

    if data["Motor Temp"] > 90:
        recommendations.append(
            "Inspect motor cooling system."
        )

    if data["Brake Temp"] > 120:
        recommendations.append(
            "Inspect brake pads and brake disc."
        )

    if data["SOC"] < 25:
        recommendations.append(
            "Recharge battery immediately."
        )

    if data["Tyre Pressure"] < 30:
        recommendations.append(
            "Inflate tyres to recommended pressure."
        )

    if data["Vibration"] > 2.5:
        recommendations.append(
            "Inspect suspension and wheel balancing."
        )

    if not recommendations:

        st.success(
            "Vehicle is operating normally."
        )

    else:

        for item in recommendations:

            st.write(f"✅ {item}")