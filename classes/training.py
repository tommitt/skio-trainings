import datetime
import pandas as pd
import streamlit as st
from utils import st_session_state

class Training:
    def __init__(self):
        self.name = ''
        self.date = datetime.date.today()
        self.discipline = 'ND'
        self.data = []

    def add_run(self, dnf=False):
        """
        Store athlete run and re-initialize session state.
        """
        self.data.append([
            st.session_state["running_athlete"],
            1000. if dnf else round(st.session_state["running_time"], 2),
        ])
        st_session_state.init_add_fields()
    
    def clear_last_run(self):
        """
        Clear last inserted run from data and re-initialize session state.
        """
        self.data = self.data[:-1]
        st_session_state.init_add_fields()
    
    def load_from_db(self, df):
        """
        Load Training object from trainings df.
        """
        self.name = df["name"].unique().item()
        self.date = df["date"].unique().item()
        self.discipline = df["discipline"].unique().item()
        self.data = df[["athlete", "time"]].values.tolist()

    def display_runs(self):
        """
        Create ordered DataFrame of the list of runs (self.data).
        Order athletes by best lap and highlight the best lap.
        """
        df = pd.DataFrame(data=self.data, columns=["Atleta", "Tempo"])

        # unstack laps on columns
        df["Giro"] = df.groupby("Atleta").transform("cumcount")
        df = df.set_index(["Atleta", "Giro"]).unstack()
        lap_cols = (df.columns.get_level_values("Giro").values + 1).astype(str)
        df.columns = lap_cols

        # order by best lap
        df["Best"] = df.min(axis=1)
        df = df.sort_values("Best").reset_index().drop(columns=["Best"])
        df.index = df.index + 1
        
        # return best lap highlighted
        return df.style.highlight_min(
            subset=lap_cols,
            axis=1,
            color="grey"
            ).format(precision=2, na_rep=' ')
