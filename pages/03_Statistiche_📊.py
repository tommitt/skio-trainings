import streamlit as st
import pandas as pd
import altair as alt
from classes.user import User
from screens.error_screens import screen_notLoggedIn

st.set_page_config(page_title="Skio - Statistiche", page_icon="❄️")

if 'user' not in st.session_state:
    screen_notLoggedIn()
    
else:
    user = st.session_state.user # type: User
    
    st.title("Statistiche 📊")

    # Frame data
    df = user.team.trainings_df()

    if df.empty:
        st.info("Nessun dato da visualizzare")
        
    else:
        # Discipline split
        st.header("Statistiche di Team")

        # Number of trainings x discipline
        st.subheader("Allenamenti per Disciplina")
        df_disciplines = df.groupby(["discipline"])[["id_training"]].nunique()
        
        donut_data = df_disciplines.reset_index().rename(columns={
            "id_training": "#Allenamenti",
            "discipline": "Disciplina"
            })
        donut_data["%Allenamenti"] = (
            donut_data["#Allenamenti"] / donut_data["#Allenamenti"].sum() * 100
            ).round(0).astype(int).astype(str) + " %"

        chart_base = alt.Chart(donut_data).encode(
            theta=alt.Theta(field="#Allenamenti", type="quantitative", stack=True),
            color=alt.Color(field="Disciplina", type="nominal"),
            )
        
        st.altair_chart((
            chart_base.mark_arc(outerRadius=120, innerRadius=40) +
            chart_base.mark_text(radius=150, size=15).encode(text="%Allenamenti")
        ), theme=None)
        
        # Select athlete
        st.markdown("***")
        st.header("Statistiche per Atleta")
        athlete_selected = st.selectbox("Atleta", options=user.team.athletes)

        # DNF %
        st.subheader("Percentuale di DNF")

        df["n_dnf"] = df["time"] == "DNF"
        df_athletes = df.groupby(["athlete", "discipline"]).agg({
            "id_training": "nunique",
            "id_run": "nunique",
            "n_dnf": "sum",
        }).reset_index()
        df_athletes["perc_dnf"] = df_athletes["n_dnf"] / df_athletes["id_run"] * 100

        perc_dnf_mean = df_athletes.groupby("discipline")["perc_dnf"].mean()
        perc_dnf_mean.name = "Media"
        perc_dnf_selected = df_athletes.loc[
            df_athletes["athlete"] == athlete_selected
            ].set_index("discipline")["perc_dnf"]
        perc_dnf_selected.name = "Atleta"

        bar_data = pd.concat([perc_dnf_mean, perc_dnf_selected], axis=1).stack().reset_index()
        bar_data.columns = ["Disciplina", "Atleta/Team", "% DNF"]

        chart = alt.Chart(bar_data).mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5,
            size=50,
            ).encode(
                x='Atleta/Team',
                y=alt.Y('% DNF', scale=alt.Scale(domain=(0, 100))),
                color='Atleta/Team',
                column='Disciplina'
                )

        st.altair_chart(chart, theme=None)
