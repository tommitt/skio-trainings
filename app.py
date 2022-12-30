import streamlit as st
from classes.user import user
from screens.training import training_main_screen
from screens.team import team_sidebar_screen

st.set_page_config(page_title="Skio - Archivia i tuoi allenamenti!", page_icon="❄️", layout="wide")

training_main_screen(user.team)

with st.sidebar:
    team_sidebar_screen(user)
