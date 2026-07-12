import pandas as pd
import plotly.express as px

from heuristic3.constants import COLORS, INCOME_ORDER


def build_scatter_data(co2_df: pd.DataFrame, damage_filtered: pd.DataFrame, y_start: int, y_end: int) -> pd.DataFrame:
    """
    Builds the country-level dataset behind Chart 3: average GDP per capita
    and CO2 per capita (from co2_df) merged with average disaster damage
    as % of GDP (from damage_filtered) over the selected year range.

    Also reused by heuristic3/chart/ml_regression.py, since the regression
    model is fit on exactly this same country-level table.

    Parameters
    ----------
    co2_df : pd.DataFrame
        Full (unfiltered-by-income) CO2/GDP dataset.
    damage_filtered : pd.DataFrame
        Damage data already filtered by year range and income group.
    y_start, y_end : int
        Selected year range.

    Returns
    -------
    pd.DataFrame with columns: Entity, income_group, All disasters,
    gdp_per_capita, co2_per_capita
    """
    co2_avg = (
        co2_df[co2_df["year"].between(y_start, y_end)]
        .groupby("country")[["gdp_per_capita", "co2_per_capita"]]
        .mean().reset_index().rename(columns={"country": "Entity"})
    )
    damage_avg = (
        damage_filtered.groupby(["Entity", "income_group"])["All disasters"]
        .mean().dropna().reset_index()
    )
    return damage_avg.merge(co2_avg, on="Entity", how="inner").dropna()


def chart(scatter_data: pd.DataFrame, y_start: int, y_end: int):
    """
    Chart 3 — builds a bubble scatter of wealth (GDP per capita) vs disaster
    damage burden, with bubble size showing CO2 per capita.

    Parameters
    ----------
    scatter_data : pd.DataFrame
        Output of build_scatter_data() above.
    y_start, y_end : int
        Selected year range — used only for the chart title.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    fig = px.scatter(
        scatter_data, x="gdp_per_capita", y="All disasters",
        color="income_group", color_discrete_map=COLORS,
        size="co2_per_capita", size_max=25, hover_name="Entity",
        hover_data={"gdp_per_capita": ":.0f", "All disasters": ":.3f",
                    "co2_per_capita": ":.2f", "income_group": True},
        labels={
            "gdp_per_capita": "GDP per Capita (USD, 2011 PPP)",
            "All disasters": "Avg Economic Damage (% of GDP)",
            "income_group": "Income Group", "co2_per_capita": "CO₂ per Capita (tonnes)",
        },
        title=f"Wealth vs. Disaster Damage Burden — Bubble Size = CO₂ per Capita ({y_start}–{y_end})",
        template="plotly_white",
        category_orders={"income_group": INCOME_ORDER},
    )
    return fig
