import streamlit as st
user = st.session_state.user

st.set_page_config(page_title="Skio - Aggiunta Allenamento", page_icon="❄️", layout="wide")
st.header("Aggiunta Allenamento 🎿")

# training info
discipline_options = ['SL', 'GS', 'SG', 'DH', 'CR', 'ND']

st.subheader("Info Allenamento")
user.team.training.name = st.text_input("Nome", key='training_name')
user.team.training.date = st.date_input("Data", key='training_date')
user.team.training.discipline = st.selectbox("Disciplina", discipline_options, key='training_discipline')

# athletes times
st.subheader("Tempi Atleti")

st.selectbox("Atleta", options=user.team.athletes, key='athlete')
st.number_input("Tempo", key='time', min_value=0.0, max_value=180.0)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.button(
        "Aggiungi tempo",
        on_click=user.team.training.add_run,
        disabled=(st.session_state["time"]==0),
    )
with col2:
    st.button(
        "Aggiungi DNF",
        on_click=user.team.training.add_run,
        args=[True],
        disabled=(st.session_state["athlete"] is None),
    )
with col3:
    st.button(
        "Cancella ultimo inserimento",
        on_click=user.team.training.clear_last_run,
        disabled=(len(user.team.training.data)==0),
    )

st.dataframe(user.team.training.display_runs())
st.caption('*DNF sono visualizzati come 1000.00')

st.button("Salva allenamento", on_click=user.team.add_training, disabled=len(user.team.training.data)==0)
