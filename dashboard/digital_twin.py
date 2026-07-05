import streamlit as st


def get_status(value):

    if value >= 90:
        return "🟢"

    elif value >= 70:
        return "🟡"

    else:
        return "🔴"


def render_digital_twin(data):

    st.subheader("🚗 Vehicle Digital Twin")

    engine = data["Motor Health"]

    battery = data["Battery Health"]

    brakes = data["Brake Health"]

    steering = 100.0        # until you simulate steering wear

    suspension = data["Bearing Health"]

    tyres = data["Tyre Health"]

    overall = (
        engine +
        battery +
        brakes +
        steering +
        suspension +
        tyres
    ) / 6

    st.markdown("---")

    c1, c2 = st.columns([1.2, 1])

    with c1:

        st.markdown("## 🚘 Vehicle")

        st.write(f"{get_status(engine)} Motor")
        st.progress(engine / 100)
        st.caption(f"{engine:.1f}%")

        st.write(f"{get_status(battery)} Battery")
        st.progress(battery / 100)
        st.caption(f"{battery:.1f}%")

        st.write(f"{get_status(brakes)} Brakes")
        st.progress(brakes / 100)
        st.caption(f"{brakes:.1f}%")

        st.write(f"{get_status(steering)} Steering")
        st.progress(steering / 100)
        st.caption(f"{steering:.1f}%")

        st.write(f"{get_status(suspension)} Suspension")
        st.progress(suspension / 100)
        st.caption(f"{suspension:.1f}%")

        st.write(f"{get_status(tyres)} Tyres")
        st.progress(tyres / 100)
        st.caption(f"{tyres:.1f}%")

    with c2:

        st.metric(
            "❤️ Overall Health",
            f"{overall:.1f}%"
        )

        st.progress(overall / 100)

        st.markdown("")

        if overall > 90:

            st.success("Vehicle Healthy")

        elif overall > 75:

            st.warning("Service Recommended")

        else:

            st.error("Immediate Inspection Required")