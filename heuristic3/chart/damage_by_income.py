import pandas as pd
import plotly.express as px

from heuristic3.constants import ACCENT, COLORS, INCOME_ORDER


def chart(damage_df: pd.DataFrame, y_start: int, y_end: int, selected_income: list):
    """
    Chart 6 — builds a bar chart of average economic disaster damage
    (% of GDP) by income group. The "consequences gap" chart.

    Parameters
    ----------
    damage_df : pd.DataFrame
        Full (unfiltered) damage dataset — filtered internally here by year
        range and income group so the chart doesn't depend on Chart 2's
        filtered frame.
    y_start, y_end : int
        Selected year range.
    selected_income : list of str
        Income groups selected via sidebar multiselect.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    damage_by_income = (
        damage_df[
            (damage_df["Year"] >= y_start) & (damage_df["Year"] <= y_end) &
            (damage_df["income_group"].isin(selected_income))
        ].dropna(subset=["income_group", "All disasters"])
        .groupby("income_group")["All disasters"].mean().reset_index()
    )
    damage_by_income["income_group"] = pd.Categorical(
        damage_by_income["income_group"], categories=INCOME_ORDER, ordered=True)
    damage_by_income = damage_by_income.sort_values("income_group")

    fig = px.bar(
        damage_by_income, x="income_group", y="All disasters",
        color="income_group", color_discrete_map=COLORS,
        labels={"All disasters": "Avg Damage (% of GDP)", "income_group": "Income Group"},
        title=f"Average Economic Damage as % of GDP by Income Group ({y_start}–{y_end})",
        template="plotly_white",
        category_orders={"income_group": INCOME_ORDER},
    )
    fig.update_layout(showlegend=False)

    low_val = damage_by_income[damage_by_income["income_group"] == "Low Income"]["All disasters"]
    if len(low_val) > 0:
        fig.add_annotation(
            x="Low Income", y=float(low_val.values[0]),
            text=f"<b>{float(low_val.values[0]):.2f}%</b> of GDP",
            showarrow=True, arrowhead=2,
            arrowcolor=ACCENT, font=dict(color=ACCENT, size=11),
            bgcolor="white", bordercolor=ACCENT,
        )

    return fig
