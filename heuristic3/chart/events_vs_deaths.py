import pandas as pd
import plotly.graph_objects as go

from heuristic3.constants import ACCENT


def chart(events_df: pd.DataFrame, deaths_df: pd.DataFrame, y_start: int, y_end: int):
    """
    Chart 7 — builds a dual-axis chart comparing global disaster event
    counts (bars) against total deaths (line) over time.

    Parameters
    ----------
    events_df, deaths_df : pd.DataFrame
        Full (unfiltered by income/type) events and deaths datasets — this
        chart is intentionally global, so it filters only by year range.
    y_start, y_end : int
        Selected year range.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    events_all_yr = events_df[
        (events_df["Year"] >= y_start) & (events_df["Year"] <= y_end) &
        (events_df["disaster_type"] == "All disasters")].copy()

    deaths_global_yr = (
        deaths_df[(deaths_df["Year"] >= y_start) & (deaths_df["Year"] <= y_end)]
        .groupby("Year")["All disasters"].sum().reset_index()
        .rename(columns={"All disasters": "total_deaths"})
    )
    dual = events_all_yr.merge(deaths_global_yr, on="Year", how="inner")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dual["Year"], y=dual["n_disasters"],
        name="No. of Disaster Events", marker_color="#adb5bd",
        yaxis="y1",
        hovertemplate="Year: %{x}<br>Events: %{y:,}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=dual["Year"], y=dual["total_deaths"],
        name="Total Deaths", line=dict(color=ACCENT, width=3),
        yaxis="y2",
        hovertemplate="Year: %{x}<br>Deaths: %{y:,.0f}<extra></extra>",
    ))

    if len(dual) > 0:
        deadliest = dual.loc[dual["total_deaths"].idxmax()]
        fig.add_annotation(
            x=int(deadliest["Year"]), y=float(deadliest["total_deaths"]),
            text=f"<b>{int(deadliest['Year'])}</b><br>{int(deadliest['total_deaths']):,} deaths",
            showarrow=True, arrowhead=2, arrowcolor="#333",
            font=dict(size=10), bgcolor="white", bordercolor="#333", yref="y2",
        )

    fig.update_layout(
        title=f"Global Disaster Events vs. Total Deaths ({y_start}–{y_end})",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Number of Disaster Events", side="left"),
        yaxis2=dict(title="Total Deaths", side="right", overlaying="y"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified", template="plotly_white",
    )
    return fig
