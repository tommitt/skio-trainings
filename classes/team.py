import streamlit as st
import pandas as pd
from classes.training import Training
from utils import st_session_state

class Team:
    def __init__(self):
        self.athletes = []
        self.trainings = []
        self.training = Training()

    def add_athlete(self, name):
        """
        Add athlete name to the team.
        """
        if name in self.athletes:
            st.error("Nome già presente")
        else:
            self.athletes.append(name)
            st_session_state.init_add_fields()

    def add_training(self):
        """
        Store the current training in a list.
        """
        self.trainings.append(self.training)
        self.training = Training()
        st_session_state.init_add_fields()

    def select_training(self, i):
        """
        Save current training if it is not empty.
        Make the selected training the new current one.
        """
        if len(self.training.data) > 0:
            self.trainings.append(self.training)
        self.training = self.trainings.pop(i)
        st_session_state.set_chosen_training(self.training)
    
    def display_team(self):
        """
        Create DataFrame to display all team members.
        """
        df = pd.DataFrame(self.athletes, columns=["Atleta"])
        df.index += 1
        return df

    # @st.cache
    def trainings_df(self):
        """
        Create DataFrame to contain all runs of each training.
        """        
        data = []
        for i in range(len(self.trainings)):
            data += [[
                i,
                self.trainings[i].date,
                self.trainings[i].name,
                self.trainings[i].discipline,
                j,
                self.trainings[i].data[j][0],
                self.trainings[i].data[j][1],
            ] for j in range(len(self.trainings[i].data))]

        return pd.DataFrame(
            data,
            columns=["id_training", "date", "name", "discipline", "id_run", "athlete", "time"]
        )

    def export_data(self):
        """
        Export all trainings to a csv.
        """
        return self.trainings_df().to_csv().encode('utf-8')
