import numpy as np
import pandas as pd
import altair as alt

def discipline_donut_chart(df):
    """
    Create a donut chart displaying the number of trainings for each discipline.
    Display the relative % as a label.
    """
    donut_data = df.groupby(["discipline"])[["id_training"]].nunique()
            
    donut_data = donut_data.reset_index().rename(columns={
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
    
    return (
        chart_base.mark_arc(outerRadius=120, innerRadius=40)
        + chart_base.mark_text(radius=140, size=15).encode(text="%Allenamenti")
    )

def teamAvg_athlete_bar_data(df, athlete, groupby_col, target_col):
    """
    Helper function for bar charts to obtain team average values and athlete values and
    stack them into a single dataframe.
    """
    teamAvg_values = df.groupby(groupby_col)[target_col].mean()
    teamAvg_values.name = "Media"

    athlete_values = df.loc[df["athlete"] == athlete].set_index(groupby_col)[target_col]
    athlete_values.name = "Atleta"

    bar_data = pd.concat([teamAvg_values, athlete_values], axis=1).stack().reset_index()
    bar_data.columns = [groupby_col, "Atleta/Team", target_col]

    return bar_data

def dnf_bar_chart(df, athlete):
    """
    Create a bar chart displaying the % of DNFs splitted per discipline of the selected athlete
    and the team average.
    """
    df["n_dnf"] = (df["time"] == "DNF")
    df_athletes = df.groupby(["athlete", "discipline"]).agg({
        "id_training": "nunique",
        "id_run": "nunique",
        "n_dnf": "sum",
    }).reset_index()
    df_athletes["% DNF"] = df_athletes["n_dnf"] / df_athletes["id_run"] * 100

    bar_data = teamAvg_athlete_bar_data(df_athletes, athlete, "discipline", "% DNF")
    bar_data = bar_data.rename(columns={"discipline": "Disciplina"})

    return alt.Chart(bar_data).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5,
        size=50,
        ).encode(
            x='Atleta/Team',
            y=alt.Y('% DNF', scale=alt.Scale(domain=(0, 100))),
            color='Atleta/Team',
            column=alt.Column(field='Disciplina', header=alt.Header(titleColor="#c9c9c9")),
            )

def best_lap_bar_chart(df, athlete):
    """
    Create a bar chart displaying at which lap an athlete has made the best run.
    The chart shows the number of trainings for each lap number splitted between the selected
    athlete and the team average.
    """
    df["lap"] = df.groupby(["id_training", "athlete"]).transform("cumcount") + 1
    df.loc[df["lap"] >= 5, "lap"] = "5+"
    df["lap"] = df["lap"].astype(str)

    df = df.loc[df["time"] != "DNF"].copy() # drop DNFs
    df["time"] = df["time"].astype(float)

    df_grouped = df.groupby(["id_training", "athlete"]).agg({"time": ["min", "idxmin"]})
    df_grouped.columns = ["best_run_time", "best_run_idx"]

    df_grouped["best_run_lap"] = df.loc[df_grouped["best_run_idx"], "lap"].values

    best_run_laps = df_grouped.groupby(["athlete", "best_run_lap"])["best_run_time"].count().reset_index()
    best_run_laps.columns = ["athlete", "best_run_lap", "# Allenamenti"]

    bar_data = teamAvg_athlete_bar_data(best_run_laps, athlete, "best_run_lap", "# Allenamenti")
    bar_data = bar_data.rename(columns={"best_run_lap": "Giro"})

    return alt.Chart(bar_data).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5,
        size=50,
        ).encode(
            x='Atleta/Team',
            y=alt.Y('# Allenamenti', axis=alt.Axis(tickMinStep=1)),
            color='Atleta/Team',
            column=alt.Column(field='Giro', header=alt.Header(titleColor="#c9c9c9")),
            )

def helper_ida_area(df, athlete, dates):
    """
    Helper function for IDA area chart to extract athlete data, stack dates,
    assign the correct labels and return the area chart.
    """
    area_data = df.loc[df["athlete"] == athlete]
    area_data = area_data.set_index("discipline")[dates].stack().reset_index()
    area_data.columns = ["Disciplina", "Data", "IDA"]
    return alt.Chart(area_data).mark_area().encode(
        x="Data",
        y="IDA",
        color="Disciplina",
    )

def ida_area_chart(df, athlete):
    """
    Compute IDA and create a stacked area chart with IDA over time divided per discipline.
    The IDA (Index of Adaptation) is computed as IDA = (first run - best run) / first run * 60s,
    and aggregated in two different ways: cumulative (mean of the past trainings at any given date)
    and punctual (mean of trainings exactly at the given date).
    Both charts for the selected athlete are returned.
    """
    df = df.loc[df["time"] != "DNF"].copy() # drop DNFs
    df["time"] = df["time"].astype(float)

    df_dates = df.groupby(
        ["id_training", "discipline", "date", "athlete"]
        ).agg({"time": ["first", "min"]})
    df_dates.columns = ["first_run_time", "best_run_time"]
    df_dates = df_dates.reset_index()

    # IDA = (first run - best run) / first run * 60s
    df_dates["IDA"] = (
        (df_dates["first_run_time"] - df_dates["best_run_time"])
        / df_dates["first_run_time"] * 60
        )
    
    dates = sorted(df["date"].unique())
    for date in dates:
        df_dates[date] = df_dates["IDA"]
        df_dates.loc[~(df_dates["date"] <= date), date] = np.nan
    
    df_cum = df_dates.groupby(
        ["athlete", "discipline"])[dates].mean().reset_index()
    df_point = df_dates.sort_values("date").groupby(
        ["athlete", "discipline"])[dates].last().reset_index()

    return (
        helper_ida_area(df_cum, athlete, dates),
        helper_ida_area(df_point, athlete, dates),
        )
