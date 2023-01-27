import streamlit as st
from classes.user import User
from screens.error_screens import screen_notLoggedIn
from utils.statistics_charts import *

st.set_page_config(page_title="Skio - Statistiche", page_icon="❄️")

if 'user' not in st.session_state:
    screen_notLoggedIn()
    
else:
    user = st.session_state.user # type: User
    
    st.title("Statistiche 📊")

    # Frame data
    df = user.team.db.copy()

    if df.empty:
        st.info("Nessun dato da visualizzare")
        
    else:
        # Team statistics
        st.header("Statistiche di Team")

        # Number of trainings x discipline
        st.subheader("Allenamenti per Disciplina")
        st.altair_chart(discipline_donut_chart(df), theme="streamlit")
        
        # Athlete statistics
        st.markdown("***")
        st.header("Statistiche per Atleta")
        athlete_selected = st.selectbox("Atleta", options=user.team.athletes)

        # DNF %
        st.subheader("Percentuale di DNF")
        st.altair_chart(dnf_bar_chart(df, athlete_selected), theme=None)

        # Adaptation to the track
        st.subheader("Giro al Miglior Tempo")
        st.altair_chart(best_lap_bar_chart(df, athlete_selected), theme=None)

        # Index of Adaptation (IDA)
        st.subheader("IDA (Indice Di Adattamento)")
        cumulative_ida, punctual_ida, ida_table = ida_line_chart(df, athlete_selected)
        tab1, tab2 = st.tabs(["Cumulativo", "Puntuale"])
        with tab1:
            st.altair_chart(cumulative_ida, theme="streamlit")
        with tab2:
            st.altair_chart(punctual_ida, theme="streamlit")
        st.dataframe(ida_table)
        st.caption(
            "IDA: Indice Di Adattamento (normalizzato a 60 s)\
            \nSappiamo quanto sia importante nel nostro sport il primo giro, quello che poi conta in gara.\
            \nPer questo abbiamo elaborato questo indice che serve per valutare il primo giro dell'atleta.\
            \nMostra il tempo ipotetico che ci metterebbe in meno nel primo giro se l'atleta lo facesse al suo massimo potenziale.\
            \nSempre riportato ad un tracciato da un minuto esatto, quindi confrontabile in ogni allenamento."
        )

