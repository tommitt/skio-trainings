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

    def clear_team(self):
        self.team = Team()
