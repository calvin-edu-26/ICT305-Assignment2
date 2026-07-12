import pandas as pd
import plotly.express as px

from heuristic3.constants import COLORS, INCOME_ORDER


def chart(damage_filtered: pd.DataFrame, y_start: int, y_end: int, top_n: int = 20):
    """
    Chart 2 — builds a horizontal bar chart of the top N countries by
    average economic disaster damage as a percentage of GDP.

    Parameters
    ----------
    damage_filtered : pd.DataFrame
        Damage data already filtered by year range and income group
        (see heuristic3/page.py sidebar filters).
    y_start, y_end : int
        Selected year range — used only for the chart title.
    top_n : int
        Number of countries to show, ranked by average damage. Default 20.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    top_damage = (
        damage_filtered.groupby(["Entity", "income_group"])["All disasters"]
        .mean().dropna().reset_index()
        .sort_values("All disasters", ascending=False).head(top_n)
    )
    top_damage["income_group"] = pd.Categorical(
        top_damage["income_group"], categories=INCOME_ORDER, ordered=True)

    fig = px.bar(
        top_damage, x="All disasters", y="Entity",
        color="income_group", color_discrete_map=COLORS,
        orientation="h",
        labels={"All disasters": "Avg Economic Damage (% of GDP)", "Entity": "Country",
                "income_group": "Income Group"},
        title=f"Top {top_n} Countries by Average Economic Damage as % of GDP ({y_start}–{y_end})",
        template="plotly_white",
        category_orders={"income_group": INCOME_ORDER},
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(hovertemplate="<b>%{y}</b><br>Avg Damage: %{x:.2f}% of GDP<extra></extra>")
    return fig
