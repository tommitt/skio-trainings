import streamlit as st

def init_add_fields():
    """
    Initialize session state values when add buttons are clicked.
    """
    st.session_state["running_time"] = 0.0
    st.session_state["new_athlete_name"] = ''
    st.session_state["rename_athlete_name"] = ''
