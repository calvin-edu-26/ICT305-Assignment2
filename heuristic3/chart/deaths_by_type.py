import pandas as pd
import plotly.express as px

from heuristic3.constants import COLORS, INCOME_ORDER

DEATH_COLS = ["Droughts", "Earthquakes", "Volcanoes", "Floods",
              "Landslides", "Storms", "Wildfires", "Extreme temperatures"]


def chart(deaths_filtered: pd.DataFrame, y_start: int, y_end: int):
    """
    Chart 4 — builds a grouped bar chart of total deaths by disaster type,
    split by income group.

    Parameters
    ----------
    deaths_filtered : pd.DataFrame
        Deaths data already filtered by year range and income group
        (see heuristic3/page.py sidebar filters).
    y_start, y_end : int
        Selected year range — used only for the chart title.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    deaths_melted = deaths_filtered.melt(
        id_vars=["Entity", "Year", "income_group"],
        value_vars=DEATH_COLS,
        var_name="disaster_type", value_name="deaths"
    ).dropna(subset=["deaths", "income_group"])

    deaths_grouped = (
        deaths_melted.groupby(["disaster_type", "income_group"])["deaths"]
        .sum().reset_index()
    )
    deaths_grouped["income_group"] = pd.Categorical(
        deaths_grouped["income_group"], categories=INCOME_ORDER, ordered=True)

    fig = px.bar(
        deaths_grouped, x="disaster_type", y="deaths",
        color="income_group", color_discrete_map=COLORS, barmode="group",
        labels={"deaths": "Total Deaths", "disaster_type": "Disaster Type", "income_group": "Income Group"},
        title=f"Total Deaths by Disaster Type and Income Group ({y_start}–{y_end})",
        template="plotly_white",
        category_orders={"income_group": INCOME_ORDER},
    )
    fig.update_layout(
        xaxis_tickangle=-30,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
