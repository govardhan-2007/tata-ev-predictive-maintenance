

import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

from dashboard.ai_panel import render_ai_panel

from core.digital_twin import DigitalTwin

from dashboard.charts import render_live_chart
from dashboard.ui import load_css, title
from dashboard.sidebar import render_sidebar
from dashboard.cards import (
    render_metric_cards,
    render_health_card
)
from dashboard.digital_twin import render_digital_twin
from dashboard.alerts import render_alerts
from config import (
    DASHBOARD_INTERVAL,
    MAX_HISTORY
)
from ai.model_manager import initialize_models

from deep_learning.sequence_buffer import SequenceBuffer
from dashboard.model_comparison import render_model_comparison
from core.trip_manager import TripManager


from dashboard.event_log import (
    log_event,
    render_event_log,
)
def initialize():

    if "digital_twin" not in st.session_state:
        st.session_state.digital_twin = DigitalTwin()
    if "history" not in st.session_state:
        st.session_state.history = pd.DataFrame(
            columns=[
                "Speed",
                "RPM",
                "SOC",
                "Motor Temp",
                "Brake Temp",
                "Battery Voltage",
                "Current",
                "Torque",
                "Vibration",
                "Tyre Pressure",
                "Steering Angle",
            ]
    )
    if "sequence_buffer" not in st.session_state:
        st.session_state.sequence_buffer = SequenceBuffer()
    if "trip_manager" not in st.session_state:
        st.session_state.trip_manager = TripManager()
    if "simulation_running" not in st.session_state:
        st.session_state.simulation_running = False

    if "last_data" not in st.session_state:
        st.session_state.last_data = st.session_state.digital_twin.step()
        


def run_dashboard():

    st.set_page_config(
        page_title="Vehicle Health AI",
        page_icon="🚗",
        layout="wide",
    )

    load_css()

    initialize()

    initialize_models()

    settings = render_sidebar()

    trip = st.session_state.trip_manager

    if settings["start_trip"]:
        trip.start()

    if settings["pause_trip"]:
        trip.pause()

    if settings["reset_trip"]:
        trip.reset()
    
    if settings["start"]:
        st.session_state.simulation_running = True

    if settings["stop"]:
        st.session_state.simulation_running = False

    if (
        "last_scenario" not in st.session_state
        or st.session_state.last_scenario != settings["scenario"]
    ):

        log_event(
            f"Scenario changed to {settings['scenario']}"
        )

        st.session_state.last_scenario = settings["scenario"]

    st.session_state["fault"] = settings["fault"]

    if (
        "last_fault" not in st.session_state
        or st.session_state.last_fault != settings["fault"]
    ):

        log_event(
            f"Fault injected : {settings['fault']}"
        )

        st.session_state.last_fault = settings["fault"]

    st.session_state["scenario"] = settings["scenario"]

    if settings["auto_refresh"]:
        st_autorefresh(
            interval=settings["refresh_rate"] * 1000,
            key="dashboard_refresh",
        )

    title()

    twin = st.session_state.digital_twin

    if st.session_state.simulation_running:

        data = twin.step()

        st.session_state.last_data = data

    else:

        data = st.session_state.get(
            "last_data",
            twin.step()
        )
    if st.session_state.simulation_running:
        trip.update(
            speed=data["Speed"],
            power=data["Current"] * data["Battery Voltage"] / 1000,
            dt=0.1,
        )

    prediction = data.get("Fault", "Healthy")

    if (
        "last_prediction" not in st.session_state
        or st.session_state.last_prediction != prediction
    ):

        log_event(
            f"AI detected : {prediction}"
        )

        st.session_state.last_prediction = prediction

    sample = [
        data["Speed"],
        data["RPM"],
        data["Torque"],
        data["Battery Voltage"],
        data["SOC"],
        data["Current"],
        data["Motor Temp"],
        data["Brake Temp"],
        data["Vibration"],
        data["Tyre Pressure"],
        data["Steering Angle"],
    ]
    st.sidebar.write(
        f"Sequence Buffer: {len(st.session_state.sequence_buffer.buffer)}/50"
    )

    st.session_state.sequence_buffer.add(sample)
    new_row = pd.DataFrame([{
        "Speed": data["Speed"],
        "RPM": data["RPM"],
        "SOC": data["SOC"],
        "Motor Temp": data["Motor Temp"],
        "Brake Temp": data["Brake Temp"],
        "Battery Voltage": data["Battery Voltage"],
        "Current": data["Current"],
        "Torque": data["Torque"],
        "Vibration": data["Vibration"],
        "Tyre Pressure": data["Tyre Pressure"],
        "Steering Angle": data["Steering Angle"],
    }])

    st.session_state.history = pd.concat(
        [st.session_state.history, new_row],
        ignore_index=True,
    )

    if len(st.session_state.history) > MAX_HISTORY:
        st.session_state.history = (
            st.session_state.history.tail(MAX_HISTORY)
        )

    render_metric_cards(data)

    render_health_card(data)
    render_live_chart(
        st.session_state.history
    )

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        render_digital_twin(data)

    with right:

        st.subheader("🚗 Vehicle Status")

        st.metric(
            "Scenario",
            settings["scenario"]
        )

        st.metric(
            "Driving Mode",
            settings["mode"]
        )

        

        if settings["fault"] == "Healthy":
            st.success("🟢 Healthy")

        elif settings["fault"] == "Motor Fault":
            st.error("🔴 Motor Fault")

        else:
            st.warning(f"⚠ {settings['fault']}")

        st.divider()

        st.subheader("🚗 Trip Status")

        summary = trip.summary()

        st.metric(
            "Trip Time",
            f"{summary['Trip Time']} s"
        )

        st.metric(
            "Distance",
            f"{summary['Distance']} km"
        )

        st.metric(
            "Energy Used",
            f"{summary['Energy']} kWh"
        )

        if trip.running:
            st.success("🟢 Trip Running")
        else:
            st.warning("⏸ Trip Paused")
        st.divider()

        render_ai_panel(
            data,
            settings["ai_model"],
        )
    
        st.divider()

        render_model_comparison(data)

        st.divider()

        render_alerts(data)

        st.divider()

        render_event_log()
    