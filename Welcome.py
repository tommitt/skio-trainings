import streamlit as st
from classes.user import User

st.set_page_config(page_title="Skio - Archivia i tuoi allenamenti!", page_icon="❄️")

try:
    if st.session_state.user is None:
        st.session_state.user = User()
except:
    st.session_state.user = User()

st.title("Welcome to Skio! ❄️")
st.markdown(
    "In questa versione alpha di Skio puoi inserire i membri del tuo team e raccogliere in un unico posto i tempi dei tuoi allenamenti.\
    \n\nIn versioni future verranno aggiunte analisi automatiche delle presentazione come Indice di Performance, Indice di Adattamento e molti altri indicatori.\
    Per questa stagione, se raccoglierai i dati con Skio, inviaci lo Stato Skio a fine stagione per [mail](mailto:tommytassi@hotmail.it) e ti faremo avere un report.\
    \n\nNon ti rimane altro che iniziare a usare Skio!"
)

st.caption("versione: alpha")
