import numpy as np
import pandas as pd
import altair as alt
from utils.settings import settings


def helper_discipline_sorter(df, discipline_col, other_cols):
    """
    Helper function to sort dataframes following discipline order specified in settings.
    """
    df["sorter"] = (
        df[discipline_col].astype("category").cat.set_categories(settings.disciplines)
    )
    df = df.set_index(["sorter"] + other_cols).sort_index().reset_index()
    return df.drop(columns=["sorter"])


def discipline_donut_chart(df):
    """
    Create a donut chart displaying the number of trainings for each discipline.
    Display the relative % as a label.
    """
    donut_data = df.groupby(["discipline"])[["id_training"]].nunique()

    donut_data = donut_data.reset_index().rename(
        columns={"id_training": "#Allenamenti", "discipline": "Disciplina"}
    )
    donut_data = helper_discipline_sorter(donut_data, "Disciplina", [])

    donut_data["%Allenamenti"] = (
        donut_data["#Allenamenti"] / donut_data["#Allenamenti"].sum() * 100
    ).round(0).astype(int).astype(str) + " %"

    chart_base = alt.Chart(donut_data).encode(
        theta=alt.Theta(field="#Allenamenti", type="quantitative", stack=True),
        color=alt.Color(field="Disciplina", type="nominal"),
    )

    return chart_base.mark_arc(outerRadius=120, innerRadius=40) + chart_base.mark_text(
        radius=140, size=15
    ).encode(text="%Allenamenti")


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
    df["n_dnf"] = df["time"] == 1000
    df_athletes = (
        df.groupby(["athlete", "discipline"])
        .agg(
            {
                "id_training": "nunique",
                "id_run": "nunique",
                "n_dnf": "sum",
            }
        )
        .reset_index()
    )
    df_athletes["% DNF"] = df_athletes["n_dnf"] / df_athletes["id_run"] * 100

    bar_data = teamAvg_athlete_bar_data(df_athletes, athlete, "discipline", "% DNF")
    bar_data = bar_data.rename(columns={"discipline": "Disciplina"})

    return (
        alt.Chart(bar_data)
        .mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5,
            size=50,
        )
        .encode(
            x="Atleta/Team",
            y=alt.Y("% DNF", scale=alt.Scale(domain=(0, 100))),
            color="Atleta/Team",
            column=alt.Column(
                field="Disciplina", header=alt.Header(titleColor="#c9c9c9")
            ),
        )
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

    df = df.loc[df["time"] < 1000].copy()  # drop DNFs

    df_grouped = df.groupby(["id_training", "athlete"]).agg({"time": ["min", "idxmin"]})
    df_grouped.columns = ["best_run_time", "best_run_idx"]

    df_grouped["best_run_lap"] = df.loc[df_grouped["best_run_idx"], "lap"].values

    best_run_laps = (
        df_grouped.groupby(["athlete", "best_run_lap"])["best_run_time"]
        .count()
        .reset_index()
    )
    best_run_laps.columns = ["athlete", "best_run_lap", "# Allenamenti"]

    bar_data = teamAvg_athlete_bar_data(
        best_run_laps, athlete, "best_run_lap", "# Allenamenti"
    )
    bar_data = bar_data.rename(columns={"best_run_lap": "Giro"})

    return (
        alt.Chart(bar_data)
        .mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5,
            size=50,
        )
        .encode(
            x="Atleta/Team",
            y=alt.Y("# Allenamenti", axis=alt.Axis(tickMinStep=1)),
            color="Atleta/Team",
            column=alt.Column(field="Giro", header=alt.Header(titleColor="#c9c9c9")),
        )
    )


def ida_line_chart(df, athlete):
    """
    Compute IDA and create a line chart with IDA over time divided per discipline.
    The IDA (Index of Adaptation) is computed as IDA = (first run - best run) / first run * 60s,
    and aggregated in two different ways: cumulative (mean of the past trainings at any given date)
    and punctual (mean of trainings exactly at the given date).
    Both charts for the selected athlete are returned, along with a table displaying the
    final cumulative IDAs for the selected athlete and the team average.
    """
    df = df.loc[df["time"] < 1000].copy()  # drop DNFs

    df_dates = df.groupby(["id_training", "discipline", "date", "athlete"]).agg(
        {"time": ["first", "min"]}
    )
    df_dates.columns = ["first_run_time", "best_run_time"]
    df_dates = df_dates.reset_index()

    # IDA = (first run - best run) / first run * 60s
    df_dates["IDA"] = (
        (df_dates["first_run_time"] - df_dates["best_run_time"])
        / df_dates["first_run_time"]
        * 60
    )

    df_dates = df_dates.groupby(["discipline", "date", "athlete"])[["IDA"]].mean()

    # compute cumulative and punctual IDAs over time
    dates = sorted(df["date"].unique())
    dates_midx = pd.MultiIndex.from_product([["cumulative", "punctual"], dates])
    df_ida = pd.DataFrame(index=df_dates.index, columns=dates_midx, dtype=float)
    for date in dates:

        # cumulative IDA
        df_ida[("cumulative", date)] = df_dates["IDA"]
        date_disciplines = (
            df_ida.loc[df_ida.index.get_level_values("date") == date]
            .index.get_level_values("discipline")
            .unique()
            .to_list()
        )
        mask_disciplines = ~(
            df_ida.index.get_level_values("discipline").isin(date_disciplines)
        )
        df_ida.loc[
            (df_ida.index.get_level_values("date") > date) | mask_disciplines,
            ("cumulative", date),
        ] = np.nan

        # punctual IDA
        mask_date = df_ida.index.get_level_values("date") == date
        df_ida.loc[mask_date, ("punctual", date)] = df_dates.loc[mask_date, "IDA"]

    df_ida = df_ida.groupby(["athlete", "discipline"]).mean().stack().reset_index()
    df_ida.columns = ["Atleta", "Disciplina", "Data", "cumulative", "punctual"]
    df_ida = helper_discipline_sorter(df_ida, "Disciplina", ["Data", "Atleta"])

    # compute final cumulative IDA for athlete and team average (for each discipline and in total)
    discipline_ida = (
        df_ida.groupby(["Disciplina", "Atleta"])["punctual"].mean().reset_index()
    )
    discipline_ida = helper_discipline_sorter(discipline_ida, "Disciplina", ["Atleta"])
    total_ida = df_ida.groupby(["Atleta"])["punctual"].mean().reset_index()
    total_ida["Disciplina"] = "Totale"

    final_ida = pd.concat([discipline_ida, total_ida])

    ida_table = pd.concat(
        [
            final_ida[final_ida["Atleta"] == athlete]
            .drop(columns=["Atleta"])
            .set_index("Disciplina"),
            final_ida.groupby("Disciplina").mean(numeric_only=True),
        ],
        axis=1,
    )
    ida_table.columns = [athlete, "Media di Team"]
    ida_table = ida_table.dropna(axis=0, how="any")

    # extract selected athlete
    line_data = df_ida[df_ida["Atleta"] == athlete]

    return (
        alt.Chart(line_data.dropna(subset=["cumulative"]))
        .mark_line(point=alt.OverlayMarkDef())
        .encode(x="Data", y=alt.Y("cumulative", title="IDA"), color="Disciplina"),
        alt.Chart(line_data.dropna(subset=["punctual"]))
        .mark_line(point=alt.OverlayMarkDef())
        .encode(x="Data", y=alt.Y("punctual", title="IDA"), color="Disciplina"),
        (ida_table.round(2).astype(str) + " s").T,
    )
