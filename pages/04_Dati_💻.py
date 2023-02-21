import streamlit as st
import datetime
from classes.user import User
from screens.error_screens import screen_notLoggedIn

st.set_page_config(page_title="Skio - Importa/Esporta Dati", page_icon="❄️")

if "user" not in st.session_state:
    screen_notLoggedIn()

else:
    user = st.session_state.user  # type: User

    st.title("Importa/Esporta Dati 💻")

    # Export data
    st.header("Esporta dati")
    if st.button("Allenamenti in CSV", disabled=len(user.team.trainings) == 0):
        st.download_button(
            label="Download CSV",
            data=user.team.trainings_df().to_csv().encode("utf-8"),
            file_name=datetime.datetime.now().strftime("%Y-%m-%d %H_%M")
            + " Allenamenti.csv",
        )

    # Load data
    st.header("Importa dati")
    st.markdown(
        "Hai già un archivio dei tuoi dati e vuoi importarli su Skio?\
        \nInviaci un sample dei tuoi dati e faremo in modo di automatizzare il processo!\
        \nInviaci una [mail](mailto:{settings.contact_email}) e descrivi come questi dati sono stati raccolti\
        (ricorda di includere l'email con cui ti sei registrato/a se non è la stessa da cui scrivi)."
    )

    st.markdown("***")

    # Delete everything
    st.header("Cancella dati")
    st.button(
        "Elimina tutti i dati",
        on_click=user.clear_team,
        disabled=len(user.team.athletes) == 0,
    )
