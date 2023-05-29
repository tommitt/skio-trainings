import streamlit as st


def init_chrono():
    st.session_state["chrono_running"] = False
    st.session_state["chrono_start_ts"] = None
    st.session_state["chrono_stop_ts"] = None


def init_training():
    st.session_state["running_time"] = 0.0
    init_chrono()
