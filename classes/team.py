from datetime import datetime

import pandas as pd
import streamlit as st
from google.cloud import firestore

from classes.training import Training
from utils import st_session_state


class Team:
    def __init__(self):
        self.id = None
        self.athletes = []
        self.trainings = []
        self.training = Training()

    def add_athlete(self, name):
        """
        Add athlete name to the team and save it into db.
        """
        if name in self.athletes:
            return -1
        else:
            # save into db
            team_ref = st.session_state.db.collection("teams").document(self.id)
            team_ref.update({"athletes": firestore.ArrayUnion([name])})

            # store into current object
            self.athletes = sorted(self.athletes + [name])

            return 0

    def rename_athlete(self, old_name, new_name):
        """
        Rename one athlete of the team and update db.
        """
        if new_name in self.athletes:
            return -1
        else:
            # update db: athletes
            team_ref = st.session_state.db.collection("teams").document(self.id)
            team_ref.update({"athletes": firestore.ArrayRemove([old_name])})
            team_ref.update({"athletes": firestore.ArrayUnion([new_name])})
            # update db: trainings
            for training in team_ref.collection("trainings").stream():
                for data in (
                    training.reference.collection("data")
                    .where("athlete", "==", old_name)
                    .stream()
                ):
                    data.reference.update({"athlete": new_name})

            # update object
            idx = self.athletes.index(old_name)
            self.athletes[idx] = new_name
            self.athletes = sorted(self.athletes)
            for i in range(len(self.trainings)):
                for j in range(len(self.trainings[i].data)):
                    if self.trainings[i].data[j][0] == old_name:
                        self.trainings[i].data[j][0] = new_name
            for j in range(len(self.training.data)):
                if self.training.data[j][0] == old_name:
                    self.training.data[j][0] = new_name

            return 0

    def add_training(self):
        """
        Save the current training into db and object if it was not saved before, update it otherwise.
        """
        trainings_ref = st.session_state.db.collection(
            "teams/" + self.id + "/trainings"
        )
        training_dict = {
            "name": self.training.name,
            "date": datetime.combine(self.training.date, datetime.min.time()),
            "discipline": self.training.discipline,
        }

        if self.training.id is None:
            # training has not been saved yet - add new document
            _, training_ref = trainings_ref.add(training_dict)
            self.training.id = training_ref.id
        else:
            # training was already saved - update existing document
            training_ref = trainings_ref.document(self.training.id)
            training_ref.update(training_dict)
            # remove training data from db
            for doc in training_ref.collection("data").stream():
                doc.reference.delete()
            # remove training object from list
            for i, t in enumerate(self.trainings):
                if t.id == self.training.id:
                    self.trainings.pop(i)
                    break
        # save training data into db
        for j, data in enumerate(self.training.data):
            _, _ = training_ref.collection("data").add(
                {
                    "athlete": data[0],
                    "time": data[1],
                    "id_run": j,
                }
            )
        # store training into trainings list
        self.trainings.append(self.training)
        # re-initialize training
        self.training = Training()

    def clear_training(self, i):
        """
        Remove the selected training from trainings and db.
        """
        training = self.trainings.pop(i)
        training_doc = st.session_state.db.collection(
            "teams/" + self.id + "/trainings"
        ).document(training.id)
        for data_doc in training_doc.collection("data").list_documents():
            data_doc.delete()
        training_doc.delete()

    def select_training(self, i):
        """
        Make the selected training the current one if the old current one is saved or empty.
        A new empty training is set if i=-1.
        """
        if len(self.training.data) > 0 and (self.training.id is None):
            return -1
        else:
            st_session_state.init_training()
            self.training = Training() if i == -1 else self.trainings[i]
            return 0

    def display_team(self):
        """
        Create DataFrame to display all team members.
        """
        return pd.DataFrame(
            self.athletes,
            columns=["Atleta"],
            index=pd.RangeIndex(start=1, stop=len(self.athletes) + 1),
        )

    def trainings_df(self):
        """
        Create DataFrame to contain all runs of each training.
        """
        data = []
        for i in range(len(self.trainings)):
            data += [
                [
                    i,
                    self.trainings[i].date,
                    self.trainings[i].name,
                    self.trainings[i].discipline,
                    j,
                    self.trainings[i].data[j][0],
                    self.trainings[i].data[j][1],
                ]
                for j in range(len(self.trainings[i].data))
            ]

        return pd.DataFrame(
            data,
            columns=[
                "id_training",
                "date",
                "name",
                "discipline",
                "id_run",
                "athlete",
                "time",
            ],
        )

    def trainings_info_df(self):
        """
        Create DataFrame to contain all trainings with relative info ordered by date.
        """
        data = [
            [
                i,
                self.trainings[i].id,
                self.trainings[i].date,
                self.trainings[i].name,
                self.trainings[i].discipline,
                len(set([d[0] for d in self.trainings[i].data])),
                len(self.trainings[i].data),
            ]
            for i in range(len(self.trainings))
        ]

        return (
            pd.DataFrame(
                data,
                columns=[
                    "id_training",
                    "id_db",
                    "Data",
                    "Nome",
                    "Disciplina",
                    "#Atleti",
                    "#Runs",
                ],
            )
            .sort_values("Data")
            .reset_index(drop=True)
            .set_index(pd.RangeIndex(start=1, stop=len(data) + 1))
        )
