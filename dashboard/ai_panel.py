import streamlit as st




from advisor.maintenance_advisor import MaintenanceAdvisor
from reports.pdf_report import PDFReport






def render_ai_panel(
    data,
    model_name,
):

    # -----------------------------
    # Select AI Model
    # -----------------------------

    if model_name == "Random Forest":

        ai = st.session_state.rf_engine

        result = ai.predict(data)

    elif model_name == "CNN-LSTM":

        if not st.session_state.sequence_buffer.ready():

            st.warning("Waiting for 50 sensor readings...")

            return

        ai = st.session_state.cnn_engine

        sequence = st.session_state.sequence_buffer.get_sequence()

        result = ai.predict(sequence)

    else:

        ai = st.session_state.rf_engine

        result = ai.predict(data)

    prediction = result["prediction"]
    confidence = result["confidence"]
    probabilities = result["probabilities"]
    advisor = MaintenanceAdvisor()

    recommendation = advisor.get_recommendation(
        prediction
    )
    pdf = PDFReport()

    st.subheader("🤖 AI Prediction")

    if prediction == "Healthy":
        
        if confidence > 95:
            st.success("🟢 Vehicle Healthy")

        elif confidence > 80:
            st.warning("🟡 Minor anomaly detected")

        else:
            st.error("🔴 Possible fault developing")

    elif prediction == "Motor Fault":
        st.error("🔴 Motor Fault Detected")

    elif prediction == "Brake Fault":
        st.warning("🟡 Brake Fault Detected")

    elif prediction == "Battery Fault":
        st.warning("🟡 Battery Fault Detected")

    elif prediction == "Bearing Fault":
        st.warning("🟠 Bearing Fault Detected")

    elif prediction == "Tyre Fault":
        st.warning("🟠 Tyre Fault Detected")

    else:
        st.info(prediction)

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Prediction",
            prediction
        )

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

    with c2:

        motor_health = data.get("Motor Health", 100)

        rul = int(motor_health * 250)

        st.metric(
            "Motor Health",
            f"{motor_health:.1f}%"
        )

        st.metric(
            "Estimated RUL",
            f"{rul:,} km"
        )
    st.divider()

    

    st.subheader("🔧 Maintenance Recommendation")

    priority = recommendation["priority"]

    if priority == "Critical":
        st.error(f"Priority : {priority}")

    elif priority == "High":
        st.warning(f"Priority : {priority}")

    else:
        st.success(f"Priority : {priority}")

    st.markdown(
        f"""
    **Recommended Action**

    {recommendation['action']}

    ---

    **Inspection**

    {recommendation['inspection']}
    """
    )
    st.divider()

    st.subheader("📊 AI Confidence")

    for fault, probability in sorted(
            probabilities.items(),
            key=lambda x: x[1],
            reverse=True):

        st.write(f"**{fault}({probability:.2f}%)**")

        st.progress(probability / 100)

        
    st.divider()

    if model_name != "CNN-LSTM":

        st.divider()

        st.subheader("🧠 AI Explainability")

        importance = ai.explain_prediction()

        for feature, score in importance:

            percentage = score * 100

            st.write(f"**{feature}** ({percentage:.1f}%)")

            st.progress(float(score))

        for feature, score in importance:

            percentage = score * 100

            st.write(f"**{feature}** ({percentage:.1f}%)")

            st.progress(float(score))   
            
    if st.button("📄 Generate Health Report"):

        filename = pdf.generate(
            data,
            prediction,
            confidence,
            recommendation,
        )

        st.success("✅ Report generated successfully.")

        with open(filename, "rb") as f:

            st.download_button(
                label="⬇ Download Report",
                data=f,
                file_name="vehicle_health_report.pdf",
                mime="application/pdf",
            )

    st.divider()