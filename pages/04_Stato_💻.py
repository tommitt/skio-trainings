import datetime
import pickle
import streamlit as st
from classes.team import Team
from classes.user import User
user = st.session_state.user # type: User


st.set_page_config(page_title="Skio - Importa/Esporta Dati", page_icon="❄️", layout="wide")
st.header("Importa/Esporta Dati 💻")

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
        file_name=datetime.datetime.now().strftime("%Y-%m-%d %H_%M") + ' Stato Skio.pkl',
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


# Delete everything
st.subheader("Cancella dati")
st.button("Elimina tutti i dati", on_click=user.clear_team, disabled=len(user.team.athletes)==0)
