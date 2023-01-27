import streamlit as st
import datetime
import pickle
from classes.team import Team
from classes.user import User
from screens.error_screens import screen_notLoggedIn

st.set_page_config(page_title="Skio - Importa/Esporta Dati", page_icon="❄️")

if 'user' not in st.session_state:
    screen_notLoggedIn()
    
else:
    user = st.session_state.user # type: User
    
    st.title("Importa/Esporta Dati 💻")

    # Export data
    st.header("Esporta dati")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Allenamenti in CSV", disabled=user.team.db.empty):
            st.download_button(
                label="Download CSV",
                data=user.team.db.to_csv().encode('utf-8'),
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
    st.header("Importa dati")

    loaded_state = st.file_uploader("Carica Stato Skio")
    if loaded_state:
        loaded_state_binary = pickle.loads(loaded_state.read())
        if isinstance(loaded_state_binary, Team):
            if st.button("Importa Stato Skio", on_click=user.load_team, args=[loaded_state_binary]):
                st.success("Stato Skio importato correttamente!")
        else:
            st.error("Il file caricato non è uno Stato Skio")

    st.markdown("***")
    
    # Delete everything
    st.header("Cancella dati")
    st.button("Elimina tutti i dati", on_click=user.clear_team, disabled=len(user.team.athletes)==0)
