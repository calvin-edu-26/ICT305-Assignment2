import pandas as pd
import plotly.express as px

from heuristic3.constants import COLORS, INCOME_ORDER


def chart(co2_filtered: pd.DataFrame, y_start: int, y_end: int):
    """
    Chart 5 — builds a multi-line chart of average CO2 per capita by
    income group over time. The "emissions gap" chart.

    Parameters
    ----------
    co2_filtered : pd.DataFrame
        CO2 data already filtered by year range and income group
        (see heuristic3/page.py sidebar filters).
    y_start, y_end : int
        Selected year range — used only for the chart title.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    co2_income = (
        co2_filtered.dropna(subset=["co2_per_capita", "income_group"])
        .groupby(["year", "income_group"])["co2_per_capita"].mean().reset_index()
    )
    co2_income["income_group"] = pd.Categorical(
        co2_income["income_group"], categories=INCOME_ORDER, ordered=True)

    fig = px.line(
        co2_income, x="year", y="co2_per_capita",
        color="income_group", color_discrete_map=COLORS,
        labels={"co2_per_capita": "CO₂ per Capita (tonnes)", "year": "Year",
                "income_group": "Income Group"},
        title=f"Average CO₂ per Capita by Income Group ({y_start}–{y_end})",
        template="plotly_white",
        category_orders={"income_group": INCOME_ORDER},
    )
    fig.update_traces(line_width=2.5)
    fig.update_layout(hovermode="x unified")
    return fig
