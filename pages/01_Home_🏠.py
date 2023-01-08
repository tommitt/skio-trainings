import streamlit as st
from classes.user import User
user = st.session_state.user # type: User


st.set_page_config(page_title="Skio - Il tuo Team", page_icon="❄️")
st.header("Il tuo Team ⛷️")

# Athletes
st.subheader("Atleti")
st.dataframe(user.team.display_team())
col1, col2 = st.columns(2)
with col1:
    new_athlete = st.text_input("Nome", key="new_athlete_name", label_visibility="collapsed")
with col2:
    st.button(
        "Aggiungi atleta",
        on_click=user.team.add_athlete,
        args=[new_athlete],
        disabled=st.session_state["new_athlete_name"]=='',
    )

# Trainings
st.subheader("Allenamenti")

df_trainings_info = user.team.trainings_info_df()
st.dataframe(df_trainings_info.drop(columns=["ID Allenamento"]))

st.write("ID Allenamento")
col1, buff, col2, col3 = st.columns(4)
idx_selected = col1.selectbox("ID Allenamento", df_trainings_info.index, label_visibility="collapsed")
id_selected = None if df_trainings_info.empty else df_trainings_info.loc[idx_selected, "ID Allenamento"]
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
