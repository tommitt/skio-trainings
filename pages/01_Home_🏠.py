import streamlit as st

from classes.user import User
from screens.error_screens import screen_notLoggedIn
from utils import st_custom_components

st.set_page_config(page_title="Skio - Il tuo Team", page_icon="❄️")

if "user" not in st.session_state:
    screen_notLoggedIn()

else:
    user = st.session_state.user  # type: User

    st.title("Il tuo Team ⛷️")

    # Athletes
    st.header("Atleti")

    # table with all athletes
    df_athletes = user.team.display_team()
    st.write(df_athletes.style.to_html(), unsafe_allow_html=True)
    st_custom_components.empty_space(1)

    # add new athlete
    col1, col2 = st.columns([3, 1])
    new_athlete = col1.text_input("Nome", label_visibility="collapsed")
    st_custom_components.button_withResponseMessage(
        button_text="Aggiungi Atleta",
        button_disabled=(new_athlete == ""),
        on_click=user.team.add_athlete,
        args=[new_athlete],
        error_message="Nome già presente",
        container=col2,
    )

    # modify existing athlete
    st.write("Modifica Atleta")
    col1, col2, col3 = st.columns([1, 2, 1])
    old_name = col1.selectbox(
        "Atleta", df_athletes["Atleta"], label_visibility="collapsed"
    )
    new_name = col2.text_input(
        "Nuovo Nome",
        key="rename_athlete_name",
        label_visibility="collapsed",
        disabled=(old_name is None),
    )
    st_custom_components.button_withResponseMessage(
        button_text="Rinomina Atleta",
        button_disabled=(new_name == ""),
        on_click=user.team.rename_athlete,
        args=[old_name, new_name],
        error_message="Nome già presente",
        container=col3,
    )

    st.markdown("***")

    # Trainings
    st.header("Allenamenti")

    # table with all trainings
    df_trainings_info = user.team.trainings_info_df()

    def highlight_selected_training(row):
        if row["id_db"] == user.team.training.id:
            return ["background-color: grey"] * len(row)
        else:
            return ["background-color: "] * len(row)

    st.write(
        df_trainings_info.style.apply(highlight_selected_training, axis=1)
        .hide(subset=["id_training", "id_db"], axis=1)
        .to_html(),
        unsafe_allow_html=True,
    )
    st_custom_components.empty_space(1)

    # interaction with specific training: select or delete
    st.write("ID Allenamento")
    col1, _, col2, col3 = st.columns(4)

    idx_selected = col1.selectbox(
        "ID Allenamento", df_trainings_info.index, label_visibility="collapsed"
    )
    id_selected = (
        None
        if df_trainings_info.empty
        else df_trainings_info.loc[idx_selected, "id_training"]
    )

    st_custom_components.button_withResponseMessage(
        button_text="Visualizza Allenamento",
        button_disabled=(idx_selected is None),
        on_click=user.team.select_training,
        args=[id_selected],
        warning_message="Hai un allenamento non salvato! Salvalo o eliminane i dati prima di selezionarne uno nuovo",
        container=col2,
    )

    button_delete_training = col3.button(
        "Elimina Allenamento", disabled=(idx_selected is None), use_container_width=True
    )
    if button_delete_training:
        st.warning("L'allenamento verrà eliminato definitivamente. Procedere?")
        st.button(
            "Procedi ed elimina",
            on_click=user.team.clear_training,
            args=[id_selected],
            use_container_width=True,
        )
    st_custom_components.empty_space(1)

    # select a new training
    st.button(
        "Nuovo Allenamento",
        on_click=user.team.select_training,
        args=[-1],
        disabled=(user.team.training.id is None),
        use_container_width=True,
    )
