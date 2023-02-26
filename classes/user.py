import streamlit as st
import datetime
from classes.team import Team
from classes.training import Training


class User:
    def __init__(self, id, email, password, firstname, lastname, birthyear, region):
        self.id = id
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.birthyear = birthyear
        self.region = region
        self.team = Team()

    def load_team_from_db(self, owner):
        """
        Load the team that the user owns from db.
        """
        teams_docs = (
            st.session_state.db.collection("teams").where("ownerId", "==", owner).get()
        )
        if len(teams_docs) == 1:
            self.team.id = teams_docs[0].id
            self.team.athletes = sorted(teams_docs[0].to_dict()["athletes"])
            for t in teams_docs[0].reference.collection("trainings").stream():
                training = Training(
                    id=t.id,
                    name=t.to_dict()["name"],
                    date=datetime.date.fromtimestamp(t.to_dict()["date"].timestamp()),
                    discipline=t.to_dict()["discipline"],
                )
                for run in t.reference.collection("data").order_by("id_run").stream():
                    training.data.append(
                        [run.to_dict()["athlete"], run.to_dict()["time"]]
                    )
                self.team.trainings.append(training)
        elif len(teams_docs) > 1:
            raise Exception("The user has associated more than one team")
        else:
            raise Exception("The user doesn't own any team")
