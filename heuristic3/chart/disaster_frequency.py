import pandas as pd
import plotly.express as px


def chart(events_filtered: pd.DataFrame, y_start: int, y_end: int):
    """
    Chart 1 — builds a multi-line chart of global disaster event counts
    over time, one line per disaster type.

    Parameters
    ----------
    events_filtered : pd.DataFrame
        Events data already filtered by year range and disaster type
        (see heuristic3/page.py sidebar filters).
    y_start, y_end : int
        Selected year range — used only for the chart title.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    fig = px.line(
        events_filtered, x="Year", y="n_disasters", color="disaster_type",
        labels={"n_disasters": "Number of Disasters", "Year": "Year", "disaster_type": "Disaster Type"},
        title=f"Global Natural Disaster Frequency by Type ({y_start}–{y_end})",
        template="plotly_white",
    )
    fig.update_traces(line_width=2)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
    )
    return fig
