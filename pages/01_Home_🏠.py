import streamlit as st
from classes.user import User
user = st.session_state.user # type: User


st.set_page_config(page_title="Skio - Il tuo Team", page_icon="❄️", layout="wide")
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

# headers
cols = st.columns((1, 2, 2, 2, 2))
fields = ['', 'Data', 'Nome', 'Disciplina', 'Azione']
for col, field_name in zip(cols, fields):
    col.write(field_name)

# corpus
for i, t in enumerate(user.team.trainings):
    col1, col2, col3, col4, col5 = st.columns((1, 2, 2, 2, 2))
    
    col1.write(i+1)
    col2.write(str(t.date))
    col3.write(t.name)
    col4.write(t.discipline)
    
    button_phold = col5.empty()
    button_phold.button("Vedi", key=i, on_click=user.team.select_training, args=[i])
