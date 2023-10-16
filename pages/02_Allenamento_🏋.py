import streamlit as st

from classes.user import User
from screens.error_screens import screen_notLoggedIn
from utils import st_custom_components
from utils.settings import settings

st.set_page_config(page_title="Skio - Aggiunta Allenamento", page_icon="❄️")

if "user" not in st.session_state:
    screen_notLoggedIn()

else:
    user = st.session_state.user  # type: User

    st.title("Aggiunta Allenamento 🎿")

    # training info
    st.subheader("Info Allenamento")
    user.team.training.name = st.text_input("Nome", value=user.team.training.name)
    user.team.training.date = st.date_input("Data", value=user.team.training.date)
    discipline_idx = settings.disciplines.index(user.team.training.discipline)
    user.team.training.discipline = st.selectbox(
        "Disciplina", settings.disciplines, index=discipline_idx
    )

    # athletes times
    st.subheader("Tempi Atleti")

    st.selectbox("Atleta", options=user.team.athletes, key="running_athlete")
    # st_custom_components.chronometer()
    st.number_input(
        "Tempo", key="running_time", min_value=0.0, max_value=settings.max_time
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button(
            "Aggiungi tempo",
            on_click=user.team.training.add_run,
            disabled=(st.session_state["running_time"] == 0),
        )
    with col2:
        st.button(
            "Aggiungi DNF",
            on_click=user.team.training.add_run,
            args=[True],
            disabled=(st.session_state["running_athlete"] is None),
        )
    with col3:
        st.button(
            "Cancella ultimo inserimento",
            on_click=user.team.training.clear_last_run,
            disabled=(len(user.team.training.data) == 0),
        )

    st.dataframe(user.team.training.display_runs())
    st.caption("*DNF sono visualizzati come 1000.00")

    st.button(
        "Salva allenamento",
        on_click=user.team.add_training,
        disabled=len(user.team.training.data) == 0,
    )
