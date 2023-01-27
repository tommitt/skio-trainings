import streamlit as st
import pandas as pd
from classes.training import Training
from utils import st_session_state
from utils.settings import settings

class Team:
    def __init__(self):
        self.athletes = []
        self.training = Training()
        self.db = pd.DataFrame(
            columns=[
                "id_training",
                "date",
                "name",
                "discipline",
                "id_run",
                "athlete",
                "time",
                ]
            )
        self.app_version = settings.version

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
            self.db["athlete"].rename({old_name: new_name}, inplace=True)
            st_session_state.init_add_fields()

    def add_training(self, init_training=True):
        """
        Store the current training to trainings db.
        """
        df = pd.DataFrame(data=self.training.data, columns=["athlete", "time"])
        df["id_training"] = 0 if self.db.empty else self.db["id_training"].max() + 1
        df["date"] = self.training.date
        df["name"] = self.training.name
        df["discipline"] = self.training.discipline
        df["id_run"] = df.index
        
        self.db = pd.concat([self.db, df], ignore_index=True)
        st_session_state.init_add_fields()

        if init_training:
            self.training = Training()

    def clear_training(self, id):
        """
        Remove the selected training from trainings db.
        """
        self.db = self.db.loc[~(self.db["id_training"] == id)].reset_index(drop=True)

    def select_training(self, id):
        """
        Make the selected training the new current one and
        save current training if it is not empty.
        """
        if len(self.training.data) > 0:
            self.add_training(init_training=False)
        self.training.load_from_db(self.db.loc[self.db["id_training"] == id])
        self.db = self.db.loc[self.db["id_training"] != id].reset_index(drop=True)

    def display_team(self):
        """
        Create DataFrame to display all team members.
        """
        df = pd.DataFrame(self.athletes, columns=["Atleta"])
        df.index += 1
        return df

    def trainings_info_df(self):
        """
        Create DataFrame to contain all trainings with relative info ordered by date.
        """
        df = self.db.groupby(["id_training", "date", "name", "discipline"])[
            ["athlete", "id_run"]].nunique().reset_index()

        df.columns = ["id_training", "Data", "Nome", "Disciplina", "# Atleti", "# Runs"]
        df = df.sort_values("Data").reset_index(drop=True)
        df.index += 1
        return df
