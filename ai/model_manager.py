import streamlit as st

from ai.inference import InferenceEngine
from ai.inference_cnn import CNNInference
from ai.inference_xgb import XGBInference

# Uncomment these after creating them
# from ai.inference_xgb import XGBInference
# from ai.inference_cnn import CNNInference


def initialize_models():

    if "rf_engine" not in st.session_state:
        st.session_state.rf_engine = InferenceEngine()

    if "xgb_engine" not in st.session_state:
        st.session_state.xgb_engine = XGBInference()
    
    if "cnn_engine" not in st.session_state:
        st.session_state.cnn_engine = CNNInference()