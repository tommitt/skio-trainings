import re

import streamlit as st
from google.cloud.firestore_v1.base_query import FieldFilter

from classes.user import User
from utils.settings import settings


def login_screen():
    if "signedUp" not in st.session_state:
        st.session_state.signedUp = True

    regions_options = [
        "Abruzzo",
        "Basilicata",
        "Calabria",
        "Campania",
        "Emilia-Romagna",
        "Friuli-Venezia Giulia",
        "Lazio",
        "Liguria",
        "Lombardia",
        "Marche",
        "Molise",
        "Piemonte",
        "Puglia",
        "Sardegna",
        "Sicilia",
        "Toscana",
        "Trentino-Alto Adige",
        "Umbria",
        "Valle d'Aosta",
        "Veneto",
        "Estero",
    ]

    st.title("Login/signup to Skio")

    # Login form
    user_email = st.text_input("Email", placeholder="example@skio.com")
    control_email = (
        len(user_email) > 0 and True
        if re.search("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", user_email)
        else False
    )
    if len(user_email) > 0 and not control_email:
        st.warning("Email non valida")

    user_password = st.text_input(
        "Password", type="password", help="Minimo 8 caratteri"
    )
    control_password = len(user_password) >= 8
    if len(user_password) > 0 and not control_password:
        st.warning("Password non valida")

    control_login = control_email and control_password

    if st.session_state.signedUp:
        # Login button logic
        if st.button("Login", disabled=(not control_login)):
            # check if email is present in users db
            users_docs = (
                st.session_state.db.collection("users")
                .where(filter=FieldFilter("email", "==", user_email))
                .get()
            )
            if len(users_docs) == 1:
                control_db_password = (
                    user_password == users_docs[0].to_dict()["password"]
                )
                # check if password is correct
                if control_db_password:
                    # login user
                    st.session_state.user = User(
                        id=users_docs[0].id, **users_docs[0].to_dict()
                    )
                    st.session_state.user.load_team_from_db(owner=users_docs[0].id)
                    st.success("Login effettuato con successo")
                    return 0
                else:
                    # password is not correct
                    st.warning("Password non corretta")
                    st.caption(
                        f"Problemi ad accedere al tuo account? [Contattaci](mailto:{settings.contact_email})!"
                    )
                    # TODO: add "Forgot password?"
            elif len(users_docs) > 1:
                raise Exception("User is saved more than once on db")
            else:
                # user need to sign-up
                st.session_state.signedUp = False
                st.experimental_rerun()

    else:
        # Signup form
        st.info("Email non registrata - Registrati come nuovo utente")

        repeated_password = st.text_input("Ripeti password", type="password")
        control_repeated_password = repeated_password == user_password
        if len(repeated_password) > 0 and not control_repeated_password:
            st.warning("Le passwords non corrispondono")

        user_firstname = st.text_input("Nome", placeholder="Mario")
        user_lastname = st.text_input("Cognome", placeholder="Rossi")
        user_birthyear = st.number_input(
            "Anno di nascita", min_value=1940, max_value=2020, value=1990
        )
        user_region = st.selectbox("Regione in cui alleni", options=regions_options)

        control_signup = (
            control_repeated_password
            and len(user_firstname) > 0
            and len(user_lastname) > 0
        )

        col1, col2 = st.columns(2)

        # Signup button logic
        if col1.button("Registrati", disabled=(not (control_login & control_signup))):
            new_user_dict = {
                "email": user_email,
                "password": user_password,
                "firstname": user_firstname,
                "lastname": user_lastname,
                "birthyear": user_birthyear,
                "region": user_region,
            }
            # save new user into db and create their team
            _, user_doc = st.session_state.db.collection("users").add(new_user_dict)
            _, team_doc = st.session_state.db.collection("teams").add(
                {"athletes": [], "ownerId": user_doc.id}
            )
            # login new user
            st.session_state.user = User(id=user_doc.id, **new_user_dict)
            st.session_state.user.team.id = team_doc.id
            st.success("Registrazione effettuata con successo")
            return 0

        # Go back to login
        if col2.button("Torna al Login"):
            st.session_state.signedUp = True
            st.experimental_rerun()
