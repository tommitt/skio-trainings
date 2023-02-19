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

    def rename_athlete(self, old_name, new_name):
        """
        Rename one athlete of the team.
        """
        if new_name in self.athletes:
            st.error("Nome già presente")
        else:
            idx = self.athletes.index(old_name)
            self.athletes[idx] = new_name
            for i in range(len(self.trainings)):
                for j in range(len(self.trainings[i].data)):
                    if self.trainings[i].data[j][0] == old_name:
                        self.trainings[i].data[j][0] = new_name
            for j in range(len(self.training.data)):
                if self.training.data[j][0] == old_name:
                    self.training.data[j][0] = new_name
            st_session_state.init_add_fields()

    def add_training(self, init_training=True):
        """
        Store the current training in a list.
        """
        self.trainings.append(self.training)
        st_session_state.init_add_fields()
        if init_training:
            self.training = Training()

    def clear_training(self, i):
        """
        Remove from trainings the selected training.
        """
        self.trainings.pop(i)
    
    def select_training(self, i):
        """
        Save current training if it is not empty.
        Make the selected training the new current one.
        """
        if len(self.training.data) > 0:
            self.add_training(init_training=False)
        self.training = self.trainings.pop(i)

    def display_team(self):
        """
        Create DataFrame to display all team members.
        """
        df = pd.DataFrame(self.athletes, columns=["Atleta"])
        df.index += 1
        return df

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

    def trainings_info_df(self):
        """
        Create DataFrame to contain all trainings with relative info ordered by date.
        """
        data = [[              
                i,  
                self.trainings[i].date,
                self.trainings[i].name,
                self.trainings[i].discipline,
        ] for i in range(len(self.trainings))]

        df = pd.DataFrame(data, columns=["id_training", "Data", "Nome", "Disciplina"]) # TODO: add #Athletes + #Runs
        df = df.sort_values("Data").reset_index(drop=True)
        df.index += 1
        return df
