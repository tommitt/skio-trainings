import streamlit as st


def screen_notLoggedIn():
    st.error(
        "Accesso all'app non effettuato!\
        \nTorna alla pagina Welcome per poter iniziare a navigare."
    )
