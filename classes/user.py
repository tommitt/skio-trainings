import streamlit as st
import pandas as pd
from classes.team import Team
from utils import st_session_state
from utils.settings import settings

class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.team = Team()

    def clear_team(self):
        self.team = Team()

    def load_team(self, team: Team):
        """
        Load team from loaded state following the right version.
        """
        if 'app_version' in team.__dict__.keys():
            if team.app_version == settings.version:
                self.team = team
            elif team.app_version in settings.deprecated_versions:
                self.load_deprecated_team(team)
            else:
                st.error("Questa versione dello Stato Skio non è più accettata. \
                    Contattaci per recuperare i tuoi dati!")
        else:
            # TODO: this must be removed in future versions
            team.app_version = settings.deprecated_versions[0]
            self.load_deprecated_team(team)
        
        st_session_state.init_add_fields()

    def load_deprecated_team(self, team: Team):
        if team.app_version == "alpha0.1":
            self.team.athletes = team.athletes
            self.team.training = team.training

            data = []
            for i, training in enumerate(team.trainings):
                data += [[
                    i,
                    training.date,
                    training.name,
                    training.discipline,
                    j,
                    training.data[j][0],
                    training.data[j][1],
                ] for j in range(len(training.data))]
            df = pd.DataFrame(data, columns=self.team.db.columns)
            df["time"] = df["time"].replace("DNF", 1000)
            self.team.db = df
        else:
            raise Exception("Wrong version for deprecated team loading")
