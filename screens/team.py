import datetime
import pickle
import streamlit as st
from classes.team import Team

def team_sidebar_screen(user):
    """
    Screen to display all the athletes in the team and all past trainings.
    Possibility to add new athletes to the team, save the current training and export all the data.
    """
    st.header("Team ⛷️")

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
    
    st.button("Nuovo allenamento", on_click=user.team.add_training, disabled=len(user.team.training.data)==0)
    
    st.markdown("***")
    
    # Export data
    st.subheader("Esporta dati")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Allenamenti in CSV", disabled=len(user.team.trainings)==0):
            st.download_button(
                label="Download CSV",
                data=user.team.export_data(),
                file_name=str(datetime.date.today()) + ' Allenamenti.csv',
            )
    with col2:
        st.download_button(
            label='Download Stato Skio',
            data=pickle.dumps(user.team),
            file_name=str(datetime.date.today()) + ' Stato Skio.pkl',
            disabled=len(user.team.athletes)==0,
        )
    st.caption("In questa versione alpha dell'app i dati non vengono salvati su server.\
        Ti consigliamo di esportare uno Stato Skio quando vuoi uscire dalla pagina e salvarlo sul tuo dispositivo.\
        Al prossimo utilizzo, carica il file nella sezione qua sotto e avrai nuovamente tutti i tuoi allenamenti!\
        ")

    # Load data
    st.subheader("Importa dati")

    loaded_state = st.file_uploader("Carica Stato Skio")
    if loaded_state:
        loaded_state_binary = pickle.loads(loaded_state.read())
        if isinstance(loaded_state_binary, Team):
            st.write("Stato Skio caricato!")
            st.button("Importa", on_click=user.load_team, args=[loaded_state_binary])
        else:
            st.error("Il file caricato non è accettato")
