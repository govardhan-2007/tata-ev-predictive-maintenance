import streamlit as st
import plotly.graph_objects as go


def create_chart(df, column, color, title):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[column],
            mode="lines",
            line=dict(color=color, width=3),
            fill="tozeroy",
        )
    )

    fig.update_layout(

        title=title,

        template="plotly_dark",

        height=250,

        margin=dict(
            l=10,
            r=10,
            t=40,
            b=10,
        ),

        paper_bgcolor="#0E1117",

        plot_bgcolor="#0E1117",

        xaxis_title="",

        yaxis_title="",

        showlegend=False,

    )

    return fig


def render_live_chart(history):

    if len(history) < 2:
        st.info("Waiting for sensor data...")
        return

    c1, c2 = st.columns(2)

    with c1:

        st.plotly_chart(

            create_chart(
                history,
                "Speed",
                "#00E5FF",
                "🚗 Speed",
            ),

            use_container_width=True,

            key="speed_chart"

        )

    with c2:

        st.plotly_chart(

            create_chart(
                history,
                "RPM",
                "#FF3D00",
                "⚙ RPM",
            ),

            use_container_width=True,

            key="rpm_chart"

        )

    c3, c4 = st.columns(2)

    with c3:

        st.plotly_chart(

            create_chart(
                history,
                "Motor Temp",
                "#FFC107",
                "🌡 Motor Temperature",
            ),

            use_container_width=True,

            key="temp_chart"

        )

    with c4:

        st.plotly_chart(

            create_chart(
                history,
                "SOC",
                "#4CAF50",
                "🔋 Battery SOC",
            ),

            use_container_width=True,

            key="soc_chart"

        )