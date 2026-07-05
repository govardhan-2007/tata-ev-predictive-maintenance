import streamlit as st


def render_sidebar():
    """
    Render the left sidebar and return user selections.
    """

    st.sidebar.title("🚗 Vehicle Health AI")

    st.sidebar.markdown("---")

    driving_mode = st.sidebar.selectbox(
        "Driving Mode",
        ["Eco", "City", "Sport"],
        index=1,
    )
    driving_scenario = st.sidebar.selectbox(
        "Driving Scenario",
        [
            "City",
            "Highway",
            "Traffic",
            "Uphill",
            "Downhill",
            "Rain",
            "Eco",
            "Sport",
        ],
        index=0,
    )

    auto_refresh = st.sidebar.checkbox(
        "Auto Refresh",
        value=True,
    )

    refresh_rate = st.sidebar.slider(
        "Refresh Interval (seconds)",
        min_value=1,
        max_value=5,
        value=1,
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader("Simulation")

    start_simulation = st.sidebar.button("▶ Start")

    stop_simulation = st.sidebar.button("⏹ Stop")

    st.sidebar.markdown("### 🚗 Trip Controls")

    start_trip = st.sidebar.button("▶ Start Trip")

    pause_trip = st.sidebar.button("⏸ Pause Trip")

    reset_trip = st.sidebar.button("🔄 Reset Trip")

    st.sidebar.markdown("---")

    st.sidebar.subheader("🤖 AI Engine")

    ai_model = st.sidebar.selectbox(
        "Select Model",
        [
            "Random Forest",
            "XGBoost",
            "CNN-LSTM",
        ],
    )
    st.sidebar.markdown("---")

    st.sidebar.subheader("⚠ Fault Injection")

    fault_type = st.sidebar.selectbox(
        "Inject Fault",
        [
            "Healthy",
            "Motor Fault",
            "Battery Fault",
            "Brake Fault",
            "Bearing Fault",
            "Tyre Fault",
        ],
    )
    st.sidebar.subheader("System Status")

    st.sidebar.success("Simulator Online")

    if "rf_engine" in st.session_state:
        st.sidebar.success("🤖 AI Engine: Loaded")
        st.sidebar.caption(f"Model: {ai_model}")
    else:
        st.sidebar.error("🤖 AI Engine: Not Loaded")
    return {
        "mode": driving_mode,
        "scenario": driving_scenario,
        "auto_refresh": auto_refresh,
        "refresh_rate": refresh_rate,
        "start": start_simulation,
        "stop": stop_simulation,
        "ai_model": ai_model,
        "fault": fault_type,
        "start_trip": start_trip,
        "pause_trip": pause_trip,
        "reset_trip": reset_trip,
    }