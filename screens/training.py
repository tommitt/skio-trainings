import streamlit as st

def training_main_screen(team):
    """
    Screen to add/modify a training.
    Possibility to add training info (name, date, discipline) and the athletes runs.
    """
    st.header("Allenamento 🎿")

    # training info
    discipline_options = ['SL', 'GS', 'SG', 'DH', 'CR', 'ND']

    st.subheader("Info Allenamento")
    team.training.name = st.text_input("Nome", key='training_name')
    team.training.date = st.date_input("Data", key='training_date')
    team.training.discipline = st.selectbox("Disciplina", discipline_options, key='training_discipline')

    # athletes times
    st.subheader("Tempi Atleti")

    st.selectbox("Atleta", options=team.athletes, key='athlete')
    st.number_input("Tempo", key='time', min_value=0.0, max_value=180.0)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button("Aggiungi tempo", on_click=team.training.add_run, disabled=st.session_state["time"]==0)
    with col2:
        st.button("Aggiungi DNF", on_click=team.training.add_run, args=[True])
    with col3:
        st.button("Cancella ultimo inserimento", on_click=team.training.clear_last_run, disabled=(len(team.training.data)==0))

    st.dataframe(team.training.display_runs())
    st.caption('*DNF sono visualizzati come 1000.00')
