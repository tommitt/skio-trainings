import streamlit as st
from classes.user import User
from screens.error_screens import screen_notLoggedIn

st.set_page_config(page_title="Skio - Il tuo Team", page_icon="❄️")

if 'user' not in st.session_state:
    screen_notLoggedIn()

else:
    user = st.session_state.user # type: User    
    
    st.title("Il tuo Team ⛷️")

    # Athletes
    st.header("Atleti")
    df_athletes = user.team.display_team()
    st.dataframe(df_athletes)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_input("Nome", key="new_athlete_name", label_visibility="collapsed")
    with col2:
        st.button(
            "Aggiungi Atleta",
            on_click=user.team.add_athlete,
            args=[st.session_state["new_athlete_name"]],
            disabled=(st.session_state["new_athlete_name"]==''),
        )

    st.write("Modifica Atleta")
    col1, col2, col3 = st.columns([1, 2, 1])
    old_name = col1.selectbox("Atleta", df_athletes["Atleta"], label_visibility="collapsed")
    col2.text_input(
        "Nuovo Nome",
        key="rename_athlete_name",
        label_visibility="collapsed",
        disabled=(old_name is None),
        )
    col3.button(
        "Rinomina Atleta",
        on_click=user.team.rename_athlete,
        args=[old_name, st.session_state["rename_athlete_name"]],
        disabled=(st.session_state["rename_athlete_name"]==''),
        )

    st.markdown("***")

    # Trainings
    st.header("Allenamenti")

    df_trainings_info = user.team.trainings_info_df()
    st.dataframe(df_trainings_info.drop(columns=["id_training"]))

    st.write("ID Allenamento")
    col1, _, col2, col3 = st.columns(4)
    idx_selected = col1.selectbox("ID Allenamento", df_trainings_info.index, label_visibility="collapsed")
    id_selected = None if df_trainings_info.empty else df_trainings_info.loc[idx_selected, "id_training"]
    col2.button(
        "Visualizza Allenamento",
        on_click=user.team.select_training,
        args=[id_selected],
        disabled=(idx_selected is None),
        )
    col3.button(
        "Elimina Allenamento",
        on_click=user.team.clear_training,
        args=[id_selected],
        disabled=(idx_selected is None),
        )
