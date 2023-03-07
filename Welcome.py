import json
import time

import streamlit as st
from google.cloud import firestore

from screens.login_screen import login_screen
from utils.settings import settings

st.set_page_config(page_title="Skio - Archivia i tuoi allenamenti!", page_icon="❄️")

if "user" not in st.session_state:
    # connect to Firestore db
    if "db" not in st.session_state:
        try:
            st.session_state.db = firestore.Client.from_service_account_info(
                json.loads(st.secrets["firebase"]["firestore"])
            )
        except Exception as e:
            raise Exception("Connection to remote db failed:", e)

    # login user
    login_return = login_screen()
    if login_return == 0:
        time.sleep(1)
        st.experimental_rerun()
else:
    st.title("Welcome to Skio! ❄️")
    st.markdown(
        f"Siamo felici di darti il benvenuto nella versione beta di Skio!\
        \n\nSkio è un'app che ti permette di generare analisi automatiche delle prestazione del tuo team.\
        \nAggiungi gli atleti al tuo team e raccogli i dati dei tuoi allenamenti - \
        dopodiché, esplora l'Indice Di Adattamento, la Percentuale di DNF e tanto altro nella sezione Statistiche.\
        \n\nSkio è in continuo aggiornamento, se hai consigli su come potremmo migliorarci, non esitare a [contattarci](mailto:{settings.contact_email}).\
        \n\nAdesso non ti rimane altro che iniziare a usare Skio!"
    )

    st.caption("versione: " + settings.version)
