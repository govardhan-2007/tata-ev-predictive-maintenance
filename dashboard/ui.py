import streamlit as st


def load_css():
    with open("assets/css/dashboard.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


def title():
    st.markdown(
        """
        <div class="main-title">
            🚗 Tata EV Predictive Maintenance Platform
        </div>

        <div class="sub-title">
            Real-Time Digital Twin | AI Powered Fault Detection | Vehicle Health Monitoring
        </div>
        """,
        unsafe_allow_html=True,
    )