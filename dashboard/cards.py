import streamlit as st


def _status_color(value, good=90, warning=70):
    if value >= good:
        return "🟢"
    elif value >= warning:
        return "🟡"
    return "🔴"


def render_metric_cards(data):

    speed = data.get("Speed", 0)
    rpm = data.get("RPM", 0)
    soc = data.get("SOC", 0)
    temp = data.get("Motor Temp", 0)
    voltage = data.get("Battery Voltage", 0)
    current = data.get("Current", 0)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric(
            "🚗 Speed",
            f"{speed:.1f} km/h"
        )

    with col2:
        st.metric(
            "⚙ RPM",
            f"{int(rpm)}"
        )

    with col3:
        st.metric(
            "🔋 Battery",
            f"{soc:.1f}%"
        )

    with col4:
        st.metric(
            "🌡 Motor Temp",
            f"{temp:.1f}°C"
        )

    with col5:
        st.metric(
            "⚡ Voltage",
            f"{voltage:.1f} V"
        )

    with col6:
        st.metric(
            "🔌 Current",
            f"{current:.1f} A"
        )


def render_health_card(data):

    engine = max(0, 100 - (data["Motor Temp"] - 35))
    battery = data["SOC"]
    brakes = max(0, 100 - data["Brake Temp"] / 2)
    tyres = max(0, 100 - abs(data["Tyre Pressure"] - 34) * 8)

    health = (
        engine +
        battery +
        brakes +
        tyres
    ) / 4

    c1, c2 = st.columns([2, 1])

    with c1:

        st.progress(health / 100)

        st.metric(
            "❤️ Overall Vehicle Health",
            f"{health:.1f}%"
        )

    with c2:

        if health > 90:
            st.success("🟢 Healthy")

        elif health > 75:
            st.warning("🟡 Warning")

        else:
            st.error("🔴 Critical")