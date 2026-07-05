import streamlit as st
import time


def render_model_comparison(data):

    st.subheader("🆚 AI Model Comparison")

    results = []

    # ------------------------
    # Random Forest
    # ------------------------

    start = time.perf_counter()

    rf = st.session_state.rf_engine

    rf_result = rf.predict(data)

    rf_time = (time.perf_counter() - start) * 1000

    results.append({
        "Model": "🌳 Random Forest",
        "Prediction": rf_result["prediction"],
        "Confidence": f"{rf_result['confidence']:.2f}%",
        "Time (ms)": f"{rf_time:.2f}"
    })

    # ------------------------
    # XGBoost
    # ------------------------

    start = time.perf_counter()

    xgb = st.session_state.xgb_engine

    xgb_result = xgb.predict(data)

    xgb_time = (time.perf_counter() - start) * 1000

    results.append({
        "Model": "⚡ XGBoost",
        "Prediction": xgb_result["prediction"],
        "Confidence": f"{xgb_result['confidence']:.2f}%",
        "Time (ms)": f"{xgb_time:.2f}"
    })

    # ------------------------
    # CNN-LSTM
    # ------------------------

    if st.session_state.sequence_buffer.ready():

        start = time.perf_counter()

        sequence = st.session_state.sequence_buffer.get_sequence()

        cnn = st.session_state.cnn_engine

        cnn_result = cnn.predict(sequence)

        cnn_time = (time.perf_counter() - start) * 1000

        results.append({
            "Model": "🧠 CNN-LSTM",
            "Prediction": cnn_result["prediction"],
            "Confidence": f"{cnn_result['confidence']:.2f}%",
            "Time (ms)": f"{cnn_time:.2f}"
        })

    else:

        results.append({
            "Model": "🧠 CNN-LSTM",
            "Prediction": "Waiting...",
            "Confidence": "--",
            "Time (ms)": "--"
        })

    st.table(results)