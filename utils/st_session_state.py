import datetime
import streamlit as st

def init_new_training():
    """
    Initialize session state values when new training is created.
    """
    st.session_state["training_name"] = ''
    st.session_state["training_date"] = datetime.date.today()
    st.session_state["training_discipline"] = "ND"

def init_add_fields():
    """
    Initialize session state values when add buttons are clicked.
    """
    st.session_state["time"] = 0.0
    st.session_state["new_athlete_name"] = ''

def set_chosen_training(training):
    """
    Set session state values for a given training.
    """
    st.session_state["training_name"] = training.name
    st.session_state["training_date"] = training.date
    st.session_state["training_discipline"] = training.discipline
