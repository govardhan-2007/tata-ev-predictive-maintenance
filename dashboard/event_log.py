import streamlit as st
from datetime import datetime


def log_event(message):

    if "event_log" not in st.session_state:
        st.session_state.event_log = []

    timestamp = datetime.now().strftime("%H:%M:%S")

    st.session_state.event_log.insert(
        0,
        f"{timestamp} - {message}"
    )

    # Keep only last 15 events
    st.session_state.event_log = (
        st.session_state.event_log[:15]
    )


def render_event_log():

    st.subheader("📋 Event Timeline")

    if "event_log" not in st.session_state:
        st.info("No events yet.")
        return

    for event in st.session_state.event_log:
        st.write(event)