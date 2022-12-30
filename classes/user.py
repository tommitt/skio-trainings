import streamlit as st
from classes.team import Team
from utils import st_session_state

class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.team = Team()

    def load_team(self, team):
        self.team = team
        st_session_state.init_add_fields()
        st_session_state.set_chosen_training(self.team.training)

user = User()
